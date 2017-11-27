import serial
import time
import simplejson as json
from random import randint

from chasis import SerialMarshal


def _parse_motor_status(resp=None):
    print 'Motor is ' + resp['motor']['status']

def _parse_battery_status(resp=None):
    print 'Battery is ' + resp['battery']['status']

def _parse_motor_action(resp=None):
    print 'Motor is ' + resp['motor']['status']

def _parse_light_status(resp=None):
    print 'Light level is ' + resp['lux']['status']


s = SerialMarshal()
s.start()

i = 0

while True:
    s.update()

    if not s.is_response_pending():
        i = randint(1, 4)

        time.sleep(3)

        print '========================================================\n'

        if i == 1:
            s.request('motor_status', _parse_motor_status)

        elif i == 2:
            s.request('battery_status', _parse_battery_status)

        elif i == 3:
            s.request('action_drive_forward', _parse_motor_action)

        elif i == 4:
            s.request('light_status', _parse_light_status)
