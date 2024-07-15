from ableton.v3.control_surface import MIDI_CC_TYPE, ElementsBase, MapMode
from functools import partial

class Elements(ElementsBase):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.add_button(3, "View_Cycle_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(6, "Play_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(7, "Stop_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_encoder_matrix([[0, 1, 12, 13, 14, 15]], "Device_Controls", is_feedback_enabled=True)
        self.add_encoder(3, "track_navigation_encoder", channel=0, mapping_sensitivity=0.1, map_mode=MapMode.LinearBinaryOffset, msg_type=MIDI_CC_TYPE,  is_feedback_enabled=True)
        self.add_encoder(4, "send_a_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(5, "send_b_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(6, "send_c_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(7, "send_d_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder_matrix([[8, 9, 10, 11, 2]], "looper_volume_controls", is_feedback_enabled=True)
