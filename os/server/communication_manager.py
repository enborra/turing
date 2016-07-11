import sys
import Queue
import threading
from flask import Flask, Response

from core.event_hook import EventHook


class CommunicationManager(object):
    _queue = None
    _server_thread = None
    _app = Flask(__name__)


    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.on_request = EventHook()


    def start(self):
        self._queue = Queue.Queue(maxsize=1)

        self._server_thread = threading.Thread(target=self.serve_forever, args=(self._queue,))
        self._server_thread.setDaemon(True)
        self._server_thread.start()
        print "[TURING.OS.SERVER] Server running on %s and listening on %d" % (self.host, self.port)

    def stop(self):
        pass


    def check(self):
        if self._queue.full():
            try:
                self.on_request.fire({
	        	    'path': self._queue.get()
        	    })
            except Exception, e:
                print '[TURING.OS.SERVER] Had trouble in queue processing: ' + str(e)


    def serve_forever(self, q):

        @self._app.route('/', defaults={'path': ''})
        @self._app.route('/<path:path>')
        def http_response(path):
            q.put(str(path))

            return Response('', 200)

        self._app.run(
            host=self.host,
            port=self.port
        )
