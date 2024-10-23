import importlib
import logging
import os
import traceback
import Live
import time

from ableton.v2.base import listens, find_if, task
from ableton.v3.control_surface import (
    ControlSurface,
    ControlSurfaceSpecification,
    create_skin,
)
from ableton.v3.control_surface.components import SessionNavigationComponent, SessionRingComponent, SessionComponent

from . import midifighterv3
from ableton.v3.live import liveobj_valid
from functools import partial

logger = logging.getLogger("HK-DEBUG")


def create_mappings(control_surface):
    mappings = {}
    mappings["Mixer"] = dict(
        target_track_send_a_control="send_a_encoder",
        target_track_send_b_control="send_b_encoder",
        target_track_send_c_control="send_c_encoder",
        target_track_send_d_control="send_d_encoder",
        target_track_pan_control="aux_encoder_4",
        # volume_controls="looper_encoders",
        # reset_channel_buttons="looper_buttons",
    )
    mappings["Transport"] = dict(
        tempo_coarse_encoder="aux_encoder_1",
        loop_start_encoder="aux_encoder_2",
        loop_button="aux_button_2",
        loop_length_encoder="aux_encoder_3",
        punch_in_button="aux_button_3",
        punch_out_button="aux_button_3",
    )
    mappings["Zooming"] = dict(
        vertical_zoom_push_button="nav_button_1",
        vertical_zoom_encoder="nav_encoder_1",
        track_encoder_push_button="nav_button_3",
        track_encoder="nav_encoder_3",
        scrub_encoder_push_button="streamdeck_encoder_4_button",
        scrub_encoder="streamdeck_encoder_4",
    )
    mappings["Device_Navigation"] = dict(
        scroll_encoder="nav_encoder_2",
    )
    mappings["View_Control"] = dict(
    )
    return mappings

class Specification(ControlSurfaceSpecification):
    elements_type = midifighterv3.Elements
    control_surface_skin = create_skin(skin=midifighterv3.Skin)
    session_ring_component_type = midifighterv3.LooperSessionRingComponent
    create_mappings_function = create_mappings
    component_map = {
        'TrackNavigation': midifighterv3.TrackNavigationComponent,
        'Mixer': partial(midifighterv3.MixerComponent, channel_strip_component_type=midifighterv3.LooperChannelStripComponent),
        'Device_Navigation': midifighterv3.DeviceNavigationComponent,
        'ViewCycle': midifighterv3.ViewCycleComponent,
        'Zooming': midifighterv3.ZoomingComponent,
        'Transport': midifighterv3.TransportComponent,
    }

def create_instance(c_instance):
    return MidiFighterV3(Specification, c_instance=c_instance)

class MidiFighterV3(ControlSurface):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)

        self.log_level = "info"

        self.start_logging()
        self._hide_browser_task = self._tasks.add(task.sequence(task.wait(5), task.run(self._hide_browser)))
        self._MidiFighterV3__on_browser_is_shown.subject = self.application.view
        self._browser_last_shown = time.monotonic()

        self._have_set_default_view = False
        self._set_default_view_task = self._tasks.add(task.run(self._set_default_view))

        self.show_message("midifighterv3: init mate")
        logger.info("midifighterv3: init started ...")

    def setup(self):
        super().setup()
        self.init()

    def _set_default_view(self):
        if self._have_set_default_view:
            return
        if not self.application.view.is_view_visible("Session") and not self.application.view.is_view_visible("Arranger"):
            logger.info("Application is invisble still, trying again later")
            self.schedule_message(5, self._set_default_view_task.restart)
            return
        self.application.view.hide_view("Detail/Clip")
        self.application.view.hide_view("Detail/DeviceChain")
        self.application.view.hide_view("Detail")
        self.application.view.hide_view("Browser")
        self.application.view.show_view("Detail/DeviceChain")
        self.song.arrangement_overdub = False
        self.song.overdub = False
        self.song.session_record = False
        self._have_set_default_view = True
        logger.info("Default view set")

    @listens("is_view_visible", "Browser")
    def __on_browser_is_shown(self):
        self._browser_last_shown = time.monotonic()

    def _hide_browser(self):
        if time.monotonic() - self._browser_last_shown > 15:
            self.application.view.hide_view("Browser")
        self.schedule_message(5, self._hide_browser_task.restart)

    def init(self):
        logger.info("init started:")
        with self.component_guard():
            logger.info("   adding skin")
            self._skin = create_skin(skin=midifighterv3.Skin, colors=midifighterv3.Rgb)

            logger.info("   adding listeners")
            self._MidiFighterV3__on_selected_track_changed.subject = self.song.view
            logger.info("   adding listeners done")

    def start_logging(self):
        """
        Start logging to a local logfile (logs/abletonosc.log),
        and relay error messages via OSC.
        """
        module_path = os.path.dirname(os.path.realpath(__file__))
        log_dir = os.path.join(module_path, "logs")
        if not os.path.exists(log_dir):
            os.mkdir(log_dir, 0o755)
        log_path = os.path.join(log_dir, "midifighterv3.log")
        self.log_file_handler = logging.FileHandler(log_path)
        self.log_file_handler.setLevel(self.log_level.upper())
        formatter = logging.Formatter("(%(asctime)s) [%(levelname)s] %(message)s")
        self.log_file_handler.setFormatter(formatter)
        logger.addHandler(self.log_file_handler)

    def stop_logging(self):
        logger.removeHandler(self.log_file_handler)

    def disconnect(self):
        self.show_message("Disconnecting...")
        logger.info("Disconnecting...")
        self.stop_logging()
        super().disconnect()

    @listens("selected_track")
    def __on_selected_track_changed(self):
        return
        # logger.info(f"selected track changed: {self.song.view.selected_track.name}")

