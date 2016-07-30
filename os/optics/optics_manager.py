import sys
import Queue
import threading

from optics.visual_detection_engine import VisualDetectionEngine
from core.event_hook import EventHook


class OpticsManager(object):
    _server_thread = None
    _queue = None


    def __init__(self):
        pass


    def start(self):
        self._queue = Queue.Queue(maxsize=1)

        print "[TURING.OS.OPTICS] Booted."

        engine = VisualDetectionEngine()
        engine.get_continuous_capture()
        # engine.track_continuous_object()


    def stop(self):
        pass


    def check(self):
        pass
