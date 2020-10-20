
Wacom report descriptor:

    06 0d ff    Usage Page (0xff0d)
    09 01       Usage (Pointer)
    a1 01       Collection (Application)
    15 00       Logical Minimum (0)
    26 ff 00    Logical Maximum (0xff)
    75 08       Report Size (8)
    85 81       Report ID (0x81)
    09 01       Usage (Pointer)
    95 32       Report Count (50)
    81 02       Input (Data, Variable, Absolute)
    85 80       Report ID (0x80)
    09 01       Usage (Pointer)
    96 68 01    Report Count (0x168)
    81 02       Input (Data, Variable, Absolute)
    85 82       Report ID (0x82)
    09 01       Usage (Pointer)
    95 32       Report Count (50)
    b1 02       Feature (Data, Variable, Absolute) ??
    85 83       Report ID (0x83)
    09 01       Usage (Pointer)
    96 68 01    Report Count (0x168)
    b1 02       Feature (Data, Variable, Absolute) ??
    85 84       Report ID (0x84)
    09 01       Usage (Pointer)
    95 32       Report Count (50)
    91 02       Output (Data, Variable, Absolute) ??
    85 85       Report ID (0x85)
    09 01       Usage (Pointer)
    96 68 01    Report Count (0x168)
    91 02       Output (Data, Variable, Absolute) ??
    c0          End collection
    
How to describe a device, but tell us ~~almost~~ nothing. Good work!

Examining logs from wacom-read-report:

    HidReport(...) <report_id = 128, data = 360 bytes, created_at = 2020-10-20T03:09:37.220154> 
           00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 
    006c | 85 01 01 77 10 76 06 03 03 02 01 64 0d b0 0d 02
    007c | 03 03 01 54 10 c5 11 01 01 04 01 3c 14 7f 12 02
    008c | 02 06 01 a8 1a ff 11 02 02 e4 7a 85 01 01 77 10
    009c | 76 06 03 03 02 01 68 0d ab 0d 02 03 03 01 55 10
    00ac | c2 11 01 01 04 01 3c 14 7c 12 02 02 06 01 a8 1a
    00bc | ff 11 02 02 48 7b 00 00 00 00 00 00 00 00 00 00
    00cc | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    00dc | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    00ec | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    00fc | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    010c | 00 00 00 00 00 00 00 00 00 00 00 00
    
The overall structure consists of 0 - 3(?) sets of log structures, each designed to store up to 5 touch events.

 * 0x00:  bit 8 indicates a record, remaining bits indicate the number of touches (1, 2, 3, 4, 5, 6 +) if touches is 0, this is an extension (for > 5 touches)
 * 0x01 - 0x08 touch #1
 * 0x09 - 0x10 touch #2
 * 0x11 - 0x18 touch #3
 * 0x19 - 0x20 touch #4
 * 0x21 - 0x28 touch #5
 * 0x29 - 0x2a time/record ID (monotonic 16-bit unsigned LE counter)

Touch record:

 * 0x00: Touch ID (1, 2, 3, 4, 6, ...) (Not sure where 5 went)
 * 0x01: Touch on/off?
 * 0x02 - 0x07: ??? 

From examining drivers/documentation x, y coordinates may have 12-bit precision split over two bytes. Some bits may record a capacitance value, which could be fun.
