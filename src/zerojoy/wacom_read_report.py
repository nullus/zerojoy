from functools import reduce
from itertools import chain
from logging import basicConfig, INFO
from typing import List

from zerojoy.collections import Empty
from zerojoy.hid import HidReport, HidDecoder, capture_hidraw_input


class HidRecorder(HidDecoder):
    def __init__(self):
        self.reports: List[HidReport] = []

    def process(self, report: HidReport):
        self.reports.append(report)


def main():
    """
    Read reports input/feature from HIDRAW device and output to console
    """
    basicConfig(level=INFO)

    recorder = HidRecorder()
    capture_hidraw_input([recorder])

    reports_diff = [
        recorder.reports[i].differing_bytes_indexes(recorder.reports[i + 1])
        for i in range(0, len(recorder.reports) - 1)]

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
    main()
