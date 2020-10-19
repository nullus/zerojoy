# Raspberry Pi Zero USB device

## The basis for a custom built USB HID

I'll choose a catchier name once this is up and running. 

### Requirements

* [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/)
* Linux VM (to manipulate ext4 filesystem)

### Set up

#### Image

Image SD card with Raspberry Pi OS (other) → Raspberry Pi OS Lite (32-bit)

#### USB Serial login

Append to first line in /boot/cmdline.txt on SD card:

    modules-load=dwc2,g_serial

Paste at the end of /boot/config.txt:

    dtoverlay=dwc2

Mount SD card root, and symlink getty service to start on boot:

    sudo ln -s /lib/systemd/system/getty@.service <SD card mount point>/etc/systemd/system/getty.target.wants/getty@ttyGS0.service

### Prototype

Undo _most_ of the above, it interferes with configuring USB gadget. Keep `/boot/config.txt` changes

Create device using libcomposite:

    sudo tar -C /sys/kernel/config/usb_gadget/ -xf zerojoy.tar --overwrite --no-same-owner
    sudo ln -s /sys/kernel/config/usb_gadget/zerojoy/functions/hid.usb0 /sys/kernel/config/usb_gadget/zerojoy/configs/c.1/
    ls /sys/class/udc | sudo tee /sys/kernel/config/usb_gadget/zerojoy/UDC

### To do/Next steps

  * Define usb_gadget configuration in code
    * HID report descriptor library
  * Programmatic deployment (e.g. Ansible via SSH, or bootstrap from git)
  * Overlayfs for read-only filesystem (i.e device hardening)
  * Build a controller for old PC 15-pin joystick, throttle, and rudder devices (e.g. CH Products)
    * ADC for Raspberry Pi Zero: [RasPiO Analog Zero](https://raspberry.piaustralia.com.au/collections/shields-and-add-ons/products/raspio-analog-zero)
    * Old CH Products: [eBay search](https://www.ebay.com.au/sch/i.html?_nkw=CH+Products&_sacat=1249)
  * Integrate Wacom Intuos Pro via Bluetooth (via HIDRAW)
    * Reverse engineer HID report
    * Design transparency for control areas
    * Create mapping for touch (up to 2?) to joystick
  * Build custom controller? 🤪
  
### References

  * [Setup for OTG Serial Gadget](https://raspberrypi.stackexchange.com/a/75551)
  * [Turn Your Raspberry Pi Zero into a USB Keyboard (HID)](https://randomnerdtutorials.com/raspberry-pi-zero-usb-keyboard-hid/) — uses libcomposite for quick device configuration
  * [pid.codes is a registry of USB PID codes for open source hardware projects](https://pid.codes/)
  * [HIDRAW - Raw Access to USB and Bluetooth Human Interface Devices](https://www.kernel.org/doc/html/latest/hid/hidraw.html)
  * [Device Class Definition for Human Interface Devices (HID)](https://www.usb.org/sites/default/files/hid1_11.pdf)
  * [HID Usage Tables](https://usb.org/sites/default/files/hut1_2.pdf)