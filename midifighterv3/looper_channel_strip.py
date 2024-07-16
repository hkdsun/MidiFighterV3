from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
from ableton.v3.control_surface.controls import ButtonControl
from ableton.v3.base import listens
from ableton.v3.base import task


import logging
logger = logging.getLogger("HK-DEBUG")
CHANNEL_FADEOUT_DURATION = 3

class LooperChannelStripComponent(ChannelStripComponentBase):
    reset_channel_button = ButtonControl()

    def set_track(self, track):
        super(LooperChannelStripComponent, self).set_track(track)
        self._LooperChannelStripComponent__on_volume_value_changed.subject = track
        self.set_reset_channel_button = self.reset_channel_button.set_control_element

    @listens("mixer_device.volume.value")
    def __on_volume_value_changed(self):
        self.song.view.selected_track = self._track

    def reset_param(self, param, reset_value=0):
        if param.state in [0, 1]: # It can be changed
            param.value = reset_value

    def reset_channel_(self, device):
        for param in device.parameters[1:]:
            self.reset_param(param)

    def set_volume(self, value):
        self._track.mixer_device.volume.value = value

    def reset_channel_fx(self):
        self.reset_param(self._track.mixer_device.panning)
        for send in self._track.mixer_device.sends:
            self.reset_param(send)
        for device in self._track.devices:
            if device.name == "Macro Filter+EQ":
                for param in device.parameters[1:]: # Excludes the first parameter (device on/off)
                    self.reset_param(param)


    @reset_channel_button.pressed
    def reset_channel(self, _):
        self._tasks.add(task.sequence(
            task.linear(self.set_volume, self._track.mixer_device.volume.value, 0, duration=CHANNEL_FADEOUT_DURATION),
            task.run(self.reset_channel_fx),
        ))
