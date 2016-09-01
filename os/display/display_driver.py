import os
import time
import sys
from PIL import Image
from PIL import ImageDraw
import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

from framework import Settings

from ui import Eye


class DisplayDriver(object):
    _environment = Settings.ENVIRONMENT_SIMULATED
    _canvas = None
    _DC = 18
    _RST = 23
    _SPI_PORT = 0
    _SPI_DEVICE = 0
    _REFRESH_SPEED = 64000000
    _image = None
    _disp = None


    _eye_left = None
    _eye_right = None


    def __init__(self):
        pass

    def start(self):
        print('[DISPLAY] Starting.')

        self._disp = TFT.ILI9341( self._DC, rst=self._RST, spi=SPI.SpiDev(self._SPI_PORT, self._SPI_DEVICE, max_speed_hz=self._REFRESH_SPEED))
        self._disp.begin()

        print('Loading image...')

        image_path = os.path.dirname(__file__) + '/eyes.jpg'

        self._image = Image.open(image_path)
        self._image = self._image.rotate(270).resize((240, 320))

        self._eye_left = Eye(self._image, 50, 100)
        self._eye_right = Eye(self._image, 200, 100)

    def update(self):
        # self._disp.clear((0, 0, 0))
        # time.sleep(0.15)
        #
        # draw = ImageDraw.Draw(self._image)
        # draw.ellipse((0, 0, 80, 80), fill=(255,255,255))
        # self._disp.display(self._image)
        # draw = None


        # time.sleep(4)
        # self._disp.clear((0, 0, 0))
        # self._disp.display()

        self._image = Image.new('RGB', (240,320))
        self._eye_left.canvas = self._image
        self._eye_right.canvas = self._image


        self._eye_left.x += 1

        self._eye_left.render()
        self._eye_right.render()

        self._disp.clear((0,0,0))
        self._disp.display(self._image)
        # self.disp.display()
