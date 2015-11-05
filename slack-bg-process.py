import urllib2
import urllib
import json
import time

__url_speak = "http://localhost:5000/suomi/"
__url_messages = "http://puhuvapaa.azurewebsites.net/api/message"

def __speak(message):
  url = "%s%s" % (__url_speak, message)
  req = urllib2.Request(url.replace(" ", "%20"))
  urllib2.urlopen(req).read()

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
