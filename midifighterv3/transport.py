from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v3.control_surface.controls import EncoderControl, ButtonControl

from ableton.v3.base import listens
from ableton.v3.base import sign
from .track_macro import TrackMacroComponent
from functools import partial
import logging
logger = logging.getLogger("HK-DEBUG")


class TransportComponent(TransportComponentBase):
    loop_length_control = EncoderControl()

    def __init__(self, *a, **k):
        (super(TransportComponent, self).__init__)(*a, **k)

    def _apply_value_to_arrangement_property(self, property_name, value):
        factor = 0.25 if self.shift_button.is_pressed else 1.0
        delta = factor * sign(value)
        old_value = getattr(self.song, property_name)
        setattr(self.song, property_name, max(0.0, old_value + delta))

    @loop_length_control.value
    def loop_length_control(self, value, _):
        self._apply_value_to_arrangement_property("loop_length", value)
