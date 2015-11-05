import urllib2

import time

__api_url = "http://192.168.140.16:5000"
__url_messages = "http://puhuvapaa.azurewebsites.net/api/message"

def __build_url(end):
  return "%s/%s" % (__api_url, end)

def left_brow(value):
  urllib2.urlopen(__build_url("turn/left-brow/%s" % value)).read()

def right_brow(value):
  urllib2.urlopen(__build_url("turn/right-brow/%s" % value)).read()

def emotion_happy():
  pass

def emotion_angry():
  right_brow(10)
  left_brow(90)

def emotion_disapointed():
  right_brow(90)
  left_brow(10)

def emotion_neutral():
  right_brow(50)
  left_brow(50)

def emotion_thinking():
  right_brow(40)
  left_brow(70)
  time.sleep(1)
  right_brow(50)
  left_brow(40)
  time.sleep(1)
  right_brow(40)
  left_brow(80)
  time.sleep(1)

def emotion_crazy():
  urllib2.urlopen(__build_url("crazy/5")).read()