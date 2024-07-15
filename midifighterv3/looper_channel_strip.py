from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
from ableton.v3.base import listens

import logging
logger = logging.getLogger("HK-DEBUG")

class LooperChannelStripComponent(ChannelStripComponentBase):
    def set_track(self, track):
        super(LooperChannelStripComponent, self).set_track(track)
        self._LooperChannelStripComponent__on_volume_value_changed.subject = track

    @listens("mixer_device.volume.value")
    def __on_volume_value_changed(self):
        self.song.view.selected_track = self._track
