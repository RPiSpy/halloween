# RP2040 PIR Relay Actuator
This script monitors a PIR and activates a Relay when motion is detected.
It can be used to activate a shop bought halloween decoration/prop that
has a momentary action button. Although it works on an RP2040 Zero it could
be used on a Pi Pico but you may need to update the GPIO references.

You can set a startup time to allow yourself time to get out of the range of
the PIR. A duration can be set to match the duration of the light/sound sequence
as well as a 'snooze' delay to stop the relay being activated to quickly.
* Start-up Sequence  : Flashing green, flashing amber, flashing red
* Flashing blue      : Waiting for motion
* Violet             : Relay active
* Red                : PIR active, waiting for duration + snooze delays
* Flashing red       : PIR activated, waiting for minimum delay to pass

# Hardware
* RP2040 based device
* PIR
* Relay module
* 5V power source

# Assumptions
It is assumed the RP2040 device is runnig the latest firmware. It is assumed you are able
to load files onto the device using a client such as Thonny or VSCode.

# Files
* main.py - The main script which must be copied to the RP2040
* hardware-test.py - An optional script which can be run to test the attached hardware
* pir-test.py - An optional script which can be run to the test the attached PIR

# Setup
## Software
* Copy main.py to device
## PIR
* Gnd  - Connect to a Gnd pin
* Data - Connect to GPIO28
* Vcc  - Connect to 3.3V or 5V (check PIR specifications)

## Relay
* Gnd    - Connect to a Gnd pin
* IN1    - Connect to GPIO29
* Vcc    - Connect to 3.3V or 5V (check relay specifications)
* Common - Connect to prop button wire
* NO     - Connect to prop button wire

## RP2040
Power via a suitable USB power source.

# Usage
* Attach all hardware items
* Double-check connections inparticular the power and ground
* Power the device
* Movement in front of the PIR should trigger the relay
* No activiations will be possible during the 'snooze' period