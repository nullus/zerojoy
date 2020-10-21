"""
Wacom tablet as "throttle" + additional buttons for full H.O.T.A.W experience
"""
from logging import basicConfig, INFO

from zerojoy.hid import capture_hidraw_input
from zerojoy.wacom.adaptor import WacomTouchDecoder
from zerojoy.wacom.port import TouchMapper


def main():
    basicConfig(level=INFO)
    wacom_decoder = WacomTouchDecoder([TouchMapper()])
    capture_hidraw_input([wacom_decoder])
