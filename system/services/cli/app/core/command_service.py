import os
import sys
import platform
import subprocess
import click
import simplejson as json

from .errors import *
from .controller_osx import OsxController
from .controller_raspberry_pi import RaspberryPiController


class CommandService(object):
    ENV_MACOS = 'osx'
    ENV_RASPBERRY_PI = 'raspberry_pi'
    ENV_UNKNOWN = 'unknown'

    _os_controller = None
    _path_services_system = os.path.dirname(os.path.realpath(__file__)) + '/../../../'
    _path_services_skill = os.path.dirname(os.path.realpath(__file__)) + '/../../../../../services/'
    _path_services_droid = os.path.dirname(os.path.realpath(__file__)) + '/../../../../../../droids/'
    _path_current_droid = None

    _storage_dir_path = '/etc/turing'
    _storage_global_config_file = 'config.json'


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

    def display(self, msg):
        msg = self._colors['white'] + '    ' + str(msg) + self._colors['white']

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
        plat_machine = platform.machine()
        plat_release = platform.release()
        plat_full_description = platform._syscmd_uname('-a')
        os_name = os.name.lower()

        if plat_name == 'linux':
            if 'raspberry' in plat_full_description.lower():
                self._env = self.ENV_RASPBERRY_PI

            elif plat_machine.startswith('arm'):
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
    # STORAGE METHODS
    # --------------------------------------------------------------------------

    def init_storage(self):
        store_exists = False
        store_init_success = True

        if os.path.isdir(self._storage_dir_path):
            store_exists = True

        else:
            try:
                self._os_controller.run_command('sudo mkdir %s' % (self._storage_dir_path))
                store_exists = True

            except Error as e:
                store_exists = False

        if not os.path.isdir(os.path.join(self._storage_dir_path, 'services')):
            self._os_controller.run_command('sudo mkdir %s' % os.path.join(self._storage_dir_path, 'services'))

        if not os.path.isdir(os.path.join(self._storage_dir_path, 'droids')):
            self._os_controller.run_command('sudo mkdir %s' % os.path.join(self._storage_dir_path, 'droids'))

        if store_exists:
            self.display('{{GREEN}}Validating filesystem: {{WHITE}}OS')

            try:
                if not os.path.isdir(self._get_config_value('service-path')):
                    self.display('{{YELLOW}}Validating filesystem: {{WHITE}}"service-path" directory does not actually exist.\n')
                    store_init_success = False

                if not os.path.isdir(self._get_config_value('droid-path')):
                    self.display('{{YELLOW}}Validating filesystem: {{WHITE}}"droid-path" directory does not actually exist.\n')
                    store_init_success = False

            except ConfigKeyNotFoundError:
                pass

        else:
            self.display('{{RED}}Had an issue accessing config storage on disk.{{WHITE}}')

        return store_init_success


    # --------------------------------------------------------------------------
    # CONFIG METHODS
    # --------------------------------------------------------------------------

    def _validate_system_config(self):
        is_config_valid = True

        try:
            cfg = self._get_config()

        except ConfigNotFoundError:
            self.display('{{YELLOW}}Config file not found. Cannot continue.')
            is_config_valid = False

        except ConfigEmptyError:
            self.display('{{YELLOW}}Config file empty. Cannot continue.')
            is_config_valid = False

        except ConfigMalformedError:
            self.display('{{YELLOW}}Config JSON is malformed. Cannot continue.')
            is_config_valid = False

        return is_config_valid

    def _validate_service_config(self, config_obj):
        current_run_file_name = None
        is_config_valid = True
        config_err_msg = None

        if config_obj is None:
            is_config_valid = False
            config_err_msg = 'config object supplied is null'

        else:
            if 'service-name' in config_obj:
                current_name = config_obj['service-name']

            else:
                is_config_valid = False
                config_err_msg = 'service.json missing "service-name" attribute'

        return (is_config_valid, config_err_msg)

    def _get_config_value(self, key):
        r = None

        try:
            cfg = self._get_config()
        except Exception:
            raise ConfigKeyNotFoundError()

        if key in cfg:
            r = cfg[key]
        else:
            raise ConfigKeyNotFoundError()

        return r

    def _set_config_value(self, key, new_val):
        try:
            cfg = self._get_config()
        except Exception:
            raise ConfigKeySetError()

        cfg[key] = new_val

        try:
            self._save_config(cfg)
        except ConfigSaveError as e:
            print(e)
            raise ConfigKeySetError()

    def _save_config(self, config_dict):
        self._elevate_privileges()

        config_file_path = '%s/%s' % (self._storage_dir_path, self._storage_global_config_file)

        try:
            with open(config_file_path, 'w') as f:
                json.dump(config_dict, f, indent=4, sort_keys=True)
        except:
            raise ConfigSaveError()


    def _get_config(self):
        config_file_path = '%s/%s' % (self._storage_dir_path, self._storage_global_config_file)
        config_file_raw = None
        config_file_contents = None

        if not os.path.isfile(config_file_path):
            raise ConfigNotFoundError()

        try:
            with open(config_file_path, 'r') as f:
                config_file_raw = f.read()

            config_file_contents = json.loads(config_file_raw)

        except:
            if len(str(config_file_raw)) <= 1:
                raise ConfigEmptyError()

            else:
                raise ConfigMalformedError()

        return config_file_contents


    # --------------------------------------------------------------------------
    # STATUS METHODS
    # --------------------------------------------------------------------------

    def get_system_status(self):
        self._elevate_privileges()

        self.display('{{WHITE}}OPERATING SYSTEM:')
        self.display('------------------------------------------------')
        self.display('{{GRAYDARK}}Filesystem: {{WHITE}}operational.')
        self._get_service_status_by_dir(self._path_services_system)
        self.display('')

        self.display('{{WHITE}}DROID:')
        self.display('------------------------------------------------')

        try:
            self._get_service_status(
                self._get_config_value('droid-path'),
                self._get_config_value('current-droid')
            )
        except ConfigKeyNotFoundError:
            self.display('{{GRAYDARK}}Droid not configured.')

        self.display('')
        self.display('')

        self.display('{{WHITE}}SKILL SERVICES:')
        self.display('------------------------------------------------')

        try:
            self._get_service_status_by_dir(self._get_config_value('service-path'))
        except ConfigKeyNotFoundError:
            self.display('{{GRAYDARK}}Skills not configured.')

        self.display('')


    def _get_service_status_by_dir(self, dir_services):
        service_dir_names = next(os.walk(dir_services))[1]

        if self._os_controller:
            if len(service_dir_names) == 0:
                msg = '{{YELLOW}}No services installed.{{WHITE}}'

                self.display(msg)

            else:
                for service_name in service_dir_names:
                    self._get_service_status(dir_services, service_name)

        self._cleanup()

    def _get_service_status(self, base_dir_path, service_name):
        path_service_config = os.path.join(
            base_dir_path,
            service_name,
            'service.json'
        )

        is_config_available = True
        is_config_valid = True
        cfg = None
        config_err_msg = None

        try:
            with open(path_service_config) as f:
                cfg = json.loads(f.read())

        except:
            is_config_available = False

        is_config_valid, config_err_msg = self._validate_service_config(cfg)

        if is_config_valid:
            is_always_on = False

            if 'always-on' in cfg:
                is_always_on = True

            if is_always_on:
                msg = '{{GRAYDARK}}Service always on: {{WHITE}}%s' % (service_name)

            else:
                msg = self._os_controller.get_service_status(service_name, cfg)

        else:
            msg = '{{RED}}%s: %s' % (config_err_msg, service_name)

        self.display(msg)


    def get_system_info(self):
        plat_name = platform.system().lower()
        plat_release = platform.release()
        plat_full_description = os.uname().nodename
        plat_machine = platform.machine()
        os_name = os.name.lower()

        self.display('Current running platform: %s, release number %s, (%s), on the %s OS' % (plat_name, plat_release, plat_full_description, plat_machine))

    # --------------------------------------------------------------------------
    # STOP METHODS
    # --------------------------------------------------------------------------

    def stop_all_services(self):
        self._elevate_privileges()

        # Stop core services in the /system/services/ directory

        self.display('{{WHITE}}OPERATING SYSTEM:')
        self.display('------------------------------------------------')
        self.display('{{GRAYDARK}}Filesystem: {{WHITE}}operational.')
        self._stop_services_by_dir(self._path_services_system)
        self.display('')

        self.display('{{WHITE}}DROID:')
        self.display('------------------------------------------------')

        try:
            self._stop_service(self._path_services_droid, self._get_config_value('current-droid'))
            self.display('{{RED}}Droid disabled: {{WHITE}}%s' % (self._get_config_value('current-droid')))
        except ConfigKeyNotFoundError:
            self.display('{{GRAYDARK}}Droid not configured.')

        self.display('')
        self.display('')

        # Stop skill services in the /services directory

        self.display('{{WHITE}}SKILL SERVICES:')
        self.display('------------------------------------------------')

        try:
            self.display(self._get_config_value('service-path'))
            self._stop_services_by_dir(self._get_config_value('service-path'))
        except ConfigKeyNotFoundError:
            self.display('{{GRAYDARK}}Services not configured.')

        self.display('')

    def _stop_service(self, base_dir_path, service_name):
        path_service_config = os.path.join(
            base_dir_path,
            service_name,
            'service.json'
        )

        is_config_available = True
        is_config_valid = True
        cfg = None
        config_err_msg = None

        try:
            with open(path_service_config) as f:
                cfg = json.loads(f.read())

        except Exception:
            is_config_available = False

        is_config_valid, config_err_msg = self._validate_service_config(cfg)

        if is_config_valid:
            is_always_on = False

            if 'always-on' in cfg:
                if cfg['always-on'] == True:
                    is_always_on = True

            if is_always_on:
                msg = '{{GRAYDARK}}Service always on: {{WHITE}}%s' % (service_name)

            else:
                msg = self._os_controller.stop_service(service_name, cfg)

        else:
            msg = '{{PURPLE}}%s:{{WHITE}} %s' % (config_err_msg, service_name)
            msg = base_dir_path + ' ::: ' + service_name

        self.display(msg)

    def _stop_services_by_dir(self, dir_services):
        service_dir_names = next(os.walk(dir_services))[1]

        if self._os_controller:
            if len(service_dir_names) == 0:
                msg = '{{YELLOW}}No services installed.{{WHITE}}'

                self.display(msg)

            else:
                for service_name in service_dir_names:
                    is_config_available = True
                    is_config_valid = True
                    cfg = None
                    config_err_msg = None

                    path_service_config = os.path.join(
                        dir_services,
                        service_name,
                        'service.json'
                    )

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
                            msg = '{{GRAYDARK}}Service always on: {{WHITE}}%s' % (service_name)

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
        self._elevate_privileges()

        # Start core services in the /system/services/ directory

        self.display('{{WHITE}}OPERATING SYSTEM:')
        self.display('------------------------------------------------')
        self.display('{{GRAYDARK}}Filesystem: {{WHITE}}operational.')
        self._start_services_by_dir(self._path_services_system)
        self.display('')

        self.display('{{WHITE}}DROID:')
        self.display('------------------------------------------------')
        self.display('{{GREEN}}Starting droid: {{WHITE}}%s' % (self._get_config_value('current-droid')))
        self._start_service(
            self._get_config_value('droid-path'),
            self._get_config_value('current-droid')
        )
        self.display('')
        self.display('')

        # Start skill services in the /services directory

        self.display('{{WHITE}}SKILL SERVICES:')
        self.display(self._path_services_skill)
        self.display('------------------------------------------------')
        self._start_services_by_dir(self._get_config_value('service-path'))
        self.display('')

    def _start_services_by_dir(self, dir_services):
        service_dir_names = next(os.walk(dir_services))[1]

        if self._os_controller:
            if len(service_dir_names) == 0:
                self.display('{{YELLOW}}No services installed.{{WHITE}}')

            else:
                for service_name in service_dir_names:
                    self._start_service(dir_services, service_name)

        self._cleanup()

    def _start_service(self, base_dir_path, service_name):
        path_service_config = os.path.join(
            base_dir_path,
            service_name,
            'service.json'
        )

        is_config_available = True
        is_config_valid = True
        cfg = None
        config_err_msg = None

        try:
            with open(path_service_config) as f:
                cfg = json.loads(f.read())

        except Exception:
            is_config_available = False

        is_config_valid, config_err_msg = self._validate_service_config(cfg)

        if is_config_valid:
            is_always_on = False

            if 'always-on' in cfg:
                if cfg['always-on'] == True:
                    is_always_on = True

            if is_always_on:
                msg = '{{GRAYDARK}}Service always on: {{WHITE}}%s' % (service_name)

            else:
                msg = self._os_controller.start_service(service_name, cfg)

        else:
            msg = '{{PURPLE}}%s:{{WHITE}} %s' % (config_err_msg, service_name)

        self.display(msg)


    # --------------------------------------------------------------------------
    # INSTALL METHODS
    # --------------------------------------------------------------------------

    def install_service(self, service_name):
        self._elevate_privileges()

        path_requested_service = os.path.join(
            self._storage_dir_path,
            self._get_config_value('service-path'),
            service_name
        )

        is_existing_path_in_storage = os.path.isdir(path_requested_service)
        is_existing_path_in_current_dir = os.path.isdir(service_name)

        if is_existing_path_in_current_dir:
            self.display('{{RED}}This directory already as a \'%s\' sub-directory.' % service_name)
        else:
            if is_existing_path_in_storage:
                self.display('{{RED}}This service is already registered locally with Turing, but is installed in a different location.')
            else:
                self.display('{{WHITE}}Downloading service..')
                # subprocess.check_output('cd $TURING_APP_DIR', shell=True)
                git_path = 'https://github.com/enborra/%s.git' % service_name

                hrm = subprocess.check_output(
                    'pwd',
                    stderr=subprocess.STDOUT,
                    shell=True
                )

                current_dir = hrm.decode('utf-8').rstrip()
                new_repo_dir = os.path.join(
                    current_dir,
                    service_name
                )

                subprocess.check_output('git clone %s --quiet' % git_path, shell=True)

                self.display('{{WHITE}}Registering repo with Turing locally...')

                subprocess.check_output(
                    'sudo ln -s %s %s' % (new_repo_dir, path_requested_service),
                    stderr=subprocess.STDOUT,
                    shell=True
                )

                self.display('{{WHITE}}Service registered successfully!')
                self.display('')

    def uninstall_service(self, service_name):
        self._elevate_privileges()

        path_requested_service = os.path.join(
            self._storage_dir_path,
            self._get_config_value('service-path'),
            service_name
        )

        is_existing_path_in_storage = os.path.isdir(path_requested_service)

        if is_existing_path_in_storage:
            self.display('{{WHITE}}Unregistering %s from Turing locally' % service_name)

            if path_requested_service.startswith('/etc/turing/'):
                subprocess.check_output(
                    'sudo rm -rf %s' % path_requested_service,
                    stderr=subprocess.STDOUT,
                    shell=True
                )
            else:
                self.display('{{RED}}Something went wrong during service uninstall.')

        else:
            self.display('{{WHITE}}%s is not locally registered with Turing')



    def install_all_services(self):
        self._elevate_privileges()

        self.display('{{WHITE}}OPERATING SYSTEM:')
        self.display('------------------------------------------------')
        can_proceed = self.init_storage()

        if not can_proceed:
            self.display('{{YELLOW}}Can\'t proceed. Stopping request.')

        else:
            # Install core services in the /system/services/ directory

            self._install_services_by_dir(self._path_services_system)
            self.display('')

            self.display('{{WHITE}}DROID:')
            self.display('------------------------------------------------')
            self.display('{{GREEN}}Installing droid: {{WHITE}}%s' % (self._get_config_value('current-droid')))
            self._install_service(
                self._get_config_value('droid-path'),
                self._get_config_value('current-droid')
            )
            self.display('')
            self.display('')

            # Install skill services in the /services directory

            self.display('{{WHITE}}SKILL SERVICES:')
            self.display('------------------------------------------------')
            self._install_services_by_dir(self._get_config_value('service-path'))
            self.display('')

    def _install_services_by_dir(self, dir_services):
        service_dir_names = next(os.walk(dir_services))[1]

        if self._os_controller:
            for service_name in service_dir_names:
                self._install_service(dir_services, service_name)

        self._cleanup()

    def _install_service(self, base_dir_path, service_name):
        path_service_config = os.path.join(
            base_dir_path,
            service_name,
            'service.json'
        )

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
                msg = '{{GRAYDARK}}Service always on: {{WHITE}}%s' % (service_name)
            else:
                msg = self._os_controller.install_service(service_name, base_dir_path, cfg)

        else:
            msg = '{{PURPLE}}%s:{{WHITE}} %s' % (config_err_msg, service_name)

        self.display(msg)


    # --------------------------------------------------------------------------
    # DROID UPDATE METHODS
    # --------------------------------------------------------------------------

    def set_active_droid(self, droid_name):
        self.display('{{YELLOW}}Booting droid: {{WHITE}}%s' % (droid_name))
        self.display('')

        self._set_config_value('current-droid', droid_name)



    # --------------------------------------------------------------------------
    # SOURCE UPDATE METHODS
    # --------------------------------------------------------------------------

    def _services_update_source(self):
        if self._os_controller:
            self._os_controller.update_source()

    def _elevate_privileges(self):
        try:
            self._os_controller.elevate_privileges()
        except PermissionError as e:
            self.display('{{YELLOW}}\n\n    Could not acquire elevated privileges. Can\'t proceed.\n\n{{WHITE}}')

            sys.exit()
