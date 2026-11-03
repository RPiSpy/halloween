#--------------------------------------
#    ___  ___  _ ____          
#   / _ \/ _ \(_) __/__  __ __ 
#  / , _/ ___/ /\ \/ _ \/ // / 
# /_/|_/_/  /_/___/ .__/\_, /  
#                /_/   /___/   
#
#  RP2040 Skull Eyes 
#
# This script has been written for a RP2040 based device.
# It sets the colour of two NeoPixels and controls two
# servos. The first servo is assumed to control the
# head and the other the jaw.
#
# Author : Matt Hawkins
# Date   : 03/11/2026
#
# Connect Servo 1 to GPIO12
# Connect Servo 2 to GPIO13
# Connect Button 1 to GPIO11 (changes eye mode)
# Connect Neopixels to GPIO26
#
# https://www.raspberrypi-spy.co.uk/
#
# The MIT License (MIT)
# Copyright 2025 Matt Hawkins
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

# Import required libraries
import machine
import neopixel
import random
import time
import _thread

# Function to adjust a colour with a defined brightness
def get_colour(baseColour,brightness=20):
    # Take a colour tuple and adjust the values using the brightness value
    brightness=brightness/100
    if brightness>0 and brightness<1:
        adjustedColour=tuple([int(x*brightness) for x in baseColour])
    else:
        adjustedColour=baseColour
    return adjustedColour

# Function to rotate through lighting modes
def callback(mode_button):
    global mode, debounce_time
    if (time.ticks_ms()-debounce_time) > 500:
        mode=mode+1
        if mode>5:
            mode=mode = 1
        print("LED Mode: "+ str(mode))
        debounce_time=time.ticks_ms()

# Function to move servos
def servo_move():
    # Set servos to mid position
    servo1.duty_u16(SRV1_MID_DUTY)
    servo2.duty_u16(SRV2_MID_DUTY)

    while True:
        # Random delay in milliseconds
        time.sleep_ms(random.randint(0, 200))
      
        # Move servo 1 - Head
        if random.randint(1, 3)==1:
            # Move servo 1
            duty = random.randint(SRV1_MIN_DUTY, SRV1_MAX_DUTY)
            servo1.duty_u16(duty)
            #print("Head : ",duty)

        # Move servo 2 - Jaw
        if random.randint(1, 2)==1:
            duty = random.choice([SRV2_MIN_DUTY,SRV2_MID_DUTY,SRV2_MAX_DUTY])
            servo2.duty_u16(duty)
            #print("Jaw : ",duty)

# Define Pins that hardware is connected to
LED_PIN=16               # Set pin number for onboard LED
NEO_PIN=26               # NeoPixels
SRV1_PIN=12              # Servo 1 - Head
SRV2_PIN=13              # Servo 2 - Jaw
BTN1_PIN=11              # Momentary switch

# Define some parameters for hardware
NEO_BPP=3                # 3 for RGB, 4 for RGBW

# Pulse Width   U16 Value
#       500us   1638
#      1000us   3276
#      2000us   6554
#      2500us   8192
# U16 65,535 represents 20ms so 1ms is ~3276

# Experimental Values
# SG90 3276 to 6554 gives 90 degree movement
# SG90 2480 to 7350 gives ~160 degree movement

# Servo pulse frequency (Hz)
SRV1_FRQ=50
SRV2_FRQ=50

# Servo 1 - Head (U16 Value)
SRV1_MIN_DUTY=3276
SRV1_MAX_DUTY=6554
SRV1_MID_DUTY=int((SRV1_MIN_DUTY+SRV1_MAX_DUTY)/2)

# Servo 2 - Jaw (U16 Value)
SRV2_MIN_DUTY=2480
SRV2_MAX_DUTY=7350
SRV2_MID_DUTY=int((SRV2_MIN_DUTY+SRV2_MAX_DUTY)/2)

# Define some NeoPixel parameters
NEO_BRIGHTNESS=25        # Set brightness as a percentage for eyes
LED_BRIGHTNESS=2         # Set brightness as a percentage for onboard LED

# Define some colours
COLOUR_RED=(255,0,0,0)
COLOUR_GREEN=(0,255,0,0)
COLOUR_BLUE=(0,0,255,0)
COLOUR_ORANGE=(255,50,0,0)
COLOUR_VIOLET=(255,0,255,0)
COLOUR_YELLOW=(255,255,0,0)
COLOUR_TEAL=(72,201,176,0)
COLOUR_PURPLE=(108,52,131,0)
COLOUR_CLEAR=(0,0,0)
COLOUR_DEFAULT = COLOUR_ORANGE

COLOUR_WHEEL = [
                COLOUR_BLUE,
                COLOUR_GREEN,
                COLOUR_RED,
                COLOUR_YELLOW,
                COLOUR_VIOLET,
                COLOUR_ORANGE,
                COLOUR_TEAL,
                COLOUR_PURPLE
                ]

# Setup onboard LED
onboardLed = neopixel.NeoPixel(machine.Pin(LED_PIN), 1)
onboardLed.fill(get_colour(COLOUR_BLUE,LED_BRIGHTNESS))
onboardLed.write()  

# Setup two Neopixels
pixels = neopixel.NeoPixel(machine.Pin(NEO_PIN), 2, bpp=NEO_BPP)

# Setup mode button using interupt with debouncing
mode = 1
debounce_time = 0
mode_button = machine.Pin(BTN1_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
mode_button.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)

print("Set servos to mid-point")

# Setup servo 1
servo1 = machine.PWM(machine.Pin(SRV1_PIN))
servo1.freq(SRV1_FRQ)
servo1.duty_u16(SRV1_MID_DUTY)

# Setup servo 2
servo2 = machine.PWM(machine.Pin(SRV2_PIN))
servo2.freq(SRV2_FRQ)
servo2.duty_u16(SRV2_MID_DUTY)

time.sleep(3)

# Start servo function to randomly move servo positions
servo_thread = _thread.start_new_thread(servo_move, ())

print("LED Mode: "+ str(mode))

# Main loop
while True:

    # Mode 1: pulse red
    # Break out of loop if mode changes
    while mode==1:
        for index in range(16,256):
            colour=(index,0,0,0)
            pixels[0] = get_colour(colour, NEO_BRIGHTNESS)
            pixels[1] = get_colour(colour, NEO_BRIGHTNESS)
            pixels.write()
            time.sleep_ms(10)
            if mode!=1:
                break
        for index in range(256,16,-1):
            colour=(index,0,0,0)
            pixels[0] = get_colour(colour, NEO_BRIGHTNESS)
            pixels[1] = get_colour(colour, NEO_BRIGHTNESS)
            pixels.write()
            time.sleep_ms(10)
            if mode!=1:
                break

    # Mode 2: pulse green
    # Break out of loop if mode changes
    while mode==2:
        for index in range(16,256):
            colour=(0,index,0,0)
            pixels[0] = get_colour(colour, NEO_BRIGHTNESS)
            pixels[1] = get_colour(colour, NEO_BRIGHTNESS)
            pixels.write()
            time.sleep_ms(10)
            if mode!=2:
                break
        for index in range(256,16,-1):
            colour=(0,index,0,0)
            pixels[0] = get_colour(colour, NEO_BRIGHTNESS)
            pixels[1] = get_colour(colour, NEO_BRIGHTNESS)
            pixels.write()
            time.sleep_ms(10)
            if mode!=2:
                break

    # Mode 3: cycle through all colours
    # Break out of loop if mode changes
    while mode==3:
        for colour in COLOUR_WHEEL:    
            pixels[0] = get_colour(colour, NEO_BRIGHTNESS)
            pixels[1] = get_colour(colour, NEO_BRIGHTNESS)
            pixels.write()
            time.sleep(1)
            if mode!=3:
                break

    # Mode 4: cycle from green to red
    # Break out of loop if mode changes
    while mode==4:
        for colour in [COLOUR_GREEN,COLOUR_RED]:    
            pixels[0] = get_colour(colour, NEO_BRIGHTNESS)
            pixels[1] = get_colour(colour, NEO_BRIGHTNESS)
            pixels.write()
            time.sleep(1)
            if mode!=4:
                break

    # Mode 5: fade between red and green
    # Break out of loop if mode changes
    while mode==5:
        for index in range(0,256):
            colour=(index,255-index,0,0)
            pixels[0] = get_colour(colour, NEO_BRIGHTNESS)
            pixels[1] = get_colour(colour, NEO_BRIGHTNESS)
            pixels.write()
            time.sleep_ms(10)
            if mode!=5:
                break
        for index in range(0,256):
            colour=(255-index,index,0,0)
            pixels[0] = get_colour(colour, NEO_BRIGHTNESS)
            pixels[1] = get_colour(colour, NEO_BRIGHTNESS)
            pixels.write()
            time.sleep_ms(10)
            if mode!=5:
                break
