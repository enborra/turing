import time

from server.communication_manager import CommunicationManager
from optics.optics_manager import OpticsManager


_environment = None


class Client(object):
    _communicator = None
    _is_running = None
    _environment = None


    def __init__(self, environment=None):
        print '[TURING] Initing client...'

        if environment:
            if environment.lower() == 'simulated':
                self._environment = 'simulated'
            elif environment.lower() == 'onboard':
                self._environment = 'onboard'

        self._communicator = CommunicationManager('', 80)
        self._communicator.on_request += self.process_client_request

        self._optics = OpticsManager(
            environment=self._environment
        )


    def process_client_request(self, args):
        print 'catching web request.'

        print args

    def start(self):
        print '[TURING.OS] Starting..'

        is_running = True

        # if self._communicator:
        #     self._communicator.start()

        if self._optics:
            self._optics.start()

        while is_running:
            time.sleep(0.00001)

            # self._communicator.check()
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
