#!/usr/bin/python

from ABE_ServoPi import PWM
import time
from ABE_helpers import ABEHelpers
from flask import Flask

limits = {
  "left-eye":(14, 200, 400),
  "right-eye":(15, 180, 360),
  "left-brow":(12, 260, 460),
  "right-brow":(13, 380, 560)
}

bus = ABEHelpers().get_smbus()
pwm = PWM(bus, 0x40)
pwm.set_pwm_freq(60)
pwm.output_enable()

app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/turn/<name>/<int:value>", methods=['GET'])
def turn_eye(name, value):
  servo_values = limits[name]
  pwm.set_pwm(servo_values[0], 0, value)
  return "Turn %s %d" % (name, value)

def scale_value():
  return

if __name__ == "__main__":
  app.run(host='0.0.0.0')
