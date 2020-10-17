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