from logging import getLogger

from zerojoy.wacom.model import TouchRecord


class TouchMapper:

    def __init__(self) -> None:
        super().__init__()
        self.log = getLogger(__name__)

    def submit(self, record: TouchRecord):
        self.log.info("TouchMapper: %s", record)
