#!/usr/bin/python

from ABE_ServoPi import PWM
import time
from ABE_helpers import ABEHelpers
from flask import Flask
import random
# enable calling speech functions
import subprocess
import oracle

limits = {
  "left-eye":(14, 200, 400),
  "right-eye":(15, 180, 360),
  "left-brow":(12, 260, 460),
  "right-brow":(13, 380, 560),
  "mouth1":(6, 0, 4000),
  "mouth2":(7, 0, 4000),
  "mouth3":(8, 0, 4000)
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

@app.route("/move/<name>/<int:start>/<int:end>/<int:speed>", methods=['GET'])
def move(name, start, end, speed):
  index = limits[name]
  if start < end:
    direction = 1
    steps = end - start
  else:
    direction = -1
    steps = start - end
  i = 0
  currentStep = start
  
  while i < steps:
    angle = scale_value(name, currentStep)
    pwm.set_pwm(index[0], 0, angle)
    i = i + 1
    currentStep = currentStep + direction
    time.sleep(0.01 * speed)
  return "ready"

@app.route("/multimove/<names>/<int:start>/<int:end>/<int:speed>", methods=['GET'])
def move_multiple(names, start, end, speed):
  splitted = names.split(",")

  if start < end:
    direction = 1
    steps = end - start
  else:
    direction = -1
    steps = start - end
  i = 0
  currentStep = start

  while i < steps:
    for name in splitted:
      index = limits[name]
      angle = scale_value(name, currentStep)
      pwm.set_pwm(index[0], 0, angle)
    i = i + 1
    currentStep = currentStep + direction
    time.sleep(0.01 * speed)

  return "OK"

@app.route("/speech/<phrase>", methods=['GET'])
def speech(phrase):
  subprocess.Popen(["espeak", phrase])
  return phrase

@app.route("/suomi/<phrase>", methods=['GET'])
def finnish(phrase):
  subprocess.Popen(["espeak", "-vfi", phrase])
  return phrase

@app.route("/oracle/<question>", methods=['GET'])
def ask_oracle(question):
  answer = oracle.ask_from_oracle(question)
  output = "%s %s" % (question, answer)
  subprocess.Popen(["espeak", "-vfi", output]);
  return answer

@app.route("/crazy/<int:howLong>", methods=['GET'])
def crazy(howLong):
  if howLong > 10:
    howLong = 10
  print "run for %d seconds" % howLong
  endTime = time.time() + howLong
  print "time: %s" % endTime
  while time.time() < endTime:
    for key, value in limits.iteritems():
      address = value[0]
      randomValue = random.randint(0, 100)
      pwm.set_pwm(address, 0, scale_value(key, randomValue))
    time.sleep(0.1)
  return "sane again"

@app.route("/servotest/<int:delay>", methods=['GET'])
def servotest(delay):
  for i in [0, 100, 50]:
    for key, value in limits.iteritems():
      address = value[0]
      pwm.set_pwm(address, 0, scale_value(key, i))
    time.sleep(1)
  return "servo test finished"

def scale_value(name, value):
  servo_values = limits[name]
  if value < 0:
    return servo_values[1]
  if value > 100:
    return servo_values[2]
  step = (servo_values[2] - servo_values[1]) / 100.0
  
  #print "Step: %s, value: %s, Servo values: %s" % (step, value, servo_values)
  return int(round((step * value) + servo_values[1]))

if __name__ == "__main__":
  app.run(host='0.0.0.0')
