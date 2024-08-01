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

def rate_limit(max_calls, period):
  def decorator(func):
      calls = 0
      last_reset = time.monotonic()

      def wrapper(*args, **kwargs):
          nonlocal calls, last_reset
          elapsed = time.monotonic() - last_reset
          if elapsed > period:
              calls = 0
              last_reset = time.monotonic()

          if calls >= max_calls:
              return # Do not call the original function
          calls += 1
          return func(*args, **kwargs)
      return wrapper
  return decorator

class ZoomingComponent(Component):
  scrub_encoder = EncoderControl()
  vertical_scroll_encoder = EncoderControl()
  vertical_zoom_encoder = EncoderControl()
  zoom_encoder = EncoderControl()


  play_button = ButtonControl()

  def __init__(self, *a, **k):
    super(ZoomingComponent, self).__init__(*a, **k)

  @play_button.pressed
  def play_button(self, button):
    if self.song.is_playing:
      self.song.stop_playing()
    else:
      self.song.play_selection()

  @zoom_encoder.value
  def zoom_encoder(self, value, encoder):
    nav = Live.Application.Application.View.NavDirection
    if value > 0:
      self.application.view.zoom_view(nav.right, "", False)
    else:
      self.application.view.zoom_view(nav.left, "", False)

  @vertical_zoom_encoder.value
  def vertical_zoom_encoder(self, value, encoder):
    nav = Live.Application.Application.View.NavDirection
    if value > 0:
      self.application.view.zoom_view(nav.down, "", False)
    else:
      self.application.view.zoom_view(nav.up, "", False)

  @vertical_scroll_encoder.value
  def vertical_scroll_encoder(self, value, encoder):
    nav = Live.Application.Application.View.NavDirection
    if value > 0:
      self.application.view.scroll_view(nav.down, "", True)
    else:
      self.application.view.scroll_view(nav.up, "", True)

  @scrub_encoder.value
  def scrub_encoder(self, value, encoder):
    if value > 0:
      self.song.scrub_by(1)
    else:
      self.song.scrub_by(-1)
