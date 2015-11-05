import urllib2
import json
import time
import re
import emotions

__api_url = "http://192.168.140.16:5000"
__url_messages = "http://puhuvapaa.azurewebsites.net/api/message"

def __handle_emoticons(message):
  for emotion in re.findall(":(.*?):", message):
    if emotion == "angry":
      emotions.emotion_angry()
    if emotion == "disappointed":
      emotions.emotion_disapointed()
    if emotion == "neutral_face":
      emotions.emotion_neutral()
    if emotion == "thinking_face":
      emotions.emotion_thinking()
    if emotion == "stuck_out_tongue_winking_eye":
      emotions.emotion_crazy()
    if emotion == "stuck_out_tongue":
      emotions.emotion_crazy()
    if emotion == "stuck_out_tongue_closed_eyes":
      emotions.emotion_crazy()

def __speak(message):
  parsedMessage = re.sub(":.*?:","",message)
  url = "%s/%s/%s" % (__api_url, "suomi", parsedMessage)
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
