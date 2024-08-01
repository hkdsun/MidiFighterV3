from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from itertools import chain, islice, repeat
from math import ceil
from ableton.v2.base import compose, find_if, listens, listens_group, liveobj_valid, task
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import EncoderControl
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
  zoom_encoder = EncoderControl()
  scroll_encoder = EncoderControl()

  def __init__(self, *a, **k):
    super(ZoomingComponent, self).__init__(*a, **k)
    self.zoom_handler = rate_limit(1, 0.1)(self.zoom_view)
    # self.scroll_handler = rate_limit(1, 0.1)(self.scroll_view)

  @zoom_encoder.value
  def zoom_encoder(self, value, encoder):
    self.zoom_handler(value)

  def zoom_view(self, value):
    nav = Live.Application.Application.View.NavDirection
    if value > 0:
      self.application.view.zoom_view(nav.right, "", False)
    else:
      self.application.view.zoom_view(nav.left, "", False)

  @scroll_encoder.value
  def scroll_encoder(self, value, encoder):
    nav = Live.Application.Application.View.NavDirection
    if value > 0:
      self.application.view.scroll_view(nav.right, "", False)
    else:
      self.application.view.scroll_view(nav.left, "", False)
