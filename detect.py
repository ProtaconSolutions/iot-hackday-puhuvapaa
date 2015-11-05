import io
import os
import picamera
import urllib2
import time
from datetime import datetime
from time import sleep 
from PIL import Image

camera = picamera.PiCamera()

# mainframeUrl = "http://192.168.140.16:5000/"
mainframeUrl = "http://127.0.0.1:5000/"

difference = 20
pixels = 120

width = 800 #1280
height = 600 #960

def compare():
   camera.resolution = (100, 75)
   stream = io.BytesIO()
   camera.capture(stream, 'jpeg')
   stream.seek(0)
   im = Image.open(stream)
   buffer = im.load()
   stream.close()
   return im, buffer

def maxIndex(pixValues):
  maxValue = max(pixValues)
  for i in range(len(pixValues)):
    if maxValue == pixValues[i]:
      return i   
  return -1	      

image1, buffer1 = compare()

timestamp = time.time()

pixAngle = [0, 20, 35, 50, 70, 85, 100] 
oldMaxIdx = -1;

while (True):

   image2, buffer2 = compare()

   pixArray = [15, 30, 45, 60, 75, 90, 100]
   pixValues = [0,0,0,0,0,0,0]

   changedpixels = 0
   for x in xrange(0, 100):
      for y in xrange(0, 75):
         pixdiff = abs(buffer1[x,y][1] - buffer2[x,y][1])
         if pixdiff > difference:
            changedpixels += 1
            for i in range(len(pixArray)):
              if pixArray[i] > x:
                pixValues[i] += 1
		break 

   if changedpixels > pixels:
      timestamp = time.time()
      for i in range(len(pixArray)):
        print "%d - %d" % (pixArray[i], pixValues[i])

      maxIdx = maxIndex(pixValues)

      if (oldMaxIdx == -1 or oldMaxIdx != maxIdx):
        angle = pixAngle[maxIdx]
#       print "max index: %d" % maxIdx

        urllib2.urlopen(mainframeUrl + "turn/left-eye/%d" % angle )
        urllib2.urlopen(mainframeUrl + "turn/right-eye/%d" % angle)
        oldMaxIdx = maxIdx
   
   image1 = image2
   buffer1 = buffer2
