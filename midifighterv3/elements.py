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
        self.add_button(0, "Instrument_Button", channel=1, msg_type=MIDI_CC_TYPE)
        # self.add_button(1, "", channel=1, msg_type=MIDI_CC_TYPE)
        # self.add_button(2, "Device_On_Off_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(3, "View_Cycle_Button", channel=1, msg_type=MIDI_CC_TYPE)
        # self.add_button(4, "Looper_Trigger", channel=1, msg_type=MIDI_CC_TYPE)
        # self.add_button(5, "Looper_Clear", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(6, "Play_Button", channel=1, msg_type=MIDI_CC_TYPE)
        self.add_button(7, "Stop_Button", channel=1, msg_type=MIDI_CC_TYPE)

        # Encoder Matrix (for device controls)
        self.add_encoder_matrix([[0, 1, 4, 5, 12, 13, 14, 15]], "Device_Controls", is_feedback_enabled=True)

        # Encoder Rotaries
        self.add_encoder(3, "track_navigation_encoder", channel=0, mapping_sensitivity=0.1, map_mode=MapMode.LinearBinaryOffset, msg_type=MIDI_CC_TYPE,  is_feedback_enabled=True)
        self.add_encoder(6, "send_a_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)
        self.add_encoder(7, "send_b_encoder", channel=0, msg_type=MIDI_CC_TYPE, is_feedback_enabled=True)

