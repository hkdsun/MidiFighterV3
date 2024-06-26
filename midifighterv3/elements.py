from ableton.v3.control_surface import MIDI_CC_TYPE, ElementsBase, MapMode
from functools import partial

class Elements(ElementsBase):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)

        # Side buttons
        self.add_button(8, "lh_button_1", channel=3, msg_type=MIDI_CC_TYPE)
        self.add_button(10, "lh_button_2", channel=3, msg_type=MIDI_CC_TYPE)
        self.add_button(11, "rh_button_1", channel=3, msg_type=MIDI_CC_TYPE)
        self.add_button(13, "rh_button_2", channel=3, msg_type=MIDI_CC_TYPE)

        # Encoder Switches
        self.add_button(0, "Mute_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(1, "Solo_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(2, "Device_On_Off_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(3, "Arm_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(4, "Play_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(5, "Stop_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(6, "Metronome_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(7, "Arrangement_Record_button", channel=1, msg_type=MIDI_CC_TYPE)

        # Encoder Rotaries
        self.add_encoder(0, "volume_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(1, "pan_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(2, "device_navigation_encoder", channel=0, map_mode=MapMode.LinearBinaryOffset, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(3, "track_navigation_encoder", channel=0, map_mode=MapMode.LinearBinaryOffset, msg_type=MIDI_CC_TYPE,  is_feedback_enabled=True)
        self.add_encoder(4, "send_a_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(5, "send_b_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(6, "cue_volume_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(7, "master_volume_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)

        # Encoder Matrix (for device controls)
        self.add_encoder_matrix([[i + 8 for i in range(8)]], "Device_Controls", is_feedback_enabled=True)

