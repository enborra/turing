import os
import subprocess

import simplejson as json


class BaseController(object):
    def update_source(self):
        pass

    def run_command(self, command_body=None):
        output = subprocess.check_output(command_body, shell=True)

        return output

    def install_service(self):
        pass
