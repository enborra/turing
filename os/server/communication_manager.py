import sys
import simplejson as json
import Queue
import threading
from flask import Flask, Response, render_template, g

from core.event_hook import EventHook


class CommunicationManager(object):
    _queue = None
    _queue_in = None
    _server_thread = None
    _app = None
    _config = {
        'server_host': '',
        'server_port': 0,
    }


    def __init__(self):
        self._app = Flask(__name__)

        self.on_request = EventHook()

        try:
            with open('os/config/core.json') as data_file:
                config_data = json.load(data_file)

                if config_data:
                    if 'servers' in config_data:
                        if 'web' in config_data['servers']:
                            if 'host' in config_data['servers']['web']:
                                self._config['server_host'] = config_data['servers']['web']['host']

                            if 'port' in config_data['servers']['web']:
                                self._config['server_port'] = config_data['servers']['web']['port']

        except Exception, e:
            print 'ERROR in CommunicationManager: ' + str(e)


    def start(self):
        self._queue = Queue.Queue(maxsize=1)
        self._queue_in = Queue.Queue(maxsize=1)

        self._server_thread = threading.Thread(target=self.serve_forever, args=(self._queue, self._queue_in))
        self._server_thread.setDaemon(True)
        self._server_thread.start()
        print "[TURING.OS.SERVER] Server running on %s and listening on %s" % (self._config['server_host'], self._config['server_port'])

    def stop(self):
        pass


    def update_state(self, state_obj):
        print 'QUEUE SIZE: ' + str(Queue.Queue.qsize(self._queue_in))

        if self._queue_in.full():
            self._queue_in.get()

        self._queue_in.put(state_obj)

        print '[TURING.OS.COMMS] Putting a request in queue for the web server thread.'

    def check(self):
        if self._queue.full():
            try:
                self.on_request.fire({
	        	    'path': self._queue.get()
        	    })
            except Exception, e:
                print '[TURING.OS.SERVER] Had trouble in queue processing: ' + str(e)


    def serve_forever(self, queue_out, queue_in):
        # _current_state = None


        @self._app.route('/', defaults={'path':''})
        @self._app.route('/<path:path>')
        def http_response(path):
            queue_out.put(str(path))

            if self._queue_in.full():
                g._current_state = queue_in.get()

                if not self._queue_in.full():
                    self._queue_in.put(g._current_state)

                print 'FOUND QUEUE REQUEST IN WEBSERVER: ' + str(g._current_state)

            resp = ''

            if '_current_state' in g:
                resp = str(g._current_state)


            try:
                resp_content = render_template('index.htm', currently_tracking_face=str(resp))
            except Exception, e:
                resp_content = str(e)

            return resp_content

        self._app.run(
            host=self._config['server_host'],
            port=self._config['server_port']
        )
