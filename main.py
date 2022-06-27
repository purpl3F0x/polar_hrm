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

import asyncio

from polar_hrm import PolarHRM


async def main(address):
    async with PolarHRM(address, timeout=100) as client:
        print(f"Connected: {client.is_connected}")
        # await client.start_listening_hr_broadcasts()
        # await client.enable_pdm_notifications()
        #
        # await asyncio.gather(*[client.request_stream_settings(i) for i in range(15)])
        # # await asyncio.gather(*[client.request_stream_settings(i) for i in range(2, 16)])
        #
        # await asyncio.sleep(300)
        # await client.disable_hr_measurement_notifications()

        await client.start_listening_hr_broadcasts()

        await asyncio.sleep(10)


if __name__ == "__main__":
    ADDRESS = "FB:D5:69:F9:76:7A"
    import logging

    logging.basicConfig(level=logging.DEBUG)

    asyncio.run(
        main(ADDRESS)
    )
