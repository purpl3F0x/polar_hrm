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

from enum import Enum, unique
from typing import NamedTuple


class HeartRateMeasurement(NamedTuple):
    """Namedtuple for measurement values.
    * `HeartRateMeasurementValues.bpm`
            Heart rate (int), in beats per minute.
    * `HeartRateMeasurementValues.list`
            ``True`` if device is contacting the body, ``False`` if not,
            ``None`` if device does not support contact detection.
    * `HeartRateMeasurementValues.energy_expended`
            Energy expended (int), in kilo joules, or ``None`` if no value.
    * `HeartRateMeasurementValues.rr`
            Sequence of RR intervals, measuring the time between
            beats. Oldest first, in ints that are units of 1024ths of a second.
            This sequence will be empty if the device does not report the intervals.
    """
    bpm: int
    RR: list[int]
    contact: bool
    energy_expended: int


@unique
class DeviceStreamingFeature(int, Enum):
    ECG = 0
    PPG = 1
    ACC = 2
    PPI = 3
    # 4 RFU
    GYRO = 5
    MAGN = 6
    # 7 - 255 RFU


@unique
class Recording(int, Enum):
    INTERVAL_1s = 1
    INTERVAL_5s = 5


@unique
class FeatureSettingID(int, Enum):
    HR = 1
    DEVICE_INFO = 2
    BATTERY_STATUS = 4
    POLAR_SENSOR_STREAMING = 8
    POLAR_FILE_TRANSFER = 16
    ALL = 0xFF


class PolarSensorSetting(NamedTuple):
    @unique
    class Type(int, Enum):
        SAMPLE_RATE = 0
        RESOLUTION = 1
        RANGE = 2
        RANGE_MILLI = 3
        CHANNELS = 4
        UNKNOWN = 0xFF

    ID: Type
    val: set


@unique
class PmdControlPointCommands(int, Enum):
    GET_MEASUREMENT_SETTINGS = 0x01
    REQUEST_MEASUREMENT_START = 0x02
    STOP_MEASUREMENT = 0x03
    GET_SDK_MODE_SETTINGS = 0x04


PolarSensorSettings: list[PolarSensorSetting]
