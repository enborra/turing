import os
import time
import sys
from PIL import Image
from PIL import ImageDraw
import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

from framework import Settings

from ui.faces.dali import DaliFace
from ui.faces.dali import Eye


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
    _face = None


    def __init__(self):
        pass

    def start(self):
        print('[DISPLAY] Starting.')

        self._disp = TFT.ILI9341( self._DC, rst=self._RST, spi=SPI.SpiDev(self._SPI_PORT, self._SPI_DEVICE, max_speed_hz=self._REFRESH_SPEED))
        self._disp.begin()

        self._image = Image.new('RGB', (240,320))
        self._renderer = ImageDraw.Draw(self._image)

        self._face = DaliFace(self._renderer)
        self._face.start()

    def update(self):
        # time.sleep(0.15)

        # draw = ImageDraw.Draw(self._image)
        # draw.ellipse((0, 0, 80, 80), fill=(255,255,255))
        # self._disp.display(self._image)

        self._renderer.rectangle((0,0,240,320), fill=(0,0,0))
        self._face.render()

        self._disp.display(self._image)
