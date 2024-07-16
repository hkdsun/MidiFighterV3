# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.12.2 (main, Feb  6 2024, 20:19:44) [Clang 15.0.0 (clang-1500.1.0.2.5)]
# Embedded file name: output/Live/mac_universal_64_static/Release/python-bundle/MIDI Remote Scripts/VCM600/TrackFilterComponent.py
# Compiled at: 2024-03-09 01:30:22
# Size of source mod 2**32: 3926 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range

from ableton.v3.live.util import get_parameter_by_name
from ableton.v3.control_surface import Component

import Live
import logging
logger = logging.getLogger("HK-DEBUG")

class TrackMacroComponent(Component):
    def __init__(self):
        Component.__init__(self)
        self._track = None
        self._device = None
        self._parameter_controls = None

        self._filter_tracks = None

    def disconnect(self):
        if self._parameter_controls != None:
            self._parameter_controls.reset()
            self._parameter_controls = None
        if self._track != None:
            self._track.remove_devices_listener(self._on_devices_changed)
            self._track = None
        self._device = None

    def on_enabled_changed(self):
        self.update()

    def set_track(self, track, flt_tracks=None):
        self._filter_tracks = flt_tracks
        if self._track != None:
            self._track.remove_devices_listener(self._on_devices_changed)
            if self._device != None:
                if self._parameter_controls != None:
                    self._parameter_controls.reset()
        self._track = track
        if self._track != None:
            self._track.add_devices_listener(self._on_devices_changed)
        self._on_devices_changed()

    def set_parameter_controls(self, controls):
        if self._device != None:
            if self._parameter_controls != None:
                self._parameter_controls.reset()
        self._parameter_controls = controls
        self.update()

    def reset_device_parameters(self):
        if self._parameter_controls != None:
            for control in self._parameter_controls:
                control.reset()

    def update(self):
        super(TrackMacroComponent, self).update()
        if self.is_enabled():
            if self._device != None:
                if self._parameter_controls != None:
                    self._parameter_controls.reset()
                    for control, parameter in zip(self._parameter_controls, self._device.parameters[1:]):
                        control.connect_to(parameter)

    def _on_devices_changed(self):
        self._device = None
        if self._track != None:
            for index in range(len(self._track.devices)):
                device = self._track.devices[-1 * (index + 1)]
                if device.name == "Macro Filter+EQ":
                    self._device = device
                    break
        self.update()
