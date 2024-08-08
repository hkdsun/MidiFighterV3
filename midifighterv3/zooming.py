from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from itertools import chain, islice, repeat
from math import ceil
from ableton.v2.base import compose, find_if, listens, listens_group, liveobj_valid, task
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import EncoderControl, ButtonControl
import Live
import time

import logging
logger = logging.getLogger("HK-DEBUG")

def rate_limit(max_calls, first_period, repeat_period=None):
  if repeat_period is None:
      repeat_period = first_period

  def decorator(func):
      calls = 0
      next_reset = time.monotonic()

      def wrapper(*args, **kwargs):
          nonlocal calls, next_reset
          is_first_call = kwargs.pop('first_call', False)
          period = first_period if is_first_call else repeat_period
          logger.info("Calls: %s, Period: %s", calls, period)
          if time.monotonic() > next_reset:
              calls = 0
              next_reset = time.monotonic() + period
          if calls >= max_calls:
              return # Do not call the original function
          calls += 1
          return func(*args, **kwargs)
      return wrapper
  return decorator

class ZoomingComponent(Component):
  vertical_zoom_encoder = EncoderControl()
  vertical_zoom_push_button = ButtonControl()

  scrub_encoder = EncoderControl()
  scrub_encoder_push_button = ButtonControl()

  track_encoder = EncoderControl()
  track_encoder_push_button = ButtonControl()
  track_encoder_ignore_delay = 0.8

  def __init__(self, *a, **k):
    super(ZoomingComponent, self).__init__(*a, **k)
    self._vertical_zoom_encoder_held = False
    self._track_encoder_held = False
    self._scrub_encoder_held = False
    self.cycle_through_best_views = rate_limit(1, 0.8, repeat_period=0.2)(self._cycle_through_best_views)
    self.last_time_track_encoder_was_cycling_views = time.monotonic()

  @track_encoder_push_button.pressed
  def track_encoder_push_button(self, button):
    self._track_encoder_held = True
    self._view_cycle_first_call = True

  @track_encoder_push_button.released
  def track_encoder_push_button(self, button):
    self._track_encoder_held = False

  @track_encoder_push_button.released_immediately
  def track_encoder_push_button(self, button):
    if self.application.view.is_view_visible("Session"):
      self.application.view.focus_view("Arranger")
    else:
      self.application.view.focus_view("Session")

  @track_encoder.value
  def track_encoder(self, value, encoder):
    if self._track_encoder_held:
      self.cycle_through_best_views(value, first_call=self._view_cycle_first_call)
      self._view_cycle_first_call = False
      self._last_time_track_encoder_was_cycling_views = time.monotonic()
    else:
      if time.monotonic() - self._last_time_track_encoder_was_cycling_views > self.track_encoder_ignore_delay:
        self.scroll_tracks(value)

  def scroll_tracks(self, value):
    nav = Live.Application.Application.View.NavDirection
    if self.application.view.is_view_visible("Session"):
      if value > 0:
        self.application.view.scroll_view(nav.right, "", self._track_encoder_held)
      else:
        self.application.view.scroll_view(nav.left, "", self._track_encoder_held)
    else:
      if value > 0:
        self.application.view.scroll_view(nav.down, "", self._track_encoder_held)
      else:
        self.application.view.scroll_view(nav.up, "", self._track_encoder_held)

  @vertical_zoom_push_button.pressed
  def vertical_zoom_push_button(self, button):
    self._vertical_zoom_encoder_held = True

  @vertical_zoom_push_button.released
  def vertical_zoom_push_button(self, button):
    self._vertical_zoom_encoder_held = False

  @vertical_zoom_encoder.value
  def vertical_zoom_encoder(self, value, encoder):
    nav = Live.Application.Application.View.NavDirection
    if value > 0:
      self.application.view.zoom_view(nav.down, "", self._vertical_zoom_encoder_held)
    else:
      self.application.view.zoom_view(nav.up, "", self._vertical_zoom_encoder_held)

  @scrub_encoder_push_button.pressed
  def scrub_encoder_push_button(self, button):
    if self.application.view.is_view_visible("Session"):
        current_track = self.song.view.selected_track
        if not liveobj_valid(current_track):
            return
        if current_track.is_foldable:
            current_track.fold_state = not current_track.fold_state
        return
    else: # Arrangement
      if self.song.is_playing:
        self.song.stop_playing()
      else:
        self.song.play_selection()

  @scrub_encoder.value
  def scrub_encoder(self, value, encoder):
    if self.application.view.is_view_visible("Session"):
      nav = Live.Application.Application.View.NavDirection
      if value > 0:
        self.application.view.scroll_view(nav.right, "", self._vertical_zoom_encoder_held)
      else:
        self.application.view.scroll_view(nav.left, "", self._vertical_zoom_encoder_held)
    else: # Arrangement view
      if value > 0:
        self.song.scrub_by(1)
      else:
        self.song.scrub_by(-1)

  valid_views = [
      # clip, device, browser
      (False, True, False),
      (True, False, False),
      (False, False, False),
  ]

  def set_application_view(self, is_detail_clip_view_visible, is_detail_device_chain_view_visible, is_browser_view_visible):
    if is_detail_clip_view_visible:
      self.application.view.show_view('Detail/Clip')
    else:
      self.application.view.hide_view('Detail/Clip')

    if is_detail_device_chain_view_visible:
      self.application.view.show_view('Detail/DeviceChain')
    else:
      self.application.view.hide_view('Detail/DeviceChain')

    if not is_detail_clip_view_visible and not is_detail_device_chain_view_visible:
      self.application.view.hide_view('Detail')


    if is_browser_view_visible:
      self.application.view.show_view('Browser')
    else:
      self.application.view.hide_view('Browser')

  def _cycle_through_best_views(self, value):
    is_detail_clip_view_visible = self.application.view.is_view_visible('Detail/Clip')
    is_detail_device_chain_view_visible = self.application.view.is_view_visible('Detail/DeviceChain')
    is_browser_view_visible = self.application.view.is_view_visible('Browser')
    current_state = (is_detail_clip_view_visible, is_detail_device_chain_view_visible, is_browser_view_visible)

    if value > 0:
      value = 1
    else:
      value = -1

    if current_state in self.valid_views:
      next_state = self.valid_views.index(current_state) + value
      if next_state < len(self.valid_views) and next_state >= 0:
        self.set_application_view(*self.valid_views[next_state])
    else:
      self.set_application_view(*self.valid_views[0])
