from ableton.v3.control_surface import MIDI_CC_TYPE, ElementsBase, MapMode
from functools import partial
import Live

class Elements(ElementsBase):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)

        # Bank 1 (Track/Transport)
        self.add_encoder(0, "send_a_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(1, "send_b_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(2, "send_c_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(3, "send_d_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)

        self.add_encoder(4,  "aux_encoder_1", channel=0, msg_type=MIDI_CC_TYPE, map_mode=MapMode.Absolute)
        self.add_encoder(5,  "aux_encoder_2", channel=0, msg_type=MIDI_CC_TYPE, map_mode=MapMode.LinearBinaryOffset)
        self.add_encoder(6,  "aux_encoder_3", channel=0, msg_type=MIDI_CC_TYPE, map_mode=MapMode.LinearBinaryOffset)
        self.add_encoder(7,  "aux_encoder_4", channel=0, msg_type=MIDI_CC_TYPE, map_mode=MapMode.Absolute)

        self.add_button(4,  "aux_button_1", channel=1, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_button(5,  "aux_button_2", channel=1, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_button(6,  "aux_button_3", channel=1, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_button(7,  "aux_button_4", channel=1, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)

        self.add_encoder(12, "nav_encoder_1", channel=0, msg_type=MIDI_CC_TYPE, map_mode=MapMode.LinearBinaryOffset)
        self.add_encoder(13, "nav_encoder_2", channel=0, msg_type=MIDI_CC_TYPE, map_mode=MapMode.LinearBinaryOffset)
        self.add_encoder(14, "nav_encoder_3", channel=0, msg_type=MIDI_CC_TYPE, map_mode=MapMode.LinearBinaryOffset)
        self.add_encoder(15, "nav_encoder_4", channel=0, msg_type=MIDI_CC_TYPE, map_mode=MapMode.LinearBinaryOffset)

        self.add_button(12, "nav_button_1", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(13, "nav_button_2", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(14, "nav_button_3", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(15, "nav_button_4", channel=1, msg_type=MIDI_CC_TYPE)

        # Bank 2 (Loopers)
        self.add_encoder_matrix([[16, 17, 18, 19, 8]], "looper_encoders", channels=0, is_feedback_enabled=True)
        self.add_button_matrix([[16, 17, 18, 19, 8]], "looper_buttons", channels=1)

