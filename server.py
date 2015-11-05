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
  index = limits[name]
  scaled = scale_value(name, value)
  pwm.set_pwm(index[0], 0, scaled)
  return "Turn %s %d Scaled value: %s" % (name, value, scaled)

@app.route("/servotest/")
def servotest()
  for i in [0, 100, 50]
    for key, value in limits.iteritems()
      address = value[0]
      pwm.set_pwm(address, 0, scale_value(key, i))
      time.sleep(1)

def scale_value(name, value):
  servo_values = limits[name]
  if value < 0:
    return servo_values[1]
  if value > 100:
    return servo_values[2]
  step = (servo_values[2] - servo_values[1]) / 100.0
  
  print "Step: %s, value: %s, Servo values: %s" % (step, value, servo_values)
  return int(round((step * value) + servo_values[1]))

if __name__ == "__main__":
  app.run(host='0.0.0.0')
