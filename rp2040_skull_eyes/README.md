# RP2040 Skull Eyes
This script provides two neopixel 'eyes' for a Halloween skull. A button can
be used to switch colour modes.

# Hardware
* RP2040 based device
* 2 NeoPixels
* 1 momentary switch
* Plastic skull
* 5V power source

# Assumptions
It is assumed the RP2040 device is runnig the latest firmware. It is assumed you are able
to load files onto the device using a client such as Thonny or VSCode.

# Files
* main.py

# Setup
## Software
* Copy main.py to device

## NeoPixels
* Gnd
* Data
* Vcc
## Button
* A - Connect to Ground
* B - Connect to GPIOXX

# Usage
* Attach all hardware items
* Double-check connections inparticular the power and ground
* Power the device
* NeoPixels should illuminate
* Pressing the button should change colour mode