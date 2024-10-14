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
PIR_PIN=29               # GPIO PIR data
RLY1_PIN=28              # GPIO for Relay #1 data
RLY1_ON_STATE=0          # 1 relay is active High
                         # 0 relay is active Low

# Define some timings
STARTUP_TIME=10          # How long to wait before checking for PIR changes
RLY1_TRIGGER_TIME=0.5    # How long to keep Relay #1 active when triggered
SEQUENCE_DURATION=10     # How long the light/sound sequence of prop lasts
SNOOZE=10                # How long to wait before we want another activation
PIR_ACTIVE_DELAY=8       # Minimum time PIR must be active for activation
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

# Define function to blink led
def blink(led,baseColour,brightness,duration,delay):
    brightness=brightness/100
    if brightness>0 and brightness<1:
        adjustedColour=tuple([int(x*brightness) for x in baseColour])
    else:
        adjustedColour=baseColour
    start = time.time()
    while time.time()-start<duration:
        led.fill(adjustedColour)
        led.write()
        time.sleep(delay/2)
        led.fill((0,0,0))
        led.write()        
        time.sleep(delay/2)

# Setup neopixel
led = neopixel.NeoPixel(machine.Pin(LED_PIN), 1)

# Setup PIR
pir = machine.Pin(PIR_PIN, machine.Pin.IN)

# Setup relay #1
relay1 = machine.Pin(RLY1_PIN, machine.Pin.OUT, value=not RLY1_ON_STATE)

print("You have %s secounds to clear the area!" % STARTUP_TIME)

# Give user time to leave the area
blink(led,COLOUR_GREEN,LED_BRIGHTNESS,STARTUP_TIME/3,1)
# Orange LED
blink(led,COLOUR_ORANGE,LED_BRIGHTNESS,STARTUP_TIME/3,0.6)
# Red LED
blink(led,COLOUR_RED,LED_BRIGHTNESS,STARTUP_TIME/3,0.2)

while pir.value()==1:
    print("Waiting for PIR to settle")
    ledColour(COLOUR_RED,LED_BRIGHTNESS)
    time.sleep(1)
    ledColour(COLOUR_BLUE,LED_BRIGHTNESS)
    time.sleep(1)

print("Now waiting for motion")

while True:

    pirState=pir.value()

    if pirState==1:
        print("PIR active but lets wait %s seconds" % PIR_ACTIVE_DELAY)
        blink(led,COLOUR_RED,LED_BRIGHTNESS,PIR_ACTIVE_DELAY,0.1)
        pirState=pir.value()

    if pirState==1:
        print("PIR ACTIVE")

        # Trigger Relay #1
        print("  Trigger Relay #1 for %s seconds" % RLY1_TRIGGER_TIME)
        ledColour(COLOUR_VIOLET,LED_BRIGHTNESS)
         
        ledColour(COLOUR_RED,LED_BRIGHTNESS)

        # Wait for light/sound sequence to finish
        print("  Wait %s seconds" % SEQUENCE_DURATION)
        time.sleep(SEQUENCE_DURATION)

        # Snooze
        print("  Snooze for %s seconds" % SNOOZE)
        blink(led,COLOUR_RED,LED_BRIGHTNESS,SNOOZE,1)

        print("Now waiting for motion")

    ledColour(COLOUR_BLUE,LED_BRIGHTNESS)
    time.sleep(0.5)
    ledColour(COLOUR_CLEAR)
    time.sleep(0.2)