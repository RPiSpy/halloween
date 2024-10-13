# Halloween

This is a collection of scripts used in my Halloween projects.

# RP2040 PIR Relay Actuator
This script was created to run on an RP2040 Zero. It monitors a PIR and
activates a Relay when motion is detected. It can be used to activate a shop
bought halloween decoration/prop that has a momentary action button.
Although it works on an RP2040 Zero it could be used on a Pi Pico but you may
need to update the GPIO references.

You can set a startup time to allow yourself time to get out of the range of
the PIR. Delays can be set for the ON and OFF states so you can reduce the
number of activations during regular PIR events.
