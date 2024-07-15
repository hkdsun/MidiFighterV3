import importlib
import logging
import os
import traceback
import Live

from ableton.v2.base import listens, find_if
from ableton.v3.control_surface import (
    ControlSurface,
    ControlSurfaceSpecification,
    create_skin,
)
from ableton.v3.control_surface.components import SessionNavigationComponent, SessionRingComponent, SessionComponent

from . import midifighterv3
from ableton.v3.live import liveobj_valid


logger = logging.getLogger("HK-DEBUG")


def create_mappings(control_surface):
    mappings = {}
    mappings["Transport"] = dict(
        play_toggle_button="play_button",
        stop_button="stop_button",
    )
    mappings["Mixer"] = dict(
        target_track_send_a_control="send_a_encoder",
        target_track_send_b_control="send_b_encoder",
        target_track_send_c_control="send_c_encoder",
        target_track_send_d_control="send_d_encoder",
        target_track_macro_controls="device_controls",
    )
    mappings["Mixer"] = dict(
        volume_controls="looper_volume_controls",
    )
    mappings["TrackNavigation"] = dict(
        scroll_encoder="track_navigation_encoder",
    )
    mappings["ViewCycle"] = dict(
        view_cycle_button="view_cycle_button",
    )
    return mappings

class Specification(ControlSurfaceSpecification):
    elements_type = midifighterv3.Elements
    control_surface_skin = create_skin(skin=midifighterv3.Skin)
    create_mappings_function = create_mappings
    component_map = {
        'DeviceNavigation': midifighterv3.SimpleDeviceNavigationComponent,
        'TrackNavigation': midifighterv3.TrackNavigationComponent,
        'Mixer': midifighterv3.MixerComponent,
        'ViewCycle': midifighterv3.ViewCycleComponent,
    }

def create_instance(c_instance):
    return MidiFighterV3(Specification, c_instance=c_instance)

class MidiFighterV3(ControlSurface):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)

        self.log_level = "info"

        self.start_logging()

        self.show_message("midifighterv3: init mate")
        logger.info("midifighterv3: init started ...")

    def setup(self):
        super().setup()
        self.init()

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
        logger.info(f"selected track changed: {self.song.view.selected_track.name}")
