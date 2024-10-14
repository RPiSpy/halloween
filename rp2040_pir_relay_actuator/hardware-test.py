#--------------------------------------
#    ___  ___  _ ____          
#   / _ \/ _ \(_) __/__  __ __ 
#  / , _/ ___/ /\ \/ _ \/ // / 
# /_/|_/_/  /_/___/ .__/\_, /  
#                /_/   /___/   
#
#  RP2040 Zero PIR Relay Activator
#  HARDWARE TEST SCRIPT
#
# Author : Matt Hawkins
# Date   : 14/10/2024
#
# https://www.raspberrypi-spy.co.uk/
#
# The MIT License (MIT)
# Copyright 2024 Matt Hawkins
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#--------------------------------------
import machine
import time
import neopixel

# Define hardware values
LED_PIN=16               # Set pin number for onboard LED
PIR_PIN=29               # User pin choice for PIR data
RLY1_PIN=28              # GPIO for Relay #1 data
RLY1_ON_STATE=0          # 1 relay is active High
                         # 0 relay is active Low

# Define some timings
LED_BRIGHTNESS=10        # Set brightness as a percentage

# Define some colours
COLOUR_RED=(255,0,0)
COLOUR_GREEN=(0,255,0)
COLOUR_BLUE=(0,0,255)
COLOUR_ORANGE=(255,128,0)
COLOUR_VIOLET=(255,0,255)
COLOUR_YELLOW=(255,255,0)
COLOUR_CLEAR=(0,0,0)

def ledColour(baseColour,brightness=20):
    brightness=brightness/100
    if brightness>0 and brightness<=1:
        adjustedColour=tuple([int(x*brightness) for x in baseColour])
    else:
        adjustedColour=tuple([int(x*0.2) for x in baseColour])
    led.fill(adjustedColour)
    led.write()    

# Setup neopixel
led = neopixel.NeoPixel(machine.Pin(LED_PIN), 1)

# Setup PIR
pir = machine.Pin(PIR_PIN, machine.Pin.IN,machine.Pin.PULL_UP)

# Setup and close relay
relay1 = machine.Pin(RLY1_PIN, machine.Pin.OUT,not RLY1_ON_STATE)

while True:
    relay1.value(not RLY1_ON_STATE)
    print("Relay Off")
    ledColour(COLOUR_GREEN,LED_BRIGHTNESS)
    time.sleep(5)

    print("PIR value : " + str(pir.value()))

    relay1.value(RLY1_ON_STATE)
    print("Relay On")
    ledColour(COLOUR_RED,LED_BRIGHTNESS)
    time.sleep(5)

    print("PIR value : " + str(pir.value()))