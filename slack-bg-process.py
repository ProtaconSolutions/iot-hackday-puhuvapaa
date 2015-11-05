import urllib2
import json
import time
import re

__api_url = "http://192.168.140.16:5000"
__url_messages = "http://puhuvapaa.azurewebsites.net/api/message"

def __build_url(end):
  return "%s/%s" % (__api_url, end)

def left_brow(value):
  urllib2.urlopen(__build_url("turn/left-brow/%s" % value)).read()

def right_brow(value):
  urllib2.urlopen(__build_url("turn/right-brow/%s" % value)).read()

def __handle_emoticons(message):
  for emotion in re.findall(":(.*?):", message):
    if emotion == "angry":
      right_brow(10)
      left_brow(90)
    if emotion == "disappointed":
      right_brow(90)
      left_brow(10)
    if emotion == "neutral_face":
      right_brow(50)
      left_brow(50)

def __speak(message):
  url = "%s/%s/%s" % (__api_url, "suomi", re.sub(":.*?:","",message))
  req = urllib2.Request(url.replace(" ", "%20").encode("utf-8"))
  urllib2.urlopen(req).read()
  __handle_emoticons(message)


def read_messages():
  req = urllib2.Request(__url_messages)
  messages = json.loads(urllib2.urlopen(req).read())
  for message in messages:
    __speak(message["Content"])

def main():
  read_messages()

if __name__ == "__main__":
  print "Kuunnellaan slakkia kunnes kuollaan."
  while 1:
    main()
    time.sleep(4.0)
