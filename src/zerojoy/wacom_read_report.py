from abc import abstractmethod, ABC
from datetime import datetime
from functools import reduce
from itertools import zip_longest, chain
from logging import getLogger, basicConfig, INFO
from struct import Struct
from typing import List, Optional

from zerojoy.collections import Empty


class HidReport:

    def __init__(self, report_data: bytearray, use_report_id: bool = False) -> None:
        super().__init__()
        if use_report_id:
            self._report_id = report_data[0]
            self.data = report_data[1:]
        else:
            self._report_id = None
            self.data = report_data.copy()
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
        return [n for n, (a, b) in enumerate(zip_longest(self.data, other.data, fillvalue=0)) if a != b]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(...) <report_id = {self.report_id}, data = {len(self.data)} bytes, " \
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
            return " ".join(f"{i:02x}" for i in self.data[addr:min(addr + width, end or len(self.data))])

        return "".join([f"{addr:04x} | {row(addr)}\n" for addr in range(start, end or len(self.data), width)])


class HidDecoder(ABC):
    @abstractmethod
    def process(self, report: HidReport):
        pass


class WacomTouchDecoder(HidDecoder):
    TOUCH_OFFSET = 0x6c
    TOUCH_RECORD_SIZE = 43

    def __init__(self):
        super().__init__()
        self.log = getLogger(__name__)

        self.record_format = Struct("<B" + "2B3H" * 5 + "H")

    def process(self, report: HidReport):
        if report.report_id == 0x80:
            self._parse_records(report.data[self.TOUCH_OFFSET:])
        else:
            self.log.warning("unrecognised report ID: %d", report.report_id)

    def _parse_records(self, records: bytearray):
        for offset in range(0, 3 * self.TOUCH_RECORD_SIZE, self.TOUCH_RECORD_SIZE):
            record = self.record_format.unpack(records[offset:offset + self.TOUCH_RECORD_SIZE])
            if record[0] & 0x80:
                touch_item_count = record[0] & 0x7f
                touch_items = [record[i + 1:i + 6] for i in range(0, 5 * min(touch_item_count, 5), 5)]
                self.log.info("1 touch %d @ %d: %s", touch_item_count, record[-1], touch_items)


class HidRecorder(HidDecoder):
    def __init__(self):
        self.reports: List[HidReport] = []

    def process(self, report: HidReport):
        self.reports.append(report)


def capture_hidraw_input(device_file: str, hidraw_decoders: List[HidDecoder]):
    log = getLogger(__name__)

    with open(device_file, "rb+", buffering=0) as device:
        try:
            while True:
                report = HidReport(bytearray(device.read(4096)), True)
                log.info("received report: %s", repr(report))
                for decoder in hidraw_decoders:
                    decoder.process(report)
        except KeyboardInterrupt:
            log.info("keyboard interrupt, exiting")


def log_hidraw_reports():
    """
    Read reports input/feature from HIDRAW device and output to console
    """
    basicConfig(level=INFO)

    recorder = HidRecorder()
    wacom_decoder = WacomTouchDecoder()
    capture_hidraw_input("/dev/hidraw0", [recorder, wacom_decoder])

    reports_diff = [recorder.reports[i].differing_bytes_indexes(recorder.reports[i + 1]) for i in range(0, len(recorder.reports) - 1)]

    report_ranges = reduce(lambda x, y: x.insert(y), chain(*reports_diff), Empty()).ranges()

    with open("hidraw.log", "w") as log_file:
        log_file.write(repr(recorder.reports[0]))
        log_file.write("\n")
        log_file.write(recorder.reports[0].hex_header())
        log_file.write(recorder.reports[0].hex_string())
        log_file.write("\n")
        for report in recorder.reports[1:]:
            log_file.write(repr(report))
            log_file.write("\n")
            log_file.write(report.hex_header())
            for range_ in report_ranges:
                log_file.write(report.hex_string(*range_))
            log_file.write("\n")


if __name__ == '__main__':
    log_hidraw_reports()
