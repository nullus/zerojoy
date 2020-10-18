#!/usr/bin/env python3

from datetime import datetime
from logging import getLogger, basicConfig, INFO
from random import randrange, choice
from time import sleep

from hid import HidDevice, hid

NULL = chr(0x0)

SWEARS = [
    "cunt",
    "fuck",
    "bastard",
    "arsehole",
    "turd",
    "fucker",
    "prick",
    "shit",
    "potato",
    "balls",
    "cock",
    "pussy",
    "wanker",
    "dick",
]

ASCII_TO_HID = {
    'a': chr(0x4),
    'b': chr(0x5),
    'c': chr(0x6),
    'd': chr(0x7),
    'e': chr(0x8),
    'f': chr(0x9),
    'h': chr(0xb),
    'i': chr(0xc),
    'k': chr(0xe),
    'l': chr(0xf),
    'n': chr(0x11),
    'o': chr(0x12),
    'p': chr(0x13),
    'r': chr(0x15),
    's': chr(0x16),
    't': chr(0x17),
    'u': chr(0x18),
    'w': chr(0x1a),
    'y': chr(0x1c),
    ' ': chr(0x2c),
}


def ascii_to_hid(x):
    return ASCII_TO_HID[x]


class HidKeyboard(HidDevice):
    def press_key(self, key, modifier=NULL) -> None:
        self.device.write((modifier + NULL + key + NULL * 5).encode())
        self.device.write((NULL * 8).encode())
        self.device.flush()


def main():
    log = getLogger(__name__)
    basicConfig(level=INFO)
    with hid("/dev/hidg0", HidKeyboard) as device:
        while True:
            sleep(randrange(3, 7))
            start_t = datetime.now()
            swear = choice(SWEARS)
            device.press_key(chr(0x25), chr(32))
            for h in map(ascii_to_hid, swear):
                device.press_key(h)
            device.press_key(chr(0x25), chr(32))
            end_t = datetime.now()
            log.info("Said %s, took %sms, %d reports", swear, (end_t - start_t).microseconds,
                     2 * (len(swear) + 2))


if __name__ == "__main__":
    main()
