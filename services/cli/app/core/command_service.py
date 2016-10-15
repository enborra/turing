import os
import platform
import subprocess
import click
import simplejson as json

from .controller_osx import OsxController
from .controller_raspberry_pi import RaspberryPiController


class CommandService(object):
    ENV_MACOS = 'osx'
    ENV_RASPBERRY_PI = 'raspberry_pi'
    ENV_UNKNOWN = 'unknown'

    _commands = None
    _os_controller = None

    _commands = None

    _colors = {
        'black':        '\033[0;30m',
        'red':          '\033[0;31m',
        'green':        '\033[0;32m',
        'brown':        '\033[0;33m',
        'blue':         '\033[0;34m',
        'purple':       '\033[0;35m',
        'cyan':         '\033[097;096m',
        'graylight':    '\033[0;37m',
        'darkgray':     '\033[1;30m',
        'redlight':     '\033[1;31m',
        'grenlight':    '\033[1;32m',
        'yellow':       '\033[0;93m',
        'bluelight':    '\033[1;34m',
        'purplelight':  '\033[1;35m',
        'cyanlight':    '\033[1;36m',
        'white':        '\033[0;97m',
    }

    def _ensure_command_library_loaded(self):
        if not self._commands:
            path_current_file = os.path.dirname(os.path.realpath(__file__)) + '/'

            with open(path_current_file + '../commands/command_library.json') as data_file:
                self._commands = json.load(data_file)


    def display(self, msg):
        msg = self._colors['white'] + '  ' + msg

        for color in self._colors:
            msg = msg.replace('{{'+color.upper()+'}}', self._colors[color])

        print(msg)


    def _cleanup(self):
        print('')


    def __init__(self):
        self._ensure_command_library_loaded()

        plat_name = platform.system().lower()
        plat_release = platform.release()
        plat_full_description = platform._syscmd_uname('-a')
        os_name = os.name.lower()

        if plat_name == 'linux':
            if 'raspberrypi' in plat_full_description.lower():
                self._env = self.ENV_RASPBERRY_PI

            else:
                self._env = self.ENV_UNKNOWN

        elif plat_name == 'darwin':
            self._env = self.ENV_MACOS

        # Instantiate controller for right platform

        if self._env == self.ENV_MACOS:
            self._os_controller = OsxController()

        elif self._env == self.ENV_RASPBERRY_PI:
            self._os_controller = RaspberryPiController()

    def get_system_status(self):
        self._ensure_command_library_loaded()

        if self._os_controller:
            for service_name in self._commands['services']:
                msg = self._os_controller.get_service_status(service_name)

                self.display(msg)

        self._cleanup()

    def _services_stop_all(self):
        self._ensure_command_library_loaded()

        if self._os_controller:
            for service_name in self._commands['services']:
                msg = self._os_controller.stop_service(service_name)

                self.display(msg)

        self._cleanup()

    def _services_start_all(self):
        self._ensure_command_library_loaded()

        if self._os_controller:
            for service_name in self._commands['services']:
                msg = self._os_controller.start_service(service_name)

                self.display(msg)

        self._cleanup()

    def _start_service(self):
        if self._os_controller:
            self._os_controller.start_service()

    def _get_service_status(self):
        if self._os_controller:
            self._os_controller.get_service_status()

    def _services_update_source(self):
        if self._os_controller:
            self._os_controller.update_source()

    def _services_install_all(self):
        if self._os_controller:
            self._os_controller.install_service()

    def get_env(self):
        run_env = self.ENV_UNKNOWN
