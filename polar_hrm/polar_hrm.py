#  Copyright (c) - Stavros Avramidis 2022.
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
#
#
#
#
#
#
#


import asyncio
import logging
from typing import Union

from bleak import BleakClient
from bleak.backends.device import BLEDevice

from .datatypes import *

_logger = logging.getLogger(__name__)


class PolarHRM(BleakClient):
    HEART_RATE_MEASUREMENT_CHARACTERISTIC_ID = "00002a37-0000-1000-8000-00805f9b34fb"
    PMD_SERVICE = "FB005C80-02E7-F387-1CAD-8ACD2D8DF0C8"
    PMD_CTRL_CHARACTERISTIC_ID = "FB005C81-02E7-F387-1CAD-8ACD2D8DF0C8"
    PMD_DATA_CHARACTERISTIC_ID = "FB005C82-02E7-F387-1CAD-8ACD2D8DF0C8"

    def __init__(self, address_or_ble_device: Union[BLEDevice, str], **kwargs):
        super().__init__(address_or_ble_device, **kwargs)

        # Callbacks
        self._hr_measurement_callback = None

        self.request_settings_observer = asyncio.Condition()
        self.request_settings_buffer = None

    async def read_pdm_ctrl(self) -> bytearray:
        return await self.read_gatt_char(PolarHRM.PMD_CTRL_CHARACTERISTIC_ID)

    async def write_pdm_ctrl(self, data: Union[bytes, bytearray, memoryview], response: bool = False) -> None:
        await self.write_gatt_char(PolarHRM.PMD_CTRL_CHARACTERISTIC_ID, data, response)

    async def start_listening_hr_broadcasts(self) -> None:
        await self.start_notify(PolarHRM.HEART_RATE_MEASUREMENT_CHARACTERISTIC_ID,
                                self.__hr_measurement_notification_handler)

    async def stop_listening_hr_broadcasts(self) -> None:
        await self.stop_notify(PolarHRM.HEART_RATE_MEASUREMENT_CHARACTERISTIC_ID)

    async def enable_pdm_notifications(self) -> None:
        await self.start_notify(PolarHRM.PMD_CTRL_CHARACTERISTIC_ID, self.__pdm_ctrl_notification_handler)
        await self.start_notify(PolarHRM.PMD_DATA_CHARACTERISTIC_ID, self.__pdm_data_notification_handler)

        a = await self.read_pdm_ctrl()
        _logger.debug(a)

    async def disable_pdm_notifications(self) -> None:
        await self.stop_notify(PolarHRM.PMD_CTRL_CHARACTERISTIC_ID)
        await self.stop_notify(PolarHRM.PMD_DATA_CHARACTERISTIC_ID)

    async def request_stream_settings(self, stream_type):
        _logger.debug(f"Requesting stream settings: {stream_type}")

        async with self.request_settings_observer:
            # await self.request_settings_observer.wait()
            _logger.debug(f"Making request: {stream_type}")
            await self.write_pdm_ctrl(bytearray([PmdControlPointCommands.GET_MEASUREMENT_SETTINGS, int(stream_type)]), response=True)

            await self.request_settings_observer.wait_for(lambda: self.request_settings_buffer is not None)
            response = self.request_settings_buffer
            self.request_settings_buffer = None
            _logger.debug(f"Got Settings Response: {response}")

        return []

    async def request_full_stream_settings(self, stream_type):
        _logger.debug(f"Requesting full stream settings: {stream_type}")

        async with self.request_settings_observer:
            # await self.request_settings_observer.wait()

            _logger.debug(f"Making request: {stream_type}")
            await self.write_pdm_ctrl(bytearray([PmdControlPointCommands.GET_SDK_MODE_SETTINGS, int(stream_type)]), response=True)

            await self.request_settings_observer.wait_for(lambda: self.request_settings_buffer is not None)
            response = self.request_settings_buffer
            self.request_settings_buffer = None
            _logger.debug(f"Got Full-Settings Response: {response}")

        return []

    async def start_ecg_streaming(self, settings: PolarSensorSetting = None):
        raise NotImplementedError

    async def start_acc_streaming(self, settings: PolarSensorSetting = None):
        raise NotImplementedError

    async def start_gyro_streaming(self, settings: PolarSensorSetting = None):
        raise NotImplementedError

    async def start_magnetometer_streaming(self, settings: PolarSensorSetting = None):
        raise NotImplementedError

    async def start_ohr_streaming(self, settings: PolarSensorSetting = None):
        raise NotImplementedError

    async def start_ohr_ppi_streaming(self, settings: PolarSensorSetting = None):
        raise NotImplementedError

    async def enable_sdk_mode(self):
        raise NotImplementedError

    async def disable_sdk_mode(self):
        raise NotImplementedError

    def set_hr_measurement_handler(self, callback):
        self._hr_measurement_callback = callback

    def __hr_measurement_notification_handler(self, _sender: int, data: bytearray):
        # _logger.debug(_sender, data)
        data = PolarHRM.__parse_hr_measurement(data)
        if self._hr_measurement_callback:
            try:
                self._hr_measurement_callback(data)
            except ... as e:
                _logger.exception(f"Exception running hr callback: {e}")
            finally:
                return

    def __pdm_ctrl_notification_handler(self, _sender: int, data: bytearray):
        # _logger.debug("PDM CTRL: ", _sender, data)
        self.request_settings_buffer = data

        # self.request_settings_observer.notify()

    def __pdm_data_notification_handler(self, _sender: int, data: bytearray):
        _logger.debug(f"PDM DATA {_sender} {data}")

    @staticmethod
    def __parse_hr_measurement(data):
        flags = data[0]

        is_uint16_measurement_mask = 0x01
        is_contact_detected_mask = 0x06
        is_energy_expended_present_mask = 0x08
        is_rr_interval_present_mask = 0x10

        sensor_contact = None
        bpm = None
        rr_interval = []
        energy_expended = None

        measurement_byte_offset = 1
        contact = bool(flags & is_contact_detected_mask)

        if flags & is_uint16_measurement_mask:
            bpm = int.from_bytes(data[measurement_byte_offset:measurement_byte_offset + 2], 'little')
            measurement_byte_offset += 2
        else:
            bpm = data[measurement_byte_offset]
            measurement_byte_offset += 1

        if flags & is_energy_expended_present_mask:
            energy_expended = int.from_bytes(data[measurement_byte_offset:measurement_byte_offset + 2], 'little')
            measurement_byte_offset += 2

        if flags & is_rr_interval_present_mask:
            while len(data[measurement_byte_offset:]) >= 2:
                rr_interval.append(int.from_bytes(data[measurement_byte_offset:measurement_byte_offset + 2], 'little'))
                measurement_byte_offset += 2

        return HeartRateMeasurement(contact=contact,
                                    bpm=bpm,
                                    RR=rr_interval,
                                    energy_expended=energy_expended)

    @staticmethod
    def __parse_settings_frame(data):
        pass
