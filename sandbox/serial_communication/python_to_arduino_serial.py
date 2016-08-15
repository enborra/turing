import serial
import time

ser = serial.Serial('/dev/cu.usbmodem1411', 115200)

i = 0
pending_response = False

while 1:
    if not pending_response:
        print 'Writing to serial: ' + str(i)

        ser.write(str(i) + '\n')
        pending_response = True

        # time.sleep(2)

    else:
        if ser.inWaiting() > 0:
            resp = str(ser.readline())

            print 'Response from device: ' + resp

            if( resp == '200' ):
                print "FOUND A 200 OK."
            elif resp == 'r2d2':
                print 'FOUND AN R2D2 RESPONSE.'

            pending_response = False

            # print 'checking'


            i = i + 1
