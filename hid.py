from abc import ABCMeta, abstractmethod
from contextlib import contextmanager


class HidDevice(object, metaclass=ABCMeta):
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