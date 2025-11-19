#--------------------------------------
#    ___  ___  _ ____          
#   / _ \/ _ \(_) __/__  __ __ 
#  / , _/ ___/ /\ \/ _ \/ // / 
# /_/|_/_/  /_/___/ .__/\_, /  
#                /_/   /___/   
#
#  RP2040 Servo Calibration
#
# Author : Matt Hawkins
# Date   : 19/11/2025
#
# Connect Servo to GPIO14
# Connect Button 1 to GPIO4 (reduces Servo Duty)
# Connect Button 2 to GPIO5 (increases Servo Duty)
# Connect Button 3 to GPIO6 (increases Servo Duty)
# Connect Button 4 to GPIO7 (increases Servo Duty)
#
# duty_u16 is value 0-65535
#  500us = 1638
# 1000us = 3277
# 1500us = 4915
# 2000us = 6554
# 2500us = 8192
#
# Button 1 - Reduce duty
# Button 2 - Increase duty
# Button 3 - Maximum Duty
# Button 4 - Minimum Duty
#
# If when using Button 1 or 2 the duty exceeds the Min/Max values
# the servo will be set to the mid position.
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
import machine
import time
import neopixel

def getColour(baseColour,brightness=20):
    # Take a colour tuple and adjust the values using the brightness value
    brightness=brightness/100
    if brightness>0 and brightness<1:
        adjustedColour=tuple([int(x*brightness) for x in baseColour])
    else:
        adjustedColour=baseColour
    return adjustedColour

def callback1(button):
    global debounce_time1,current_duty
    if (time.ticks_ms()-debounce_time1) > 500:
        current_duty=current_duty-SRV_DUTY_INC
        if current_duty<SRV_MIN_DUTY:
          current_duty=SRV_MID_DUTY
          onboardLed.fill(getColour(COLOUR_RED,LED_BRIGHTNESS))
          onboardLed.write()
          time.sleep(0.5)
        servo.duty_u16(current_duty)
        print("Current Duty : "+str(current_duty))
        debounce_time1=time.ticks_ms()

def callback2(button):
    global debounce_time2,current_duty
    if (time.ticks_ms()-debounce_time2) > 500:
        current_duty=current_duty+SRV_DUTY_INC
        if current_duty>SRV_MAX_DUTY:
          current_duty=SRV_MID_DUTY
          onboardLed.fill(getColour(COLOUR_RED,LED_BRIGHTNESS))
          onboardLed.write()
          time.sleep(0.5)
        servo.duty_u16(current_duty)
        print("Current Duty : "+str(current_duty))
        debounce_time2=time.ticks_ms()

def callback3(button):
    global debounce_time3,current_duty
    if (time.ticks_ms()-debounce_time3) > 500:
        servo.duty_u16(SRV_MAX_DUTY)
        current_duty = SRV_MAX_DUTY
        print("Current Duty : "+str(current_duty))
        debounce_time3=time.ticks_ms()

def callback4(button):
    global debounce_time4,current_duty
    if (time.ticks_ms()-debounce_time4) > 500:
        servo.duty_u16(SRV_MIN_DUTY)
        current_duty = SRV_MIN_DUTY
        print("Current Duty : "+str(current_duty))
        debounce_time4=time.ticks_ms()

# Define hardware values
LED_PIN=16              # Set pin number for onboard LED
BTN1_PIN=4              # Momentary switch GP4
BTN2_PIN=5              # Momentary switch GP5
BTN3_PIN=6              # Momentary switch GP6
BTN4_PIN=7              # Momentary switch GP7

SRV_PIN=14               # Servo
SRV_FRQ=50
SRV_DUTY_INC=100

# duty_u16 is value 0-65535
#  500us = 1638
# 1000us = 3277
# 1500us = 4915
# 2000us = 6554
# 2500us = 8192

# SG90
SRV_MIN_DUTY=1638
SRV_MAX_DUTY=8192

# MG996R
SRV_MIN_DUTY=3277
SRV_MAX_DUTY=6554

# Get Servo centre
SRV_MID_DUTY=int((SRV_MIN_DUTY+SRV_MAX_DUTY)/2)

# Set brightness as a percentage
LED_BRIGHTNESS=1

# Define some colours
COLOUR_RED=(255,0,0,0)
COLOUR_GREEN=(0,255,0,0)
COLOUR_BLUE=(0,0,255,0)

# Setup onboard LED
onboardLed = neopixel.NeoPixel(machine.Pin(LED_PIN), 1)

# Setup Servo
servo = machine.PWM(machine.Pin(SRV_PIN))
servo.freq(SRV_FRQ)
current_duty = SRV_MID_DUTY
servo.duty_u16(current_duty)

# Setup buttons using interupt with debouncing
debounce_time1 = 0
debounce_time2 = 0
debounce_time3 = 0
debounce_time4 = 0
button1 = machine.Pin(BTN1_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(BTN2_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
button1.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback1)
button2.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback2)

button3 = machine.Pin(BTN3_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
button4 = machine.Pin(BTN4_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
button3.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback3)
button4.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback4)

# Turn on/off onboard LED
onboardLed.fill(getColour(COLOUR_BLUE,LED_BRIGHTNESS))
onboardLed.write()  

print("Current Duty : "+str(current_duty))

# Main loop
while True:
    onboardLed.fill(getColour(COLOUR_BLUE,LED_BRIGHTNESS))
    onboardLed.write()  
    time.sleep(1)
    onboardLed.fill(getColour(COLOUR_GREEN,LED_BRIGHTNESS))
    onboardLed.write()
    time.sleep(1)
