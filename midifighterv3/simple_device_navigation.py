# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.12.2 (main, Feb  6 2024, 20:19:44) [Clang 15.0.0 (clang-1500.1.0.2.5)]
# Embedded file name: output/Live/mac_universal_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v3/control_surface/components/simple_device_navigation.py
# Compiled at: 2024-03-11 15:53:16
# Size of source mod 2**32: 2149 bytes
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v3.live import liveobj_changed, liveobj_valid
from ableton.v3.control_surface.components import Scrollable, ScrollComponent
from ableton.v3.control_surface.display import Renderable
from ableton.v3.control_surface.controls import ButtonControl
from ableton.v3.control_surface import find_instrument_devices

from typing import cast
import Live
import logging

logger = logging.getLogger("HK-DEBUG")
NavDirection = Live.Application.Application.View.NavDirection

class SimpleDeviceNavigationComponent(ScrollComponent, Renderable, Scrollable):
    def __init__(self, name='Device_Navigation', *a, **k):
        (super().__init__)(a, name=name, scroll_skin_name="Device.Navigation", **k)
        self._previously_appointed_device = None

    def can_scroll_up(self):
        return True

    def can_scroll_down(self):
        return True

    def scroll_up(self):
        self._scroll_device_chain(NavDirection.left)

    def scroll_down(self):
        self._scroll_device_chain(NavDirection.right)

    def _scroll_device_chain(self, direction):
        view = self.application.view
        if view.is_view_visible("Detail"):
            if not view.is_view_visible("Detail/DeviceChain"):
                view.show_view("Detail")
                view.show_view("Detail/DeviceChain")
            view.scroll_view(direction, "Detail/DeviceChain", False)
        else:
            view.scroll_view(direction, "Detail/DeviceChain", False)
        self._tasks.add(self._notify_device_selection)

    def _notify_device_selection(self, _):
        device = self.song.appointed_device
        if liveobj_valid(device):
            if liveobj_changed(device, self._previously_appointed_device):
                self._previously_appointed_device = device
                self.notify(self.notifications.Device.select, cast(str, device.name))
