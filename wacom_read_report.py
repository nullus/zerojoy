def pretty_print_hex(bytearray_):
    width = 32
    print("      ", " ".join(f"{col:02x}" for col in range(0, width)))

    for line in range(0, len(bytearray_), width):
        b = bytearray_[line:line + width]
        print(f"{line:04x} | ", end="")
        if b:
            print(" ".join(f"{i:02x}" for i in b))


def output_hidraw_reports():
    """
    Read reports input/feature from HIDRAW device and output to console
    """

    with open("/dev/hidraw0", "rb+", buffering=0) as device:
        while True:
            report_data = device.read(1024)
            report_id = report_data[0]
            print(f"Report ID: {report_id}, Report data length: {len(report_data) - 1}")
            pretty_print_hex(report_data[1:])


if __name__ == '__main__':
    output_hidraw_reports()
