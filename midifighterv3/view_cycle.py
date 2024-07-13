# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.12.2 (main, Feb  6 2024, 20:19:44) [Clang 15.0.0 (clang-1500.1.0.2.5)]
# Embedded file name: output/Live/mac_universal_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/simple_device_navigation.py
# Compiled at: 2024-03-11 15:53:16
# Size of source mod 2**32: 2149 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.live import liveobj_changed, liveobj_valid
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import ButtonControl
import Live
import logging
import time

logger = logging.getLogger("HK-DEBUG")

class ViewCycleComponent(Component):
    view_cycle_button = ButtonControl()

    valid_views = [
        # clip, device, browser
        (False, False, False),
        # (True, False, False),
        (False, True, False),
        # (False, False, True),
    ]

    def __init__(self, *a, **k):
        (super().__init__)(a, **k)
        self.view_state = -1
        self.last_time_cycle_pressed = time.time()

    def update_view_state(self, view):
        # if it's been more than 1 minute since the last time the cycle button was pressed, update the view state
        if time.time() - self.last_time_cycle_pressed > 60:
            self.view_state = -1
            return

        is_detail_clip_view_visible = view.is_view_visible('Detail/Clip')
        is_detail_device_chain_view_visible = view.is_view_visible('Detail/DeviceChain')
        is_browser_view_visible = view.is_view_visible('Browser')
        current_state = (is_detail_clip_view_visible, is_detail_device_chain_view_visible, is_browser_view_visible)
        if current_state in self.valid_views:
            self.view_state = self.valid_views.index(current_state)
        else:
            self.view_state = -1

    def fold_songs(self, song):
        for track in song.tracks:
            if track.is_foldable:
                track.fold_state = 1

    @view_cycle_button.pressed
    def cycle_view(self, _button):
        self.update_view_state(self.application.view)
        new_state = self.view_state + 1
        if new_state >= len(self.valid_views):
            new_state = 0

        desired_state = self.valid_views[new_state]
        if desired_state[0]:
            self.application.view.show_view('Detail/Clip')
        else:
            self.application.view.hide_view('Detail/Clip')

        if desired_state[1]:
            self.application.view.show_view('Detail/DeviceChain')
        else:
            self.application.view.hide_view('Detail/DeviceChain')

        if not desired_state[0] and not desired_state[1]:
            self.application.view.hide_view('Detail')

        if desired_state[2]:
            self.application.view.show_view('Browser')
        else:
            self.application.view.hide_view('Browser')

        if new_state == 0:
            self.fold_songs(self.song)

        self.last_time_cycle_pressed = time.time()

