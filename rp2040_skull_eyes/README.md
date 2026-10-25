# RP2040 Skull Eyes
This script controls two servos and two neopixel 'eyes' for a Halloween skull. A button can
be used to switch colour modes. The servos are used to rotate the head and move the jaw.

# Hardware
* RP2040 based device
* 2 NeoPixels
* 1 momentary switch
* 2 servos
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
* Gnd    - Connect to Gnd pin
* Data   - Connect to GP26
* Vcc    - Connect to 5V pin
## Button
* A      - Connect to Gnd pin
* B      - Connect to GP12
## Servos
### Servo 1 - Head
* Gnd    - Connect to Gnd pin
* Signal - Connect to GP14
* Vcc    - Connect to 5V pin
### Servo 2 - Jaw
* Gnd    - Connect to Gnd pin
* Signal - Connect to GP15
* Vcc    - Connect to 5V pin

## RP2040
Power via a suitable USB power source.

# Usage
* Attach all hardware items
* Double-check connections inparticular the power and ground
* Power the device
* NeoPixels should illuminate
* Pressing the button should change colour mode
* Both servos should move in a random pattern
