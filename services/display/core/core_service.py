
import sys
import Queue
import threading
from flask import Flask, Response, render_template



class DisplayService(object):
    _queue = None
    _server_thread = None
    _app = None
    _config = {
        'server_host': '',
        'server_port': 0
    }


    def __init__(self):
        self._app = Flask(__name__)

        # self.on_request = EventHook()

    def start(self):
        self._queue = Queue.Queue(maxsize=1)

        self._server_thread = threading.Thread(target=self.serve_forever, args=(self._queue))
        self._server_thread.setDaemon(True)
        self._server_thread.start()

        print 'Started server.'

        while True:
            import time

            time.sleep(1)

            print '.'


    def serve_forever(self, queue_out):
            @self._app.route('/')
            def http_response():
                return Response('asdf')
