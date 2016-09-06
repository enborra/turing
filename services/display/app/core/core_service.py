
import os, platform
import time
import sys

from PIL import Image
from PIL import ImageDraw

from libs import ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

import paho.mqtt.client as mqtt
from ui.faces.dali import DaliFace

if platform.system().lower() == 'darwin':
    print 'RUNNING ON OSX. CAN\'T RUN DISPLAY.'


class DisplayService(object):
    _environment = None
    _comm_client = None

    _canvas = None
    _DC = 18
    _RST = 23
    _SPI_PORT = 0
    _SPI_DEVICE = 0
    _REFRESH_SPEED = 64000000
    _image = None
    _renderer = None
    _disp = None
    _face = None


    def __init__(self):
        self._comm_client = mqtt.Client()
        self._comm_client.on_message = self._on_message
        self._comm_client.on_connect = self._on_connect
        self._comm_client.on_publish = self._on_publish
        self._comm_client.on_subscribe = self._on_subscribe

        if platform.system().lower() == 'darwin':
            self._environment = 'SIMULATED'
        else:
            self._environment = 'ONBOARD'

    def start(self):
        self._connect_to_comms()

        if self._environment == 'ONBOARD':
            self._disp = TFT( self._DC, rst=self._RST, spi=SPI.SpiDev(self._SPI_PORT, self._SPI_DEVICE, max_speed_hz=self._REFRESH_SPEED))
            self._disp.begin()

            self._image = Image.new('RGB', (240,320))
            self._renderer = ImageDraw.Draw(self._image)

        self._face = DaliFace(self._renderer)
        self._face.start()

        while True:
            self.update()

    _comm_delay = 0

    def update(self):
        if self._comm_delay > 60:
            self._comm_client.loop()
            self._comm_delay = 0

        else:
            self._comm_delay += 1

        self._face.render()
        if self._environment == 'ONBOARD':
            self._disp.display(self._image)




    def _connect_to_comms(self):
        try:
            self._comm_client.connect('localhost', 1883, 60)
        except Exception, e:
            time.sleep(1)
            self._connect_to_comms()


    def _on_connect(self, client, userdata, flags, rc):
        print "New connection: " + str(rc)

        self._comm_client.subscribe('system', 0)


    def _on_message(self, client, userdata, msg):
        print 'GOT MESSAGE (qos=' + str(msg.qos) + ', topic=' + str(msg.topic) + '): ' + str(msg.payload)

        self._face.blink()

    def _on_publish(self, mosq, obj, mid):
        print 'mid: ' + str(mid)

    def _on_subscribe(self, mosq, obj, mid, granted_qos):
        print 'Subscribed: ' + str(mid) + ' ' + str(granted_qos)

    def _on_log(self, mosq, obj, level, string):
        print 'Log: ' + str(string)
