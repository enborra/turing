import serial
import time
import simplejson as json


ser = serial.Serial('/dev/cu.usbmodem1411', 115200)

i = 0
pending_response = False

while 1:
    if not pending_response:
        print 'Writing to serial: ' + str(i)

        if str(i).startswith('1'):
            ser.write('motor_status\n')
            pending_response = True

        elif str(i).startswith('2'):
            ser.write('battery_status\n')
            pending_response = True

        elif str(i).startswith('3'):
            ser.write('action_drive_forward\n')
            pending_response = True

        else:
            ser.write(str(i) + '\n')
            pending_response = True

    else:
        if ser.inWaiting() > 0:
            resp = str(ser.readline())

            print 'Response from device: ' + resp

            if( resp == '200' ):
                print "FOUND A 200 OK."
            elif resp == 'r2d2':
                print 'FOUND AN R2D2 RESPONSE.'

            else:
                try:
                    resp_obj = json.loads(resp)

                    print 'Motor status is: ' + resp_obj['motor']['status']

                except Exception, e:
                    print 'poof.'

            pending_response = False

            # print 'checking'


            i = i + 1

            time.sleep(2)
