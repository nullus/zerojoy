from logging import getLogger
from struct import Struct
from typing import List, Iterable, Tuple, Any

from zerojoy.wacom.model import TouchRecord, Touch
from zerojoy.hid import HidReport, HidDecoder
from zerojoy.wacom.port import TouchMapper


class WacomTouchDecoder(HidDecoder):
    """
    Decode Wacom Intuos Pro HID (raw)

    Each HID report contains up to three events, each event contains up to five touch coordinates
    """

    TOUCH_OFFSET = 0x6c
    TOUCH_RECORD_SIZE = 43
    TOUCH_RECORDS_PER_REPORT_MAX = 3
    TOUCH_ITEMS_PER_RECORD_MAX = 5
    TOUCH_RECORD_VALID_BIT = 0x80
    TOUCH_RECORD_TOUCH_ITEMS_BITS = 0x7f
    TOUCH_ITEM_ELEMENTS_COUNT = 6

    def __init__(self, mappers: List[TouchMapper]):
        super().__init__()
        self.mappers = mappers
        self.log = getLogger(__name__)

        self.record_format = Struct("<B" + "2B2H2B" * self.TOUCH_ITEMS_PER_RECORD_MAX + "H")

    def process(self, report: HidReport):
        if report.report_id == 0x80:
            for record in self._parse_records(report.data[self.TOUCH_OFFSET:]):
                for mapper in self.mappers:
                    mapper.submit(record)
        else:
            self.log.warning("unrecognised report ID: %d", report.report_id)

    def _parse_records(self, records: bytearray) -> Iterable[TouchRecord]:
        for offset in range(0, self.TOUCH_RECORDS_PER_REPORT_MAX * self.TOUCH_RECORD_SIZE, self.TOUCH_RECORD_SIZE):
            record = self.record_format.unpack(records[offset:offset + self.TOUCH_RECORD_SIZE])
            (is_valid, touch_item_total) = (
                record[0] & self.TOUCH_RECORD_VALID_BIT != 0, record[0] & self.TOUCH_RECORD_TOUCH_ITEMS_BITS)
            (event_time, event_time_id) = divmod(record[-1], 100)
            if is_valid and touch_item_total != 0:
                yield TouchRecord(
                    self._parse_touch_items(record[1:-1], touch_item_total),
                    event_time, event_time_id
                )

    def _parse_touch_items(self, record: Tuple[Any], touch_item_total: int) -> List[Touch]:
        touch_item_count = min(touch_item_total, self.TOUCH_ITEMS_PER_RECORD_MAX)
        return [
            Touch(record[i], record[i + 1] != 0, record[i + 2], record[i + 3], record[i + 4], record[i + 5])
            for i in range(0, self.TOUCH_ITEM_ELEMENTS_COUNT * touch_item_count, self.TOUCH_ITEM_ELEMENTS_COUNT)
        ]
