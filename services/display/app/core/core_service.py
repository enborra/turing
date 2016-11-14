import time
import threading

import paho.mqtt.client as mqtt

from core.framework import MachineSystem
from core.framework import Foreman
from core.framework import Interface
from core.ui.faces.clock import ClockFace
from core.ui.faces.dali import DaliFace

if MachineSystem.is_simulated():
    import Tkinter
    from PIL import ImageTk


class DisplayService(object):
    # Communications threading properties

    _comm_client = None
    _comm_delay = 0
    _thread_comms = None
    _thread_lock = None

    _dummy_variable = 0

    # Ui properties

    _face = None


    def __init__(self):
        self._comm_client = mqtt.Client()
        self._comm_client.on_message = self._on_message
        self._comm_client.on_connect = self._on_connect
        self._comm_client.on_publish = self._on_publish
        self._comm_client.on_subscribe = self._on_subscribe

        Foreman.initialize()

    def start(self):
        Foreman.debug_msg('Starting CoreService')

        Foreman.start()

        Foreman.on_second += self._process_second
        Foreman.on_frame += self._process_frame
        Foreman.on_second_half += self._process_second_half

        self._thread_lock = threading.Lock()

        self._thread_comms = threading.Thread(target=self._start_thread_comms)
        self._thread_comms.setDaemon(True)
        self._thread_comms.start()

        # Load initial display face

        self._load_face('clock')

        while True:
            self.update()

    def update(self):
        Foreman.update()

    def _load_face(self, face_name):
        if face_name == 'dali':
            if self._face:
                self._face.stop()

            self._face = DaliFace(
                ui_width_size=Interface.UI_SIZE_LARGE,
                ui_height_size=Interface.UI_SIZE_LARGE
            )

            self._face.start()

        elif face_name == 'clock':
            if self._face:
                self._face.stop()

            self._face = ClockFace(
                ui_width_size=Interface.UI_SIZE_LARGE,
                ui_height_size=Interface.UI_SIZE_LARGE
            )

            self._face.start()

    def _start_thread_comms(self):
        print 'Comms thread started.'

        self._connect_to_comms()

        print 'Connected to comms server.'

        while True:
            self._thread_lock.acquire()

            try:
                if self._comm_delay > 2000:
                    self._comm_client.loop()
                    self._comm_delay = 0

                else:
                    self._comm_delay += 1

            finally:
                self._thread_lock.release()

    def _process_second(self, args=None):
        # Foreman.debug_msg('event: half-second elapsed, frame rate %s' % Foreman.get_frame_rate())
        # Foreman.debug_msg('event: second elapsed.')
        pass

    def _process_second_half(self, args=None):
        # Foreman.debug_msg('event: half-second elapsed, frame rate %s' % Foreman.get_frame_rate())
        pass

    def _process_frame(self, args=None):
        img = self._face.render()
        img = img.rotate(-90, expand=True)

        Foreman.draw(img)

    def _connect_to_comms(self):
        print 'connecting to comms system.'

        try:
            self._comm_client.connect('localhost', 1883, 60)
            print('Connected to local Grand Central.')
        except Exception, e:
            print('Could not connect to local Grand Central. Retrying..')

            time.sleep(1)
            self._connect_to_comms()

    def _on_connect(self, client, userdata, flags, rc):
        print("New connection: " + str(rc))

        self._comm_client.subscribe('system', 0)

    def _on_message(self, client, userdata, msg):
        print 'GOT MESSAGE (qos=' + str(msg.qos) + ', topic=' + str(msg.topic) + '): ' + str(msg.payload)

        req_msg = str(msg.payload)

        if req_msg == 'clock':
            self._load_face('clock')

        elif req_msg == 'dali':
            self._load_face('dali')

        import sys
        sys.stdout.flush()

    def _on_publish(self, mosq, obj, mid):
        print 'mid: ' + str(mid)

    def _on_subscribe(self, mosq, obj, mid, granted_qos):
        print 'Subscribed: ' + str(mid) + ' ' + str(granted_qos)

    def _on_log(self, mosq, obj, level, string):
        print 'Log: ' + str(string)
