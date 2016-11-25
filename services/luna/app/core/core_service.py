import threading

import paho.mqtt.client as mqtt

from visual_detection_engine import VisualDetectionEngine


class CoreService(object):
    # Communications threading properties

    _comm_client = None
    _comm_delay = 0
    _thread_comms = None
    _thread_lock = None


    def __init__(self):
        pass

    def start(self):
        self._comm_client = mqtt.Client()
        self._comm_client.on_message = self._on_message
        self._comm_client.on_connect = self._on_connect
        self._comm_client.on_publish = self._on_publish
        self._comm_client.on_subscribe = self._on_subscribe

        self._thread_lock = threading.Lock()

        self._thread_comms = threading.Thread(target=self._start_thread_comms)
        self._thread_comms.setDaemon(True)
        self._thread_comms.start()

        engine = VisualDetectionEngine()
        engine.on_face_detected += self._handle_face_detection


        # FIND AND TRACK A FACE
        # Very buggy due to environmental noise. Even if
        # detection is successful, tracking likely to be sketchy and mis-focused
        # engine.track_continuous_object()

        # CONTINUOUS FACIAL DETECTION
        # Continuous loop of re-detection of existence of a face. Very reliable
        # for facial / eyes / smile detection
        engine.get_continuous_capture()

        # LOOP
        # Depends on database setting state of whether a face has been detected and
        # is being tracked.
        # engine.loop()

        # TRACK FACES
        # Haven't cleaned up, early test code.
        # engine.track_face()


    def _handle_face_detection(self):
        self._comm_client.publish('/system', 'detected_face')

    def _on_connect(self, client, userdata, flags, rc):
        pass

    def _on_message(self, client, userdata, msg):
        pass

    def _on_publish(self, mosq, obj, mid):
        pass

    def _on_subscribe(self, mosq, obj, mid, granted_qos):
        pass

    def _on_log(self, mosq, obj, level, string):
        pass

    def _connect_to_comms(self):
        print('connecting to comms system.')

        try:
            self._comm_client.connect('localhost', 1883, 60)

        except Exception, e:
            print('Could not connect to local Grand Central. Retrying in one second.')

            time.sleep(1)
            self._connect_to_comms()

    def _start_thread_comms(self):
        print('Comms thread started.')

        self._connect_to_comms()

        print('Connected to comms server.')

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
