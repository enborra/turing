import os
import subprocess

import simplejson as json


class BaseController(object):
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

    def stop_service(self):
        self._ensure_command_library_loaded()

    def start_service(self):
        self._ensure_command_library_loaded()

    def install_service(self):
        self._ensure_command_library_loaded()

    def display(self, msg):
        msg = self._colors['white'] + '  ' + msg

        for color in self._colors:
            msg = msg.replace('{{'+color.upper()+'}}', self._colors[color])

        print(msg)

    def update_source(self):
        self._ensure_command_library_loaded()

    def run_command(self, command_body=None):
        output = subprocess.check_output(command_body, shell=True)

        return output

    def _cleanup(self):
        print('')
