import sys
import simplejson as json
import Queue
import threading
from flask import Flask, Response, render_template, g

from core import BaseController
from core.event_hook import EventHook
import rethinkdb as r

from storage import Storable


class CommunicationManager(BaseController):
    _queue = None
    _queue_in = None
    _server_thread = None
    _app = None
    _config = {
        'server_host': '',
        'server_port': 0,
    }


    def __init__(self):
        BaseController.__init__(self)

        self._class_output_id = 'turing.os.server'
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
            self.output('ERROR: ' + str(e))


    def start(self):
        self._queue = Queue.Queue(maxsize=1)
        self._queue_in = Queue.Queue(maxsize=1)

        self._server_thread = threading.Thread(target=self.serve_forever, args=(self._queue, self._queue_in))
        self._server_thread.setDaemon(True)
        self._server_thread.start()

        self.output('Server running on %s and listening on %s' % (self._config['server_host'], self._config['server_port']))

    def stop(self):
        pass


    def check(self):
        if self._queue.full():
            try:
                self.on_request.fire({
	        	    'path': self._queue.get()
        	    })
            except Exception, e:
                self.output('Had trouble in queue processing: ' + str(e))


    def serve_forever(self, queue_out, queue_in):
        @self._app.route('/')
        def http_response():
            queue_out.put('asdf')

            system_state = None

            try:
                s = Storable('turing')
                res = s.get('active_state', {'key': 'system_state'})

                conn = r.connect('localhost', 28015)
                system_state_obj = r.db('turing').table('active_state').filter({'key': 'system_state'}).run(conn)

                for doc in system_state_obj:
                    system_state = doc['val']

            except Exception, e:
                self.output('errortown: ' + str(e))

            try:
                resp_content = render_template('index.htm', currently_tracking_face=str(system_state))

            except Exception, e:
                resp_content = str(e)

            return resp_content

        @self._app.route('/sleep')
        def http_response_sleep():
            resp = 'goodnight.'

            try:
                s = Storable('turing')
                s.upsert('active_state', {'key': 'system_state', 'val': 'sleeping'})

            except Exception, e:
                self.output('ERROR: ' + str(e))
                resp = 'Error: ' + str(e)

            return Response(resp)

        @self._app.route('/wake')
        def http_response_wake():
            resp = 'good morning!'

            try:
                s = Storable('turing')
                s.upsert('active_state', {'key': 'system_state', 'val': 'running'})

            except Exception, e:
                self.output('ERROR: ' + str(e))

                resp = 'Error: ' + str(e)

            return Response(resp)

        @self._app.route('/api/camera')
        def http_response_api_camera():
            resp = ''

            try:
                s = Storable('turing')
                resp = s.get('active_state', {'key': 'system_state'})

                for doc in resp:
                    resp = str(doc['val'])

                conn = r.connect('localhost', 28015)
                system_state_obj = r.db('turing').table('active_state').filter({'key': 'system_state'}).run(conn)

                for doc in system_state_obj:
                    system_state = doc['val']

            except Exception, e:
                self.output('ERROR: ' + str(e))

            return Response(resp)

        self._app.run(
            host=self._config['server_host'],
            port=self._config['server_port']
        )
