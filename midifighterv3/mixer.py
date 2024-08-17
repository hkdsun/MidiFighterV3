from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.components import MixerComponent as MixerComponentBase
from ableton.v3.control_surface.controls import ButtonControl

from ableton.v3.base import listens
from .track_macro import TrackMacroComponent
from functools import partial
import logging
logger = logging.getLogger("HK-DEBUG")


class MixerComponent(MixerComponentBase):
    def __init__(self, *a, **k):
        self._track_macros = TrackMacroComponent()
        (super(MixerComponent, self).__init__)(*a, **k)

        self._MixerComponent__on_target_track_changed.subject = self._target_track
        self.__on_target_track_changed() if self._target_track else None
        self.set_target_track_macro_controls = partial(self._track_macros.set_parameter_controls)

    @listens('target_track')
    def __on_target_track_changed(self):
        self._track_macros.set_track(self._target_track.target_track)
        default_device = None
        for device in self._target_track.target_track.devices:
            if device.name == 'Macro Filter+EQ':
                default_device = device
                break
        if default_device is None:
            for device in self._target_track.target_track.devices:
                if device.type == 1:
                    default_device = device
                    break
        if default_device is None:
            return
        self.song.view.select_device(default_device, False)
