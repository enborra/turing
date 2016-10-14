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


    def __init__(self):
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
        if self._os_controller:
            self._get_service_status()

    def _services_stop_all(self):
        if self._os_controller:
            self._os_controller.stop_service()

    def _services_start_all(self):
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
