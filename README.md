# iot-hackday-puhuvapaa
TODO: FIX THIS BEFORE PRODUCTION!

# Installation

Install Flask (and its requirements)

  pip install Flask
  sudo apt-get install python-smbus

Install ServoPi library:

  git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
  export PYTHONPATH=${PYTHONPATH}:~/ABElectronics_Python_Libraries/ServoPi/

Or whatever folder contains that ServoPi thingy

Raspberry Pi Camera Board

1. Follow instructions to place the camera on the Pi.
2. Do the steps 2 and 3 from this tutorial: http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
3. Do the steps 7 and 8 from this tutorial: http://www.pyimagesearch.com/2015/02/23/install-opencv-and-python-on-your-raspberry-pi-2-and-b/
4. Do the steps 4 from http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
5. Time to code! Do step 5 from the aforementioned link.

# Usage

Run server:
> python server.py

## Motors and leds
HTTP GET:
http://localhost:5000/turn/{part}/{value}

Replace `{part}` with one of following values
* Motors:
  * `left-eye`
  * `right-eye`
  * `left-brow`
  * `right-brow`
* Leds:
  * `mouth1`
  * `mouth2`
  * `mouth3`

Replace `{value}` with integer between 0-100.

## Speech
HTTP GET:
http://localhost:500/speech/{content}

Replace `{content}` with wanted speech output
