import sys
import Queue
import threading

from optics.visual_detection_engine import VisualDetectionEngine
from core.event_hook import EventHook


class OpticsManager(object):
    _server_thread = None
    _queue = None
    _environment = None
    _engine = None


    def __init__(self, environment=None):
        self._environment = environment


    def start(self):
        self._queue = Queue.Queue(maxsize=1)

        print "[TURING.OS.OPTICS] Booted."

        self._engine = VisualDetectionEngine(
            environment=self._environment
        )

    def stop(self):
        pass


    def check(self):
        # engine.get_continuous_capture()
        # engine.track_continuous_object()
        # self._engine.track_face()
        self._engine.loop()
