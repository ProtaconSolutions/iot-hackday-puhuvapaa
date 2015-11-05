import sys
import socket
import urllib2

__timeout = 5
__server = "http://192.168.140.16:5000/"

def __build_url(end):
  return "%s%s" % (__server, end)

def happy():
  urllib2.urlopen(__build_url("turn/left-eye/100")).read()
  urllib2.urlopen(__build_url("turn/right-eye/0")).read()
  urllib2.urlopen(__build_url("turn/left-brow/50")).read()
  urllib2.urlopen(__build_url("turn/right-brow/50")).read()
  urllib2.urlopen(__build_url("speech/im_happy")).read()

def main(argv):
  print "Emotions test program"
  print "Arguments: %s" % argv

  socket.setdefaulttimeout(__timeout)

  for argument in argv:
    if argument == "happy":
      happy()

if __name__ == "__main__":
  main(sys.argv[1:])
