import serial
import simplejson as json
from random import randint



class SerialMarshal(object):
    _connection = None
    _pending_response = False
    _callback_queue = {}


    def __init__(self):
        pass

    def start(self):
        self._connection = serial.Serial('/dev/cu.usbmodem1411', 115200)
        self._pending_response = False

    def request(self, msg, callback_method=None):
        request_id = randint(1000,9999)
        request_payload = str(request_id) + ':' + msg + '\n'

        print 'Writing to serial: ' + request_payload

        if callback_method:
            self._callback_queue[request_id] = callback_method

        self._connection.write(request_payload)
        self._pending_response = True

    def stop(self):
        self._connection.close()

    def is_response_pending(self):
        return self._pending_response

    def update(self):
        resp = None
        resp_obj = None

        if self._connection.inWaiting() > 0:
            resp = str(self._connection.readline())

            try:
                resp_obj = json.loads(resp)

                if resp_obj:
                    if 'rid' in resp_obj:
                        rid = int(resp_obj['rid'])

                        if rid in self._callback_queue:
                            self._callback_queue[rid](resp_obj)

                    if 'status' in resp_obj:
                        print 'FOUND A CHASIS NOTIFICATION.'

                        resp_obj = None

            except ValueError:
                # Response was not JSON
                resp_obj = None

        if resp_obj:
            self._pending_response = False
