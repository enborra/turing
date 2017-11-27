import time
import simplejson as json

from framework import BaseController
from server.communication_manager import CommunicationManager
from optics.optics_manager import OpticsManager
from chasis import ChasisController
from core import Settings
import rethinkdb as r
from storage import Storable


_environment = None


class Client(BaseController):
    _communicator = None
    _chasis = None

    _is_running = None
    _environment = None


    def __init__(self):
        self._class_output_id = 'turing.os'

        self.output('Booting')

        self._chasis = ChasisController()

        try:
            with open('os/config/core.json') as data_file:
                config_data = json.load(data_file)

                if config_data:
                    if 'environment' in config_data:
                        config_env = config_data['environment'].lower()

                        if config_env == Settings.ENVIRONMENT_SIMULATED:
                            self._environment = Settings.ENVIRONMENT_SIMULATED

                        elif config_env == Settings.ENVIRONMENT_ONBOARD:
                            self._environment = Settings.ENVIRONMENT_ONBOARD

                    if 'servers' in config_data:
                        if 'web' in config_data['servers']:
                            if 'host' in config_data['servers']['web']:
                                server_host = config_data['servers']['web']['host']

                            if 'port' in config_data['servers']['web']:
                                server_port = config_data['servers']['web']['port']

        except Exception, e:
            pass

        if not self._environment:
            self._environment = Settings.ENVIRONMENT_SIMULATED


        self._communicator = CommunicationManager()
        self._communicator.on_request += self.process_client_request

        self._optics = OpticsManager(
            environment=self._environment
        )


    def process_client_request(self, args):
        print 'catching web request.'

    def start(self):
        self.output('Starting up...')

        is_running = True

        if self._communicator:
            self._communicator.start()

        if self._optics:
            self._optics.start()

        i = 0

        s = Storable('turing')
        s.upsert('active_state', {'key': 'system_state', 'val': 'booting'})
        s.upsert('active_state', {'key': 'system_state', 'val': 'running'})

        while is_running:
            time.sleep(0.00001)

            self._communicator.check()
            self._optics.check()

    def stop(self):
        if self._communicator:
            self._communicator.stop()

        if self._optics:
            self._optics.stop()

    def destroy(self):
        self._is_running = False

        if self._communicator:
            self._communicator.stop()
            self._communicator.destroy()
