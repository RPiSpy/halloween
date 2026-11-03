# RP2040 Moving Skull With Eyes
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
The following is assumed:
* the RP2040 device is runnig the latest firmware.
* you are able to load files onto the device using a client such as Thonny or VSCode.
* Servo 1 is a MG996R type.
* Servo 2 is a SG90 type.

# Files
* main.py

# Setup
## Software
* Copy main.py to device

## NeoPixels
* Data   - Connect to GP26
* Vcc    - Connect to 5V pin
* Gnd    - Connect to Gnd pin

## Button
A simple momentary action switch with two contacts.
* A      - Connect to Gnd pin
* B      - Connect to GP11

## Servos
### Servo 1 - Head
MG996R Type
* Signal - Connect to GP14
* Vcc    - Connect to 5V pin
* Gnd    - Connect to Gnd pin

### Servo 2 - Jaw
SG90 Type
* Signal - Connect to GP15
* Vcc    - Connect to 5V pin
* Gnd    - Connect to Gnd pin

## RP2040
Power via a suitable USB power source.

# Usage
* Attach all hardware items
* Double-check connections inparticular the power and ground
* Power the device
* Servos should centre
* NeoPixels should illuminate
* Pressing the button should change colour mode
* Both servos should move in a random pattern

# Notes
* You can use this code with or without both servos, the neopixels or the button.
