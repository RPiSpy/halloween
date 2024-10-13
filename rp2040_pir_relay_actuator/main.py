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

# Define some constants
LED_PIN=16               # Set pin number for onboard LED
PIR_PIN=29               # User pin choice for PIR data
RELAY1_PIN=28            # User pin choice for Relay #1 data
STARTUP_TIME=20          # How long to wait before checking for PIR changes
RELAY1_TRIGGER_TIME=0.5  # How long to keep Relay #1 active when triggered
PIR_ON_WAIT=30           # How long to stay in the ON state
PIR_OFF_WAIT=10          # How long to stay in the OFF state

# Define some colours
COLOUR_RED=(64,0,0)
COLOUR_GREEN=(0,64,0)
COLOUR_BLUE=(0,0,64)
COLOUR_ORANGE=(64,46,0)

# Define function to blink pixel
def blink(pixel,colour,duration,delay):
    start = time.time()
    while time.time()-start<duration:
        pixel.fill(colour)
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
blink(pixel,COLOUR_GREEN,STARTUP_TIME/3,1)
# Orange LED
blink(pixel,COLOUR_ORANGE,STARTUP_TIME/3,0.6)
# Red LED
blink(pixel,COLOUR_RED,STARTUP_TIME/3,0.2)

while pir.value()==1:
    print("Waiting for PIR to settle")
    pixel.fill(COLOUR_RED)
    pixel.write()
    time.sleep(1)
    pixel.fill(COLOUR_BLUE)
    pixel.write()
    time.sleep(1)

print("Now waiting for PIR")

pixel.fill(COLOUR_BLUE)
pixel.write()

pirCurrentState=0
pirPreviousState=0

while True:
    
    pirCurrentState=pir.value()

    if pirCurrentState!=pirPreviousState:
        
        if pirCurrentState==1:
          print("PIR ON")
          pixel.fill(COLOUR_RED)
          pixel.write()

          # Trigger Relay #1
          print("  Trigger Relay #1")
          relay1.high()
          time.sleep(RELAY1_TRIGGER_TIME)
          relay1.low()

          # Wait
          print("  Wait %s seconds" % PIR_ON_WAIT)
          time.sleep(PIR_ON_WAIT)
        else:
          print("PIR OFF")
          pixel.fill(COLOUR_BLUE)
          pixel.write()
          relay1.low()
          
          # Wait
          print("  Wait %s seconds" % PIR_OFF_WAIT)
          time.sleep(PIR_OFF_WAIT)
 
          print("Wait for PIR")

        pirPreviousState=pirCurrentState