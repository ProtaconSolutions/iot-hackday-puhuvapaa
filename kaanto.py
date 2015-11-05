#!/usr/bin/python

from ABE_ServoPi import PWM
import time
from ABE_helpers import ABEHelpers

"""

Servo testi

"""

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()

pwm = PWM(bus, 0x40)

# Set PWM frequency to 60 Hz
pwm.set_pwm_freq(60)
pwm.output_enable()

port = input("Anna portti: ")
print ("portiksi asetettu: " + port)

while (True):
  # Move servo on port 0 between three points
  dir = input("Anna asento: ")
  print ("uusi asento: " + dir)
  pwm.set_pwm(port, 0, dir)
  time.sleep(1)

