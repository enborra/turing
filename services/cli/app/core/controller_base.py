import os
import subprocess

import simplejson as json


class BaseController(object):
    _commands = None


    def _ensure_command_library_loaded(self):
        if not self._commands:
            path_current_file = os.path.dirname(os.path.realpath(__file__)) + '/'

            with open(path_current_file + '../commands/command_library.json') as data_file:
                self._commands = json.load(data_file)

    def update_source(self):
        self._ensure_command_library_loaded()

    def run_command(self, command_body=None):
        output = subprocess.check_output(command_body, shell=True)

        return output
