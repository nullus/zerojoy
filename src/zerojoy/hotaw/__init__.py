"""
Wacom tablet as "throttle" + additional buttons for full H.O.T.A.W experience
"""
from logging import basicConfig, INFO

from zerojoy.hid import capture_hidraw_input
from zerojoy.wacom.adaptor import WacomTouchDecoder, JoystickEncoder
from zerojoy.wacom.port import TouchMapper


def main():
    basicConfig(level=INFO)
    joystick_encoder = JoystickEncoder()
    touch_mapper = TouchMapper([joystick_encoder])
    wacom_decoder = WacomTouchDecoder([touch_mapper])
    capture_hidraw_input([wacom_decoder])
