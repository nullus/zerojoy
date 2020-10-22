Using the pseudo-code from [HID 1.11 specification](https://www.usb.org/sites/default/files/hid1_11.pdf):
    
    Usage Page (Generic Desktop),               0x05 0x01
    Usage (Joystick),                           0x09 0x04
    Collection (Application),                   0xa1 0x01
        Usage Page (Generic Desktop),           0x05 0x01 # redundant?
        Usage (Pointer),                        0x09 0x01
        Collection (Physical),                  0xa1 0x00
            Logical Minimum (-127),             0x15 0x81
            Logical Maximum (127),              0x25 0x7f
            Report Size (8),                    0x75 0x08
            Report Count (2),                   0x95 0x02
            Usage (X),                          0x09 0x30                          
            Usage (Y),                          0x09 0x31
            Input (Data, Variable, Absolute),   0x81 0x02
            Logical Minimum (0),                0x15 0x00
            Logical Maximum (1),                0x25 0x01
            Report Count (8),                   0x95 0x08
            Report Size (1),                    0x75 0x01
            Usage Page (Buttons),               0x05 0x09 
            Usage Minimum (Button 1),           0x19 0x01
            Usage Maximum (Button 8),           0x29 0x08
            Unit (None),                        0x65 0x00
            Input (Data, Variable, Absolute)    0x81 0x02
        End Collection,                         0xc0
    End Collection                              0xc0

Ignoring above, and instead using the HID report descriptor lifted from my budget joystick adaptor:

    0x05 0x01           Usage Page (Generic Desktop)
    0x09 0x05           Usage (Gamepad)
    0xa1 0x01           Collection (Application)
    0x15 0x00           Logical Minimum (0)
    0x25 0x01           Logical Maximum (1)
    0x35 0x00           Physical Minimum (0)
    0x45 0x01           Physical Maximum (1)
    0x75 0x01           Report Size (1)
    0x95 0x04           Report Count (4)
    0x05 0x09           Usage Page (Buttons)
    0x19 0x01           Usage Minimum (1)
    0x29 0x04           Usage Maximum (4)
    0x81 0x02           Input (Data, Variable, Absolute)
    0x95 0x14           Report Count (20)
    0x81 0x01           Input (Constant, Array, Absolute)
    0x05 0x01           Usage Page (Generic Desktop)
    0x26 0xff 0x00      Logical Maximum (255)
    0x46 0xff 0x00      Physical Maximum (255)
    0x09 0x30           Usage (X)
    0x09 0x31           Usage (Y)
    0x09 0x35           Usage (Rz)
    0x09 0x36           Usage (Slider)
    0x75 0x08           Report Size (8)
    0x95 0x04           Report Count (4)
    0x81 0x02           Input (Data, Variable, Absolute)
    0xc0
    
Attempt adding hat switch description, lifted from [XBox 360 controller](https://github.com/ViGEm/ViGEmBus/issues/40):

    09 39          (LOCAL)  USAGE              0x00010039 Hat switch (Dynamic Value)  
    15 01          (GLOBAL) LOGICAL_MINIMUM    0x01 (1)  
    25 08          (GLOBAL) LOGICAL_MAXIMUM    0x08 (8)  
    35 00          (GLOBAL) PHYSICAL_MINIMUM   0x00 (0)  <-- Info: Consider replacing 35 00 with 34
    46 3B01        (GLOBAL) PHYSICAL_MAXIMUM   0x013B (315)  
    66 1400        (GLOBAL) UNIT               0x0014 Rotation in degrees [1° units] (4=System=English Rotation, 1=Rotation=Degrees)  <-- Info: Consider replacing 66 1400 with 65 14
    75 04          (GLOBAL) REPORT_SIZE        0x04 (4) Number of bits per field  
    95 01          (GLOBAL) REPORT_COUNT       0x01 (1) Number of fields <-- Redundant: REPORT_COUNT is already 1 
    81 42          (MAIN)   INPUT              0x00000042 (1 field x 4 bits) 0=Data 1=Variable 0=Absolute 0=NoWrap 0=Linear 0=PrefState 1=Null 0=NonVolatile 0=Bitmap 
    75 04          (GLOBAL) REPORT_SIZE        0x04 (4) Number of bits per field <-- Redundant: REPORT_SIZE is already 4 
    95 01          (GLOBAL) REPORT_COUNT       0x01 (1) Number of fields <-- Redundant: REPORT_COUNT is already 1 
    15 00          (GLOBAL) LOGICAL_MINIMUM    0x00 (0)  <-- Info: Consider replacing 15 00 with 14
    25 00          (GLOBAL) LOGICAL_MAXIMUM    0x00 (0)  <-- Info: Consider replacing 25 00 with 24
    35 00          (GLOBAL) PHYSICAL_MINIMUM   0x00 (0) <-- Redundant: PHYSICAL_MINIMUM is already 0 <-- Info: Consider replacing 35 00 with 34
    45 00          (GLOBAL) PHYSICAL_MAXIMUM   0x00 (0)  <-- Info: Consider replacing 45 00 with 44
    65 00          (GLOBAL) UNIT               0x00 No unit (0=None)  <-- Info: Consider replacing 65 00 with 64
    81 03          (MAIN)   INPUT              0x00000003 (1 field x 4 bits) 1=Constant 1=Variable 0=Absolute 0=NoWrap 0=Linear 0=PrefState 0=NoNull 0=NonVolatile 0=Bitmap
