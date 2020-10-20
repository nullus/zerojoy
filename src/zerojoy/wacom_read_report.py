from datetime import datetime
from functools import reduce
from itertools import zip_longest, chain
from logging import getLogger, basicConfig, INFO
from typing import List, Optional

from zerojoy.collections import Empty


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
        return self.hex_string()

    @staticmethod
    def hex_header() -> str:
        width = 16

        return "".join(["       "] + [f"{col:02x} " for col in range(0, width)] + ["\n"])

    def hex_string(self, start=0, end=None):
        width = 16

        def row(addr):
            return " ".join(f"{i:02x}" for i in self._data[addr:min(addr + width, end or len(self._data))])

        return "".join([f"{addr:04x} | {row(addr)}\n" for addr in range(start, end or len(self._data), width)])


def log_hidraw_reports():
    """
    Read reports input/feature from HIDRAW device and output to console
    """
    reports: List[HidReport] = []

    log = getLogger(__name__)
    basicConfig(level=INFO)

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

    report_ranges = reduce(lambda x, y: x.insert(y), chain(*reports_diff), Empty()).ranges()

    with open("hidraw.log", "w") as log_file:
        log_file.write(repr(reports[0]))
        log_file.write("\n")
        log_file.write(reports[0].hex_header())
        log_file.write(reports[0].hex_string())
        log_file.write("\n")
        for report in reports[1:]:
            log_file.write(repr(report))
            log_file.write("\n")
            log_file.write(report.hex_header())
            for range_ in report_ranges:
                log_file.write(report.hex_string(*range_))
            log_file.write("\n")


if __name__ == '__main__':
    log_hidraw_reports()
