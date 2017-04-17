import os
import subprocess

import simplejson as json


class BaseController(object):
    def update_source(self):
        pass

    def run_command(self, command_body=None):
        output = None

        output = subprocess.check_output(
            command_body,
            stderr=subprocess.STDOUT,
            shell=True
        )

        return output.decode('UTF-8')

    def install_service(self):
        pass

    def elevate_privaleges(self):
        pass
