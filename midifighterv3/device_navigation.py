from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.components import DeviceNavigationComponent as DeviceNavigationComponentBase
from ableton.v3.control_surface.controls import StepEncoderControl

from ableton.v3.base import listens
from ableton.v3.base import sign
import logging
logger = logging.getLogger("HK-DEBUG")


class DeviceNavigationComponent(DeviceNavigationComponentBase):

    def __init__(self, *a, **k):
        super(DeviceNavigationComponent, self).__init__(*a, **k)
        self.scroll_encoder._stepper.num_steps = 4
