
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
from ui.faces.clock import ClockFace

if platform.system().lower() == 'darwin':
    import pygame
    import Tkinter
    from PIL import ImageTk

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
    _comm_delay = 0

    root = None
    canvas = None




    def __init__(self):
        self._comm_client = mqtt.Client()
        self._comm_client.on_message = self._on_message
        self._comm_client.on_connect = self._on_connect
        self._comm_client.on_publish = self._on_publish
        self._comm_client.on_subscribe = self._on_subscribe

        if platform.system().lower() == 'darwin':
            self._environment = 'SIMULATED'

            # img = ImageTk.PhotoImage(self._image)
            # self._lbl.configure(image=img)
            # self._lbl.image = img

            # self._screen.mainloop()

        else:
            self._environment = 'ONBOARD'

    def start(self):
        self._connect_to_comms()

        if self._environment == 'ONBOARD':
            self._disp = TFT( self._DC, rst=self._RST, spi=SPI.SpiDev(self._SPI_PORT, self._SPI_DEVICE, max_speed_hz=self._REFRESH_SPEED))
            self._disp.begin()

        elif self._environment == 'SIMULATED':
            self._image = Image.new('RGB', (320,240), 'red')
            self._renderer = ImageDraw.Draw(self._image)
            # self._renderer.rectangle((0,0, 100,100), fill=(0,200,0), outline='blue')

            self._screen = Tkinter.Tk(className='Window')
            # self._canvas = Tkinter.Canvas(self._screen, bg='blue', height=250, width=300)
            self._screen.geometry("320x240")

            self._image_photo = ImageTk.PhotoImage(self._image)

            self._lbl = Tkinter.Label(self._screen, text='asdf', image=self._image_photo)
            self._lbl.pack(side='bottom', fill='both', expand='yes')

            # self._screen.mainloop()


        # self._image = Image.new('RGB', (240,320), (200,0,0))
        # self._renderer = ImageDraw.Draw(self._image)

        self._face = DaliFace(self._renderer)
        self._face = ClockFace(self._renderer)
        self._face.start()

        while True:
            self.update()

    def update(self):
        if self._comm_delay > 60:
            self._comm_client.loop()
            self._comm_delay = 0

        else:
            self._comm_delay += 1

        self._face.render()

        if self._environment == 'ONBOARD':
            self._disp.display(self._image)

        else:
            if self._image:
                # pass

                # pass
                # print 'IN VIRTUAL ENVIRONMENT.'
                #
                # self._renderer.point((0,0), fill='red')
                #
                # self._canvas.create_image(0,0, image=ImageTk.PhotoImage(self._image))
                #
                # self._canvas.update()
                # self._screen.update()

                # self._canvas.create_rectangle(50, 20, 150, 80, fill="#476042")

                # self._renderer.point((10,10), fill='red')
                #
                # img = ImageTk.PhotoImage(self._image)
                #
                # self._canvas.create_image(0, 0, image=img)
                # self._canvas.image = img

                self._renderer.rectangle((0,0, 100,100), fill=(0,10,0))
                self._phtimg = ImageTk.PhotoImage(self._image)
                self._lbl.config(image=self._phtimg)

                self._screen.update()




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

        # self._face.blink()

    def _on_publish(self, mosq, obj, mid):
        print 'mid: ' + str(mid)

    def _on_subscribe(self, mosq, obj, mid, granted_qos):
        print 'Subscribed: ' + str(mid) + ' ' + str(granted_qos)

    def _on_log(self, mosq, obj, level, string):
        print 'Log: ' + str(string)
