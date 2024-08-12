from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.components import DeviceNavigationComponent as DeviceNavigationComponentBase
from ableton.v3.control_surface.controls import EncoderControl, ButtonControl

from ableton.v3.base import listens
from ableton.v3.base import sign
from .track_macro import TrackMacroComponent
from functools import partial
import logging
logger = logging.getLogger("HK-DEBUG")


class DeviceNavigationComponent(DeviceNavigationComponentBase):
    scrolling_step_delay = 0.8
