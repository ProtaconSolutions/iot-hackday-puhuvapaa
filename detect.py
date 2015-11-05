import io
import os
import picamera
import urllib2
import time
from datetime import datetime
from PIL import Image

camera = picamera.PiCamera()

# mainframeUrl = "http://192.168.140.16:5000/"
mainframeUrl = "http://127.0.0.1:5000/"

difference = 20
pixels = 120

width = 1280
height = 960

def compare():
   camera.resolution = (100, 75)
   stream = io.BytesIO()
   camera.capture(stream, 'jpeg')
   stream.seek(0)
   im = Image.open(stream)
   buffer = im.load()
   stream.close()
   return im, buffer

image1, buffer1 = compare()

timestamp = time.time()

while (True):

   image2, buffer2 = compare()

   pixLeft = 0
   pixMiddle = 0
   pixRight = 0


   changedpixels = 0
   for x in xrange(0, 100):
      for y in xrange(0, 75):
         pixdiff = abs(buffer1[x,y][1] - buffer2[x,y][1])
         if pixdiff > difference:
            changedpixels += 1
	    if x < 40:
		pixLeft += 1
	    elif x < 60:
		pixMiddle += 1
	    else:
		pixRight += 1

   if changedpixels > pixels:
      timestamp = time.time()
      # print "Left : %d" % pixLeft # 100
      # print "Mid  : %d" % pixMiddle
      # print "Right: %d" % pixRight # 0
      direction = ''
      if pixLeft > 50 and pixMiddle > 50 and pixRight > 50: 
        if pixLeft > pixMiddle:
           if pixLeft > pixRight:
              direction = 'left'
           else:
              direction = 'right'
        else:
           if pixMiddle > pixRight:
              direction = 'middle'
           else:
              direction = 'right'
        #print direction
	if direction == 'left':
       	  urllib2.urlopen(mainframeUrl + "turn/left-eye/100")
       	  urllib2.urlopen(mainframeUrl + "turn/right-eye/100")
	elif direction == 'right':
       	  urllib2.urlopen(mainframeUrl + "turn/left-eye/0")
       	  urllib2.urlopen(mainframeUrl + "turn/right-eye/0")
	elif direction == 'middle':
       	  urllib2.urlopen(mainframeUrl + "turn/left-eye/50")
       	  urllib2.urlopen(mainframeUrl + "turn/right-eye/50")

   image1 = image2
   buffer1 = buffer2
