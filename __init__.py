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
        metronome_button="metronome_button",
        # arrangement_position_encoder="encoder_7"
    )
    mappings["Recording"] = dict(
        arrangement_record_button="arrangement_record_button",
    )
    mappings["Mixer"] = dict(
        target_track_solo_button="solo_button",
        target_track_mute_button="mute_button",
        target_track_arm_button="arm_button",
        target_track_volume_control="volume_encoder",
        target_track_pan_control="pan_encoder",
        target_track_send_a_control="send_a_encoder",
        target_track_send_b_control="send_b_encoder",
        target_track_macro_controls="device_controls",
        prehear_volume_control="cue_volume_encoder",
        master_track_volume_control="master_volume_encoder",
    )
    mappings["Device"] = dict(
        device_on_off_button="device_on_off_button",
        # parameter_controls="device_controls",
    )
    mappings["TrackNavigation"] = dict(
        scroll_encoder="track_navigation_encoder",
    )
    mappings["DeviceNavigation"] = dict(
        scroll_encoder="device_navigation_encoder",
    )
    mappings["SessionNavigation"] = dict(
        page_up_button="lh_button_1",
        page_down_button="lh_button_2",
        page_left_button="rh_button_1",
        page_right_button="rh_button_2",
    )
    return mappings

class Specification(ControlSurfaceSpecification):
    elements_type = midifighterv3.Elements
    control_surface_skin = create_skin(skin=midifighterv3.Skin)
    create_mappings_function = create_mappings
    component_map = {
        'DeviceNavigation': midifighterv3.SimpleDeviceNavigationComponent,
        'TrackNavigation': midifighterv3.TrackNavigationComponent,
        'SessionNavigation': SessionNavigationComponent,
        'Mixer': midifighterv3.MixerComponent,
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
