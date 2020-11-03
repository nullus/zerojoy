#!/usr/bin/env python

from fcntl import ioctl
from struct import unpack


# 32-bit architecture
_C_INT_SIZE = 4

# From /usr/include/asm-generic/ioctl.h
_IOC_NRBITS = 8
_IOC_TYPEBITS = 8
_IOC_SIZEBITS = 14
_IOC_DIRBITS = 2
_IOC_WRITE = 1 << 0
_IOC_READ = 1 << 1
_IOC_NRMASK = (1 << _IOC_NRBITS) - 1
_IOC_TYPEMASK = (1 << _IOC_TYPEBITS) - 1
_IOC_SIZEMASK = (1 << _IOC_SIZEBITS) - 1
_IOC_DIRMASK = (1 << _IOC_DIRBITS) - 1
_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_SIZESHIFT = _IOC_TYPESHIFT + _IOC_TYPEBITS
_IOC_DIRSHIFT: int = _IOC_SIZESHIFT + _IOC_SIZEBITS


def _IOC(write: bool, type_: str, number: int, size: int) -> int:
    """
    Create ioctl request
    """
    return (
        (_IOC_WRITE if write else _IOC_READ) << _IOC_DIRSHIFT |
        (ord(type_) & _IOC_TYPEMASK) << _IOC_TYPEBITS |
        (number & _IOC_NRMASK) << _IOC_NRSHIFT |
        (size & _IOC_SIZEMASK) << _IOC_SIZESHIFT
    )


# From /usr/include/linux/hid.h
HID_MAX_DESCRIPTOR_SIZE = 4096

# From /usr/include/linux/hidraw.h
HIDIOCGRDESCSIZE = _IOC(False, 'H', 0x01, _C_INT_SIZE)
HIDIOCGRDESC = _IOC(False, 'H', 0x02, _C_INT_SIZE + HID_MAX_DESCRIPTOR_SIZE)
def HIDIOCGRAWNAME(length: int) -> int: return _IOC(False, 'H', 0x04, length)


def main():
    """
    Retrieve and display HID report descriptor from /dev/hidraw0
    """

    with open("/dev/hidraw0", "rb+") as device:
        name_array = bytearray(256)
        ioctl(device.fileno(), HIDIOCGRAWNAME(len(name_array)), name_array)
        print(name_array.split(b'\x00', 1)[0].decode())
        size_array = bytearray(4)
        ioctl(device.fileno(), HIDIOCGRDESCSIZE, size_array)
        size = unpack("I", size_array)[0]
        print(f"hidraw report size = {size}")
        report_desc_array = size_array + bytearray(HID_MAX_DESCRIPTOR_SIZE)
        ioctl(device.fileno(), HIDIOCGRDESC, report_desc_array)
        report_desc = report_desc_array[_C_INT_SIZE:size + _C_INT_SIZE].hex()
        print("report descriptor:")
        print(report_desc)


if __name__ == '__main__':
    main()
