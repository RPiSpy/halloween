#--------------------------------------
#    ___  ___  _ ____          
#   / _ \/ _ \(_) __/__  __ __ 
#  / , _/ ___/ /\ \/ _ \/ // / 
# /_/|_/_/  /_/___/ .__/\_, /  
#                /_/   /___/   
#
#  RP2040 Zero PIR Relay Activator
#
# Author : Matt Hawkins
# Date   : 13/10/2024
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
RELAY1_PIN=28            # User pin choice for Relay #1 data

# Define some timings
STARTUP_TIME=10          # How long to wait before checking for PIR changes
RELAY1_TRIGGER_TIME=0.5  # How long to keep Relay #1 active when triggered
SEQUENCE_DURATION=10     # How long the light/sound sequence of prop lasts
SNOOZE=10                # How long to wait before we want another activation
PIR_OFF_WAIT=10          # How long to stay in the OFF state
PIXEL_BRIGHTNESS=10      # Set brightness as a percentage

# Define some colours
COLOUR_RED=(255,0,0)
COLOUR_GREEN=(0,255,0)
COLOUR_BLUE=(0,0,255)
COLOUR_ORANGE=(255,128,0)
COLOUR_VIOLET=(255,0,255)
COLOUR_CLEAR=(0,0,0)

def pixelColour(baseColour,brightness=20):
    brightness=brightness/100
    if brightness>0 and brightness<=1:
        adjustedColour=tuple([int(x*brightness) for x in baseColour])
    else:
        adjustedColour=tuple([int(x*0.2) for x in baseColour])
    pixel.fill(adjustedColour)
    pixel.write()    

# Define function to blink pixel
def blink(pixel,baseColour,brightness,duration,delay):
    brightness=brightness/100
    if brightness>0 and brightness<1:
        adjustedColour=tuple([int(x*brightness) for x in baseColour])
    else:
        adjustedColour=baseColour
    start = time.time()
    while time.time()-start<duration:
        pixel.fill(adjustedColour)
        pixel.write()
        time.sleep(delay/2)
        pixel.fill((0,0,0))
        pixel.write()        
        time.sleep(delay/2)

# Setup neopixel
pixel = neopixel.NeoPixel(machine.Pin(LED_PIN), 1)

# Setup PIR
pir = machine.Pin(PIR_PIN, machine.Pin.IN,machine.Pin.PULL_DOWN)

# Setup and close relay
relay1 = machine.Pin(RELAY1_PIN, machine.Pin.OUT)
relay1.low()

print("You have %s secounds to clear the area!" % STARTUP_TIME)

# Give user time to leave the area
blink(pixel,COLOUR_GREEN,PIXEL_BRIGHTNESS,STARTUP_TIME/3,1)
# Orange LED
blink(pixel,COLOUR_ORANGE,PIXEL_BRIGHTNESS,STARTUP_TIME/3,0.6)
# Red LED
blink(pixel,COLOUR_RED,PIXEL_BRIGHTNESS,STARTUP_TIME/3,0.2)

while pir.value()==1:
    print("Waiting for PIR to settle")
    pixelColour(COLOUR_RED,PIXEL_BRIGHTNESS)
    time.sleep(1)
    pixelColour(COLOUR_BLUE,PIXEL_BRIGHTNESS)
    time.sleep(1)

print("Now waiting for motion")

while True:

    pirState=pir.value()

    if pirState==1:
        print("PIR ON")

        # Trigger Relay #1
        print("  Trigger Relay #1 for %s seconds" % RELAY1_TRIGGER_TIME)
        pixelColour(COLOUR_VIOLET,PIXEL_BRIGHTNESS)
        relay1.high()
        time.sleep(RELAY1_TRIGGER_TIME)
        relay1.low()
        pixelColour(COLOUR_RED,PIXEL_BRIGHTNESS)

        # Wait for light/sound sequence to finish
        print("  Wait %s seconds" % SEQUENCE_DURATION)
        time.sleep(SEQUENCE_DURATION)

        # Snooze
        print("  Snooze for %s seconds" % SNOOZE)
        time.sleep(SNOOZE)

        print("Now waiting for motion")

    pixelColour(COLOUR_BLUE,PIXEL_BRIGHTNESS)
    time.sleep(0.5)
    pixelColour(COLOUR_CLEAR)
    time.sleep(0.2)