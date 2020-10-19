from datetime import datetime
from functools import reduce
from itertools import zip_longest, chain
from logging import getLogger, basicConfig, INFO
from typing import List, Optional

from zerojoy.collections import Empty


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


class HidReport:

    def __init__(self, report_data: bytearray, use_report_id: bool = False) -> None:
        super().__init__()
        if use_report_id:
            self._report_id = report_data[0]
            self._data = report_data[1:]
        else:
            self._report_id = None
            self._data = report_data.copy()
        self._created_at = datetime.utcnow()

    @property
    def report_id(self) -> Optional[int]:
        return self._report_id

    def differing_bytes_indexes(self, other: 'HidReport') -> List[int]:
        """
        Ordered list of indexes where values of report data differ
        """
        if self._report_id != other._report_id:
            raise ValueError(f"reports should have matching IDs ({self._report_id} != {other._report_id})")
        return [n for n, (a, b) in enumerate(zip_longest(self._data, other._data, fillvalue=0)) if a != b]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(...) <report_id = {self.report_id}, data = {len(self._data)} bytes, " \
               f"created_at = {self._created_at.isoformat(timespec='microseconds')}> "

    def __str__(self) -> str:
        width = 16

        def row(addr):
            return " ".join(f"{i:02x}" for i in self._data[addr:addr + width])

        return "".join([
            "       ",
        ] + [
            f"{col:02x} " for col in range(0, width)
        ] + [
            "\n",
        ] + [
            f"{addr:04x} | {row(addr)}\n" for addr in range(0, len(self._data), width)
        ])


def log_hidraw_reports():
    """
    Read reports input/feature from HIDRAW device and output to console
    """
    reports = []

    with open("/dev/hidraw0", "rb+", buffering=0) as device:
        try:
            while True:
                report_data = bytearray(device.read(1024))
                report = HidReport(report_data, True)
                log.info("received report: %s", repr(report))
                if report.report_id == 0x80:
                    reports.append(report)
        except KeyboardInterrupt:
            log.info("keyboard interrupt, exiting")

    reports_diff = [reports[i].differing_bytes_indexes(reports[i + 1]) for i in range(0, len(reports) - 1)]

    report_ranges = reduce(lambda x, y: x.insert(y), chain(*reports_diff), Empty())

    with open("hidraw.log", "w") as log_file:
        for report in reports:
            log_file.write(str(report))
            log_file.write("\n")


if __name__ == '__main__':
    log = getLogger(__name__)
    basicConfig(level=INFO)
    log_hidraw_reports()
