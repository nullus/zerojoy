#!/usr/bin/env python3

from functools import reduce
from logging import getLogger, basicConfig, INFO
from operator import or_
from struct import Struct

from zerojoy.hid import HidDevice, hid


class HidJoystick(HidDevice):

    def __init__(self, device) -> None:
        super().__init__(device)
        self.x = 128
        self.y = 128
        self.rz = 128
        self.slider = 128
        self.button = [0, 0, 0, 0]
        self.struct = Struct("B" * 7)

    def encode(self):
        return self.struct.pack(
            reduce(or_, (b << p for p, b in enumerate(self.button))), 0, 0,
            self.x, self.y, self.rz, self.slider)


def main():
    log = getLogger(__name__)
    basicConfig(level=INFO)
    with hid("/dev/hidg0", HidJoystick) as device:
        while True:
            command = input("> ")
            for button in [0, 1, 2, 3]:
                if str(button + 1) in command:
                    device.button[button] = int(not device.button[button])
            if "l" in command:
                device.x = 0
            if "r" in command:
                device.x = 255
            if "u" in command:
                device.y = 0
            if "d" in command:
                device.y = 255
            if "c" in command:
                device.x = 128
                device.y = 128
            if "h" in command:
                device.slider = 128
            if "f" in command:
                device.slider = 255
            if "z" in command:
                device.slider = 0
            device.send_report()


if __name__ == "__main__":
    main()
