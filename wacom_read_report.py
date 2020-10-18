
def output_hidraw_reports():
    """
    Read reports input/feature from HIDRAW device and output to console
    """

    with open("/dev/hidraw0", "rb+", buffering=0) as device:
        while True:
            report_data = device.read(1024)
            print(f"Report data length: {len(report_data)}")
            print(report_data.hex())


if __name__ == '__main__':
    output_hidraw_reports()
