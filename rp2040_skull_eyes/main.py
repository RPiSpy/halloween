#--------------------------------------
#    ___  ___  _ ____          
#   / _ \/ _ \(_) __/__  __ __ 
#  / , _/ ___/ /\ \/ _ \/ // / 
# /_/|_/_/  /_/___/ .__/\_, /  
#                /_/   /___/   
#
#  RP2040 Skull Eyes 
#
# Author : Matt Hawkins
# Date   : 24/10/2024
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
import _thread
import random

def getColour(baseColour,brightness=20):
    # Take a colour tuple and adjust the values using the brightness value
    brightness=brightness/100
    if brightness>0 and brightness<1:
        adjustedColour=tuple([int(x*brightness) for x in baseColour])
    else:
        adjustedColour=baseColour
    return adjustedColour

def callback(mode_button):
    global mode, debounce_time
    if (time.ticks_ms()-debounce_time) > 500:
        mode=mode+1
        if mode>4:
            mode=mode = 1
        print("Mode: "+ str(mode))
        debounce_time=time.ticks_ms()

def servo_rotate():
    servo.duty_u16(SRV_MID_DUTY)
    
    max = SRV_MID_DUTY+SRV_END_STOP
    min = SRV_MID_DUTY-SRV_END_STOP
    
    while True:
      time.sleep(random.randint(1, 3))
      duty = random.randint(min, max)      
      servo.duty_u16(duty)    

# Define Pins that hardware is connected to
LED_PIN=16               # Set pin number for onboard LED
BTN_PIN=29               # Momentary switch
NEO_PIN=15               # NeoPixels
SRV_PIN=14               # Servo

# Define some parameters for hardware
NEO_BPP=3                # 3 for RGB, 4 for RGBW



# Servo values for SG90
SRV_FRQ=50               # Pulse frequency of servo
SRV_MAX_DUTY=8500        # Previously measured value
SRV_MIN_DUTY=1700        # Previously measured value
SRV_END_STOP=3000        # Duty either side of mid point
SRV_MID_DUTY=int((SRV_MIN_DUTY+SRV_MAX_DUTY)/2)

# Define some timings
NEO_BRIGHTNESS=20        # Set brightness as a percentage
LED_BRIGHTNESS=10        # Set brightness as a percentage

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
onboardLed.fill(getColour(COLOUR_BLUE,LED_BRIGHTNESS))
onboardLed.write()  

# Setup two neopixels
pixels = neopixel.NeoPixel(machine.Pin(NEO_PIN), 2, bpp=NEO_BPP)

# Setup mode button using interupt with debouncing
mode = 1
debounce_time = 0
mode_button = machine.Pin(BTN_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
mode_button.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)

# Setup servo
servo = machine.PWM(machine.Pin(SRV_PIN))
servo.freq(SRV_FRQ)
servo.duty_u16(SRV_MID_DUTY)

# Start servo function to randomly move servo position
servo_thread = _thread.start_new_thread(servo_rotate, ())

print("Mode: "+ str(mode))

# Main loop
while True:

    # Mode 1: pulse red
    # Break out of loop if mode changes
    while mode==1:
        for index in range(16,256):
            colour=(index,0,0,0)
            pixels[0] = getColour(colour, NEO_BRIGHTNESS)
            pixels[1] = getColour(colour, NEO_BRIGHTNESS)
            pixels.write()
            time.sleep_ms(10)
            if mode!=1:
                break
        for index in range(256,16,-1):
            colour=(index,0,0,0)
            pixels[0] = getColour(colour, NEO_BRIGHTNESS)
            pixels[1] = getColour(colour, NEO_BRIGHTNESS)
            pixels.write()
            time.sleep_ms(10)
            if mode!=1:
                break

    # Mode 2: pulse green
    # Break out of loop if mode changes
    while mode==2:
        for index in range(16,256):
            colour=(0,index,0,0)
            pixels[0] = getColour(colour, NEO_BRIGHTNESS)
            pixels[1] = getColour(colour, NEO_BRIGHTNESS)
            pixels.write()
            time.sleep_ms(10)
            if mode!=2:
                break
        for index in range(256,16,-1):
            colour=(0,index,0,0)
            pixels[0] = getColour(colour, NEO_BRIGHTNESS)
            pixels[1] = getColour(colour, NEO_BRIGHTNESS)
            pixels.write()
            time.sleep_ms(10)
            if mode!=2:
                break

    # Mode 3: cycle through all colours
    # Break out of loop if mode changes
    while mode==3:
        for colour in COLOUR_WHEEL:    
            pixels[0] = getColour(colour, NEO_BRIGHTNESS)
            pixels[1] = getColour(colour, NEO_BRIGHTNESS)
            pixels.write()
            time.sleep(1)
            if mode!=3:
                break

    # Mode 4: cycle from green to red
    # Break out of loop if mode changes
    while mode==4:
        for colour in [COLOUR_GREEN,COLOUR_RED]:    
            pixels[0] = getColour(colour, NEO_BRIGHTNESS)
            pixels[1] = getColour(colour, NEO_BRIGHTNESS)
            pixels.write()
            time.sleep(1)
            if mode!=4:
                break

    # Mode 5: fade between red and green
    # Break out of loop if mode changes
    while mode==5:
        for index in range(0,256):
            colour=(index,255-index,0,0)
            pixels[0] = getColour(colour, NEO_BRIGHTNESS)
            pixels[1] = getColour(colour, NEO_BRIGHTNESS)
            pixels.write()
            time.sleep_ms(10)
            if mode!=5:
                break
        for index in range(0,256):
            colour=(255-index,index,0,0)
            pixels[0] = getColour(colour, NEO_BRIGHTNESS)
            pixels[1] = getColour(colour, NEO_BRIGHTNESS)
            pixels.write()
            time.sleep_ms(10)
            if mode!=5:
                break