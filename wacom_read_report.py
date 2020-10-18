from itertools import zip_longest
from logging import getLogger, basicConfig


def pretty_print_hex(bytearray_):
    width = 32
    print("      ", " ".join(f"{col:02x}" for col in range(0, width)))

    for line in range(0, len(bytearray_), width):
        b = bytearray_[line:line + width]
        print(f"{line:04x} | ", end="")
        if b:
            print(" ".join(f"{i:02x}" for i in b))


class SequenceDiff(object):

    def __init__(self) -> None:
        super().__init__()
        self._previous = []

    def difference(self, seq):
        r = [n for n, (a, b) in enumerate(zip_longest(self._previous, seq, fillvalue=0)) if a ^ b]
        self._previous = seq
        return r


def output_hidraw_reports():
    """
    Read reports input/feature from HIDRAW device and output to console
    """

    d = SequenceDiff()

    with open("/dev/hidraw0", "rb+", buffering=0) as device:
        while True:
            report_data = device.read(1024)
            report_id = report_data[0]
            log.info("Report ID: %d, data length: %d", report_id, len(report_data) - 1)
            # pretty_print_hex(report_data[1:])
            print(d.difference(report_data[1:]))


if __name__ == '__main__':
    log = getLogger(__name__)
    basicConfig()
    output_hidraw_reports()
