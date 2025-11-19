# Halloween

This is a collection of scripts used in my Halloween projects.

# RP2040 PIR Relay Actuator
This script monitors a PIR and activates a Relay when motion is detected.
It can be used to activate a shop bought halloween decoration/prop that
has a momentary action button. Although it works on an RP2040 Zero it could
be used on a Pi Pico but you may need to update the GPIO references.

# RP2040 Skull Eyes
This script provides two neopixel 'eyes' for a Halloween skull. A button can
be used to switch colour modes. A servo provides movement.

# RP2040 Servo Calibration
This script allows a servo to be tested. Buttons can be used to increase/decrease the duty ratio and send the servo to it's minimum and maximum travel. Suitable for a servo with a duty range of 1ms to 2ms. This values can be adjusted if required.

#  RP2040 Motion Eyes Sound
This script provides two neopixel 'eyes' with motion activated sound. The idea is to add eyes and sound
to an existing prop such as a giant spider.
