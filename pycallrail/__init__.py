"""
CallRail API Wrapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Python wrapper for the CallRail API.

:copyright: (c) 2023 by Predictive Data Lab
:license: MIT, see LICENSE for more details.

"""

__title__ = 'pycallrail'
__author__ = 'Engineering @ Predictive Data Lab'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023 by Predictive Data Lab'
__version__ = '0.9.0.1'

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

import logging
from typing import NamedTuple, Literal

from callrail import *
from base import *
from errors import *
from helpers import *
from mixins import *
from objects import *

class VersionInfo(NamedTuple):
    major: int
    minor: int
    revision: int
    build: int
    release: Literal['alpha', 'beta', 'rc', 'final']

version_info: VersionInfo = VersionInfo(
    major=0,
    minor=9,
    revision=0,
    build=0,
    release='final'
)

logging.getLogger(__name__).addHandler(logging.NullHandler())

del logging, NamedTuple, Literal, VersionInfo