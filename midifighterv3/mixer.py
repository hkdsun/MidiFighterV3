from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.components import MixerComponent as MixerComponentBase
from ableton.v3.control_surface.controls import EncoderControl

from ableton.v3.base import listens
from .track_macro import TrackMacroComponent
from functools import partial
import logging
logger = logging.getLogger("HK-DEBUG")


class MixerComponent(MixerComponentBase):
    filter_control = EncoderControl()
    lfo_control = EncoderControl()

    def __init__(self, *a, **k):
        self._track_macros = TrackMacroComponent()
        (super(MixerComponent, self).__init__)(*a, **k)

        self._MixerComponent__on_target_track_changed.subject = self._target_track
        self.__on_target_track_changed() if self._target_track else None

    def __getattr__(self, name):
        if name == 'set_target_track_macro_controls':
            return partial(self._track_macros.set_parameter_controls)
        else:
            return super(MixerComponent, self).__getattr__(name)

    @listens('target_track')
    def __on_target_track_changed(self):
        logger.info("Target track changed")
        flt_tracks = list(filter((lambda t: "[FLT]" in t.name), self.song.tracks))
        self._track_macros.set_track(self._target_track.target_track, flt_tracks=flt_tracks)
