"""
Wacom tablet as "throttle" + additional buttons for full H.O.T.A.W experience
"""
from logging import basicConfig, INFO

from zerojoy.hid import capture_hidraw_input
from zerojoy.wacom.adaptor import WacomTouchDecoder, JoystickEncoder
from zerojoy.wacom.port import TouchMapper


hid_report_desc = [
    '05 01',        # Usage Page (Generic Desktop)
    '09 05',        # Usage (Gamepad)
    'a1 01',        # Collection (Application)
    '15 00',        # Logical Minimum (0)
    '25 01',        # Logical Maximum (1)
    '35 00',        # Physical Minimum (0)
    '45 01',        # Physical Maximum (1)
    '75 01',        # Report Size (1)
    '95 04',        # Report Count (4)
    '05 09',        # Usage Page (Buttons)
    '19 01',        # Usage Minimum (1)
    '29 04',        # Usage Maximum (4)
    '81 02',        # Input (Data, Variable, Absolute)
    '95 14',        # Report Count (20)
    '81 01',        # Input (Constant, Array, Absolute)
    '05 01',        # Usage Page (Generic Desktop)
    '26 ff00',     # Logical Maximum (255)
    '46 ff00',     # Physical Maximum (255)
    '09 30',        # Usage (X)
    '09 31',        # Usage (Y)
    '09 35',        # Usage (Rz)
    '09 36',        # Usage (Slider)
    '75 08',        # Report Size (8)
    '95 04',        # Report Count (4)
    '81 02',        # Input (Data, Variable, Absolute)
    # Hacked in hat?
    '09 39',        # Usage (Hat Switch)
    '15 01',        # (GLOBAL) LOGICAL_MINIMUM    0x01 (1)
    '25 08',        # (GLOBAL) LOGICAL_MAXIMUM    0x08 (8)
    '35 00',        # (GLOBAL) PHYSICAL_MINIMUM   0x00 (0)  <-- Info: Consider replacing 35 00 with 34
    '46 3B01',      # (GLOBAL) PHYSICAL_MAXIMUM   0x013B (315)
    '66 1400',      # (GLOBAL) UNIT               0x0014 Rotation in degrees [1° units] (4=System=English Rotation, 1=Rotation=Degrees)  <-- Info: Consider replacing 66 1400 with 65 14
    '75 04',        # (GLOBAL) REPORT_SIZE        0x04 (4) Number of bits per field
    '95 01',        # (GLOBAL) REPORT_COUNT       0x01 (1) Number of fields <-- Redundant: REPORT_COUNT is already 1
    '81 42',        # (MAIN)   INPUT              0x00000042 (1 field x 4 bits) 0=Data 1=Variable 0=Absolute 0=NoWrap 0=Linear 0=PrefState 1=Null 0=NonVolatile 0=Bitmap
    '65 00',        # (GLOBAL) UNIT               0x00 No unit (0=None)  <-- Info: Consider replacing 65 00 with 64
    '81 03',        # (MAIN)   INPUT              0x00000003 (1 field x 4 bits) 1=Constant 1=Variable 0=Absolute 0=NoWrap 0=Linear 0=PrefState 0=NoNull 0=NonVolatile 0=Bitmap
    'c0',           # End Collection
]


def main():
    basicConfig(level=INFO)
    joystick_encoder = JoystickEncoder()
    touch_mapper = TouchMapper([joystick_encoder])
    wacom_decoder = WacomTouchDecoder([touch_mapper])
    capture_hidraw_input([wacom_decoder])
