from ableton.v3.control_surface import MIDI_CC_TYPE, ElementsBase, MapMode
from functools import partial

class Elements(ElementsBase):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.add_button(0, "Mute_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(1, "Solo_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(2, "Arm_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(3, "Device_On_Off_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(4, "Play_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(5, "Stop_Button", channel=1, msg_type=MIDI_CC_TYPE)

        self.add_encoder(0, "volume_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(1, "pan_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(2, "track_navigation_encoder", channel=0, map_mode=MapMode.LinearBinaryOffset, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(3, "device_navigation_encoder", channel=0, map_mode=MapMode.LinearBinaryOffset, msg_type=MIDI_CC_TYPE,  is_feedback_enabled=True)
        self.add_encoder(4, "send_a_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(5, "send_b_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(6, "encoder_7", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(7, "encoder_8", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)

        self.add_encoder_matrix([[i + 8 for i in range(8)]], "Device_Controls", is_feedback_enabled=True)

