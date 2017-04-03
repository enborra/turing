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

    _os_controller = None
    _path_services_system = os.path.dirname(os.path.realpath(__file__)) + '/../../../'
    _path_services_skill = os.path.dirname(os.path.realpath(__file__)) + '/../../../../../services/'

    _colors = {
        'black':        '\033[0;30m',
        'red':          '\033[0;31m',
        'green':        '\033[0;32m',
        'brown':        '\033[0;33m',
        'blue':         '\033[0;34m',
        'purple':       '\033[0;35m',
        'cyan':         '\033[097;096m',
        'graylight':    '\033[0;37m',
        'graydark':     '\033[1;30m',
        'redlight':     '\033[1;31m',
        'greenlight':    '\033[1;32m',
        'yellow':       '\033[0;93m',
        'bluelight':    '\033[1;34m',
        'purplelight':  '\033[1;35m',
        'cyanlight':    '\033[1;36m',
        'white':        '\033[0;97m',
    }



    # --------------------------------------------------------------------------
    # UTILITY METHODS
    # --------------------------------------------------------------------------

    def get_env(self):
        run_env = self.ENV_UNKNOWN

    def _validate_service_config(self, config_obj):
        current_run_file_name = None
        is_config_valid = True
        config_err_msg = None

        # if 'install' in config_obj:
        #     if 'osx' in config_obj['install']:
        #         if (config_obj['install']['osx'] is not None) and (str(config_obj['install']['osx']) is not ''):
        #             current_run_file_name = config_obj['install']['osx']
        #
        #         else:
        #             is_config_valid = False
        #             config_err_msg = 'service.json "osx" install parameter empty'
        #
        #     else:
        #         is_config_valid = False
        #         config_err_msg = 'service.json "install" attribute collection missing "osx" property'
        #
        # else:
        #     is_config_valid = False
        #     config_err_msg = 'service.json missing "install" attribute collection'

        if 'service_name' in config_obj:
            current_name = config_obj['service_name']

        else:
            is_config_valid = False
            config_err_msg = 'service.json missing "service_name" attribute'

        return (is_config_valid, config_err_msg)

    def display(self, msg):
        msg = self._colors['white'] + '    ' + msg

        for color in self._colors:
            msg = msg.replace('{{'+color.upper()+'}}', self._colors[color])

        print(msg)

    def _cleanup(self):
        print('')


    # --------------------------------------------------------------------------
    # CORE CLASS METHODS
    # --------------------------------------------------------------------------

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


    # --------------------------------------------------------------------------
    # STATUS METHODS
    # --------------------------------------------------------------------------

    def get_system_status(self):
        self._os_controller.elevate_privaleges()

        self.display('{{WHITE}}CORE SERVICES:')
        self.display('------------------------------------------------')
        self._get_service_status(self._path_services_system)

        self.display('{{WHITE}}SKILL SERVICES:')
        self.display('------------------------------------------------')
        self._get_service_status(self._path_services_skill)

    def _get_service_status(self, dir_services):
        service_dir_names = next(os.walk(dir_services))[1]

        if self._os_controller:
            if len(service_dir_names) == 0:
                msg = '{{YELLOW}}No services installed.{{WHITE}}'

                self.display(msg)

            else:
                for service_name in service_dir_names:
                    path_service_config = dir_services + service_name + '/service.json'
                    is_config_available = True
                    is_config_valid = True
                    cfg = None
                    config_err_msg = None

                    try:
                        json_data_raw = open(path_service_config).read()
                        cfg = json.loads(json_data_raw)

                    except Exception:
                        is_config_available = False

                    is_config_valid, config_err_msg = self._validate_service_config(cfg)

                    if is_config_valid:
                        is_always_on = False

                        if 'always-on' in cfg:
                            if cfg['always-on'] == True:
                                is_always_on = True

                        if is_always_on:
                            msg = '{{GREEN}}Service always on: {{WHITE}}%s' % (service_name)

                        else:
                            msg = self._os_controller.get_service_status(service_name, cfg)

                    else:
                        msg = '{{RED}}%s: %s' % (config_err_msg, service_name)

                    self.display(msg)


        self._cleanup()


    # --------------------------------------------------------------------------
    # STOP METHODS
    # --------------------------------------------------------------------------

    def stop_all_services(self):
        # Stop core services in the /system/services/ directory

        self.display('{{WHITE}}CORE SERVICES:')
        self.display('------------------------------------------------')
        self._stop_services_by_dir(self._path_services_system)

        # Stop skill services in the /services directory

        self.display('{{WHITE}}SKILL SERVICES:')
        self.display('------------------------------------------------')
        self._stop_services_by_dir(self._path_services_skill)

    def _stop_services_by_dir(self, dir_services):
        service_dir_names = next(os.walk(dir_services))[1]

        if self._os_controller:
            for service_name in service_dir_names:
                path_service_config = dir_services + service_name + '/service.json'
                is_config_available = True
                is_config_valid = True
                cfg = None
                config_err_msg = None

                try:
                    json_data_raw = open(path_service_config).read()
                    cfg = json.loads(json_data_raw)

                except Exception:
                    is_config_available = False

                is_config_valid, config_err_msg = self._validate_service_config(cfg)

                if is_config_valid:
                    is_always_on = False

                    if 'always-on' in cfg:
                        if cfg['always-on'] == True:
                            is_always_on = True

                    if is_always_on:
                        msg = '{{GREEN}}Service always on: {{WHITE}}%s' % (service_name)

                    else:
                        msg = self._os_controller.stop_service(service_name, cfg)

                else:
                    msg = '{{PURPLE}}%s:{{WHITE}} %s' % (config_err_msg, service_name)

                self.display(msg)

        self._cleanup()


    # --------------------------------------------------------------------------
    # START METHODS
    # --------------------------------------------------------------------------

    def start_all_services(self):
        # Start core services in the /system/services/ directory

        self.display('{{WHITE}}CORE SERVICES:')
        self.display('------------------------------------------------')
        self._start_services_by_dir(self._path_services_system)

        # Start skill services in the /services directory

        self.display('{{WHITE}}SKILL SERVICES:')
        self.display('------------------------------------------------')
        self._start_services_by_dir(self._path_services_skill)

    def _start_services_by_dir(self, dir_services):
        service_dir_names = next(os.walk(dir_services))[1]

        if self._os_controller:
            for service_name in service_dir_names:
                path_service_config = dir_services + service_name + '/service.json'
                is_config_available = True
                is_config_valid = True
                cfg = None
                config_err_msg = None

                try:
                    json_data_raw = open(path_service_config).read()
                    cfg = json.loads(json_data_raw)

                except Exception:
                    is_config_available = False

                is_config_valid, config_err_msg = self._validate_service_config(cfg)

                if is_config_valid:
                    is_always_on = False

                    if 'always-on' in cfg:
                        if cfg['always-on'] == True:
                            is_always_on = True

                    if is_always_on:
                        msg = '{{GREEN}}Service always on: {{WHITE}}%s' % (service_name)

                    else:
                        msg = self._os_controller.start_service(service_name, cfg)

                else:
                    msg = '{{PURPLE}}%s:{{WHITE}} %s' % (config_err_msg, service_name)

                self.display(msg)

        self._cleanup()


    # --------------------------------------------------------------------------
    # INSTALL METHODS
    # --------------------------------------------------------------------------

    def install_all_services(self):
        # Install core services in the /system/services/ directory

        self.display('{{WHITE}}CORE SERVICES:')
        self.display('------------------------------------------------')
        self._install_services_by_dir(self._path_services_system)

        # Install skill services in the /services directory

        self.display('{{WHITE}}SKILL SERVICES:')
        self.display('------------------------------------------------')
        self._install_services_by_dir(self._path_services_skill)

    def _install_services_by_dir(self, dir_services):
        service_dir_names = next(os.walk(dir_services))[1]

        if self._os_controller:
            for service_name in service_dir_names:
                path_service_config = dir_services + service_name + '/service.json'
                is_config_available = True
                is_config_valid = True
                cfg = None
                config_err_msg = None

                try:
                    json_data_raw = open(path_service_config).read()
                    cfg = json.loads(json_data_raw)

                except Exception:
                    is_config_available = False

                is_config_valid, config_err_msg = self._validate_service_config(cfg)

                if is_config_valid:
                    msg = self._os_controller.install_service(service_name, dir_services, cfg)

                else:
                    msg = '{{PURPLE}}%s:{{WHITE}} %s' % (config_err_msg, service_name)

                self.display(msg)

        self._cleanup()


    # --------------------------------------------------------------------------
    # SOURCE UPDATE METHODS
    # --------------------------------------------------------------------------

    def _services_update_source(self):
        if self._os_controller:
            self._os_controller.update_source()
