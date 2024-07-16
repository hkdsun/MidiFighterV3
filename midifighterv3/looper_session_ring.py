from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.control_surface.components import SessionRingComponent as SessionRingComponentBase

def looper_tracks_to_use(song):
    looper_tracks = []
    for track in song.tracks:
        if track.name.startswith("Loop "):
            looper_tracks.append(track)

    for track in song.tracks:
        if track.name == "Vocals In":
            looper_tracks.append(track)

    if len(looper_tracks) == 0:
        return song.visible_tracks
    return looper_tracks

class LooperSessionRingComponent(SessionRingComponentBase):
    def __init__(self, *a, **k):
        tracks_to_use = lambda: looper_tracks_to_use(self.song)
        super(LooperSessionRingComponent, self).__init__(*a, tracks_to_use=tracks_to_use, **k)
