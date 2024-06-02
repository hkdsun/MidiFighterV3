from ableton.v3.control_surface import MIDI_CC_TYPE, ElementsBase, MapMode
from functools import partial

class Elements(ElementsBase):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.add_button(16, "Mute_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(17, "Solo_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(18, "Arm_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(19, "Device_On_Off_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(20, "Play_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(21, "Stop_Button", channel=1, msg_type=MIDI_CC_TYPE)

        self.add_encoder(16, "volume_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(17, "pan_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(18, "track_navigation_encoder", channel=0, map_mode=MapMode.LinearBinaryOffset, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(19, "device_navigation_encoder", channel=0, map_mode=MapMode.LinearBinaryOffset, msg_type=MIDI_CC_TYPE,  is_feedback_enabled=True)
        self.add_encoder(20, "send_a_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(21, "send_b_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(22, "encoder_7", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(23, "encoder_8", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)

        self.add_encoder_matrix([[i + 24 for i in range(8)]], "Device_Controls", is_feedback_enabled=True)

