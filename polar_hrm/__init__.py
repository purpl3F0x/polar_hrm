"""Top-level package for polar_hrm."""

__author__ = """Stavros Avramidis"""
__email__ = "stavros9899@gmail.com"

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

import logging

from .__version__ import __version__
from .datatypes import *
from .polar_hrm import *

_logger = logging.getLogger(__name__)
# _logger.addHandler(logging.NullHandler())
