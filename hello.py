#!/usr/bin/python

from ABE_ServoPi import PWM
import time
from ABE_helpers import ABEHelpers
from flask import Flask

bus = ABEHelpers().get_smbus()
pwm = PWM(bus, 0x40)
pwm.set_pwn_freq(60)
pwm.output_enable()

app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/turn-eye/<int:eye_index>/<int:degree>", methods=['GET'])
def turn_eye(eye_index, degree):
  pwm_set_pwm(15, 0, degree)
  return "Kaanto %d %d" % (degree, eye_index)

if __name__ == "__main__":
  app.run(host='0.0.0.0')
