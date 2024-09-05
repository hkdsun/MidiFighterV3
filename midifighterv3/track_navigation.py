# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.12.2 (main, Feb  6 2024, 20:19:44) [Clang 15.0.0 (clang-1500.1.0.2.5)]
# Embedded file name: output/Live/mac_universal_64_static/Release/python-bundle/MIDI Remote Scripts/FANTOM/mixer.py
# Compiled at: 2024-03-09 01:30:22
# Size of source mod 2**32: 2494 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.components import Scrollable, ScrollComponent
from ableton.v3.control_surface.controls import InputControl
from ableton.v3.live import liveobj_valid
import Live
NavDirection = Live.Application.Application.View.NavDirection

class TrackNavigationComponent(ScrollComponent, Scrollable):
    def can_scroll_up(self):
        return self.song.view.selected_track != self.song.tracks[0]

    def can_scroll_down(self):
        return self.song.view.selected_track != self.song.master_track

    def all_tracks(self):
        return self.tracks_to_use() + (self.song.master_track,)

    def tracks_to_use(self):
        return tuple(self.song.visible_tracks) + tuple(self.song.return_tracks)

    def manage_instruments_fold_state(self, track, fold_state):
        if liveobj_valid(track) and track.name == 'Instruments' and track.is_foldable:
            track.fold_state = fold_state

    def reset_view(self):
        self.application.view.hide_view('Browser')
        self.application.view.show_view('Detail/DeviceChain')

    def scroll_up(self):
        selected_track = self.song.view.selected_track
        all_tracks = self.all_tracks()
        index = list(all_tracks).index(selected_track)
        new_track = all_tracks[index - 1]
        self.song.view.selected_track = new_track
        # self.reset_view()
        # self.manage_instruments_fold_state(new_track, 1)

    def scroll_down(self):
        selected_track = self.song.view.selected_track
        all_tracks = self.all_tracks()
        index = list(all_tracks).index(selected_track)
        new_track = all_tracks[index + 1]
        self.song.view.selected_track = new_track
        # self.reset_view()
        # self.manage_instruments_fold_state(new_track, 0)
