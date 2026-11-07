#--------------------------------------
#    ___  ___  _ ____          
#   / _ \/ _ \(_) __/__  __ __ 
#  / , _/ ___/ /\ \/ _ \/ // / 
# /_/|_/_/  /_/___/ .__/\_, /  
#                /_/   /___/   
#
#  RP2040 Servo Tester
#
# Allows a servo to be tested by turning a potentiometer. Can be
# used to test the range of movement and determine suitable
# duty vaues for another piece of software.
#
# Author : Matt Hawkins
# Date   : 07/11/2026
#
# Connect Servo to GPIO29
# Connect Potentiometer to GPIO26
# Connect Screen to GPIO2 (SDA), GPIO3 (SCL)
#
# duty_u16 is value 0-65535
# duty_u16 = (duty_ms/20)*65535
# duty_ms = (duty_u16/65535)*20
#  500us = 0.50ms = 1638   -90   degrees 
# 1000us = 1.00ms = 3277   -45   degrees
# 1250us = 1.25ms = 4096   -22.5 degrees
# 1500us = 1.50ms = 4915     0   degrees
# 1750us = 1.75ms = 5734   +22.5 degrees
# 2000us = 2.00ms = 6554   +45   degrees
# 2500us = 2.50ms = 8192   +90   degrees
#
# ADC
# 0V   = 0
# 3.3V = 65535
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
import ssd1306

# Servo
SRV_PIN=29               # Servo
SRV_FRQ=50

# ADC
ADC_PIN=26
ADC_MIN_OFFSET=320
ADC_MAX_OFFSET=0
ADC_RANGE=(65535-ADC_MAX_OFFSET)-(0+ADC_MIN_OFFSET)

# OLED Screen
OLED_SDA=2
OLED_SCL=3
I2C_CHANNEL=1

# Servo
SRV_MIN_DUTY=1638
SRV_MAX_DUTY=8192
SRV_RANGE=SRV_MAX_DUTY-SRV_MIN_DUTY

print("ADC Range   : ",ADC_RANGE)
print("Servo Range : ",SRV_RANGE)

# Get Servo centre
SRV_MID_DUTY=int((SRV_MIN_DUTY+SRV_MAX_DUTY)/2)

# Setup Screen
i2c=machine.I2C(I2C_CHANNEL,sda=machine.Pin(OLED_SDA), scl=machine.Pin(OLED_SCL),freq=200000)
oled=ssd1306.SSD1306_I2C(128,64,i2c,addr=0x3C)

# Setup Servo
servo = machine.PWM(machine.Pin(SRV_PIN))
servo.freq(SRV_FRQ)
current_duty = SRV_MID_DUTY
servo.duty_u16(current_duty)

dial= machine.ADC(ADC_PIN)

while True:
    
    # Read ADC
    dial_value=dial.read_u16()
    time.sleep_ms(1)
    dial_value=dial.read_u16()
    
    servo_duty_u16=(((dial_value-ADC_MIN_OFFSET+ADC_MAX_OFFSET)/ADC_RANGE)*SRV_RANGE)+SRV_MIN_DUTY 
    servo_duty_ms = (servo_duty_u16/65535)*20

    servo_duty_u16=int(servo_duty_u16)
    servo.duty_u16(servo_duty_u16)

    # Update OLED screen
    oled.fill(0)
    oled.text('Dial     : '+str(int(dial_value)), 1, 1, 1)
    oled.text('Servo U16: '+str(servo_duty_u16), 1, 16, 1)
    oled.text('Servo ms : '+str(servo_duty_ms), 1, 32, 1)
    oled.show()
    
    time.sleep_ms(300)