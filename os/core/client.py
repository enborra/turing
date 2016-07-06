import time

from server.communication_manager import CommunicationManager


_environment = None


class Client(object):
    _communicator = None
    _is_running = None


    def __init__(self):
        print '[TURING] Initing client...'

        self._communicator = CommunicationManager('', 80)
        self._communicator.on_request += self.process_client_request


    def process_client_request(self, args):
        print 'catching web request.'

        print args

    def start(self):
        print '[TURING.OS] Starting..'

        is_running = True

        if self._communicator:
            self._communicator.start()

        while is_running:
            time.sleep(0.00001)

            self._communicator.check()

    def stop(self):
        if self._communicator:
            self._communicator.stop()

    def destroy(self):
        self._is_running = False

        if self._communicator:
            self._communicator.stop()
            self._communicator.destroy()
