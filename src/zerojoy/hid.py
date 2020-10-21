from abc import ABCMeta, abstractmethod, ABC
from contextlib import contextmanager
from datetime import datetime
from itertools import zip_longest
from logging import getLogger
from typing import Optional, List


class HidDevice(metaclass=ABCMeta):
    def __init__(self, device) -> None:
        super().__init__()
        self.device = device

    def send_report(self):
        self.device.write(self.encode())
        self.device.flush()

    @abstractmethod
    def encode(self):
        pass


@contextmanager
def hid(device_name, cls):
    with open(device_name, 'rb+') as device:
        yield cls(device)


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


def capture_hidraw_input(hidraw_decoders: List[HidDecoder], device_file: str = "/dev/hidraw0"):
    log = getLogger(__name__)

    with open(device_file, "rb+", buffering=0) as device:
        try:
            while True:
                report = HidReport(bytearray(device.read(4096)), True)
                log.debug("received report: %s", repr(report))
                for decoder in hidraw_decoders:
                    decoder.process(report)
        except KeyboardInterrupt:
            log.info("keyboard interrupt, exiting")
