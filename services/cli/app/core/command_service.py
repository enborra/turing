import os
import platform
import subprocess
import click
import simplejson as json

from .controller_osx import OsxController


class CommandService(object):
    ENV_MACOS = 'osx'
    ENV_RASPBERRY_PI = 'raspberry_pi'
    ENV_UNKNOWN = 'unknown'

    _commands = None
    _os_controller = None


    def __init__(self):
        self.get_env()

        if self._env == self.ENV_MACOS:
            self._os_controller = OsxController()
        elif self._env == self.ENV_RASPBERRY_PI:
            self._os_controller = None

    def get_system_status(self):
        if self._env == self.ENV_MACOS:
            print('Status of system services on this Mac:')
            print('-')

            self._services_stop_all()

        elif self._env == self.ENV_RASPBERRY_PI:
            print('Status of system services on this Raspberry Pi:')
            print('-')


    def _services_stop_all(self):
        if self._os_controller:
            self._os_controller.stop_service()

    def _services_install_all(self):
        if self._os_controller:
            self._os_controller.install_service()

    def get_env(self):
        run_env = self.ENV_UNKNOWN

        plat_name = platform.system().lower()
        plat_release = platform.release()
        plat_full_description = platform._syscmd_uname('-a')
        os_name = os.name.lower()

        if plat_name == 'linux':
            if 'raspberrypi' in plat_full_description.lower():
                run_env = self.ENV_RASPBERRY_PI

            else:
                run_env = self.ENV_UNKNOWN

        elif plat_name == 'darwin':
            run_env = self.ENV_MACOS

        self._env = run_env
