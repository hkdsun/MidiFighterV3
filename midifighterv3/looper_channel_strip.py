from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
from ableton.v3.control_surface.controls import PlayableControl
from ableton.v3.base import listens, listens_group
from ableton.v3.base import task


import logging
logger = logging.getLogger("HK-DEBUG")
CHANNEL_FADEOUT_DURATION = 2

class LooperChannelStripComponent(ChannelStripComponentBase):
    reset_channel_button = PlayableControl(mode=PlayableControl.Mode.playable_and_listenable)

    def __init__(self, *a, **k):
        super(LooperChannelStripComponent, self).__init__(*a, **k)
        self.set_reset_channel_button = self.reset_channel_button.set_control_element

    def set_track(self, track):
        super(LooperChannelStripComponent, self).set_track(track)
        self._LooperChannelStripComponent__on_volume_value_changed.subject = track
        device = self.macro_device()
        if device:
            self._LooperChannelStripComponent__on_fx_values_changed.replace_subjects(device.parameters[1:])

    @listens("mixer_device.volume.value")
    def __on_volume_value_changed(self):
        if self._track.name == "Master" or self._track.name == "Main":
            return
        if not self._track.is_visible:
            self._track.group_track.fold_state = False
        self.song.view.selected_track = self._track

    @listens_group("value")
    def __on_fx_values_changed(self, param):
        # Parameters starting with "Macro " are the unassigned knobs in the macro device
        if not param.name.startswith("Macro ") and param.value != param.default_value:
            self.reset_channel_button.color = 79

    def reset_param(self, param, reset_value=None):
        if reset_value is None:
            reset_value = param.default_value
        if param.state in [0, 1]: # It can be changed
            param.value = reset_value

    def set_volume(self, value):
        self._track.mixer_device.volume.value = value

    def macro_device(self):
        if self._track is None:
            return None

        for device in self._track.devices:
            if device.name == "Macro Filter+EQ":
                return device
        return None

    def reset_channel_fx(self):
        self.reset_param(self._track.mixer_device.panning)
        for send in self._track.mixer_device.sends:
            self.reset_param(send, reset_value=0)
        device = self.macro_device()
        if device:
                for param in device.parameters[1:]: # Excludes the first parameter (device on/off)
                    self.reset_param(param)


    @reset_channel_button.pressed
    def reset_channel(self, _):
        self.reset_channel_button.color = 0

        if self._track is None:
            return

        self.song.view.selected_track = self._track

        volume = self._track.mixer_device.volume
        fadeout_duration = CHANNEL_FADEOUT_DURATION * (volume.value - volume.min)
        fadeout_task = None
        if fadeout_duration > 0:
            fadeout_task = task.linear(self.set_volume, self._track.mixer_device.volume.value, 0, duration=fadeout_duration)
        else:
            fadeout_task = task.run(self.set_volume, 0)

        self._tasks.add(task.sequence(fadeout_task, task.run(self.reset_channel_fx)))
