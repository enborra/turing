import os
import platform
import subprocess
import click
import simplejson as json


class CommandService(object):

    ENV_MACOS = 'osx'
    ENV_RASPBERRY_PI = 'raspberry_pi'
    ENV_UNKNOWN = 'unknown'

    _commands = None


    @classmethod
    def get_system_status(cls):
        env = cls.get_env()

        if env == cls.ENV_MACOS:
            print('Status of system services on this Mac:')
            print('-')

            cls._services_stop_all()

        elif env == cls.ENV_RASPBERRY_PI:
            print('Status of system services on this Raspberry Pi:')
            print('-')


    @classmethod
    def _services_stop_all(cls):
        cls._ensure_command_library_loaded()

        path_current_file = os.path.dirname(os.path.realpath(__file__)) + '/'
        path_app_root = path_current_file + '../../'
        path_source_root = cls._commands['file_locations']['services_source_directory']

        path_run_directory = cls._commands['file_locations']['services_run_directory_osx']

        for service_name in cls._commands['services']:
            current_service_config = cls._commands['services'][service_name]
            current_service_name = current_service_config['name']
            current_service_run_file_name = current_service_config['install']['osx']

            # If the service is running, stop it

            try:
                cls.run_command('sudo launchctl list | grep %s' % current_service_name)
                cls.run_command('sudo launchctl unload %s' % (path_run_directory + current_service_run_file_name))

                print('Stopped service: %s' % current_service_name)

            except Exception:
                print('Service was not running: %s' % current_service_name)


    @classmethod
    def _services_install_all(cls):
        cls._ensure_command_library_loaded()

        # print cls._commands

        # for service_config in cls._commands['services']:
        #     print service_config

            # output = cls.run_command('sudo launchctl unload '+service_name)
            # output = cls.run_command('sudo ln -sf ')

        path_current_file = os.path.dirname(os.path.realpath(__file__)) + '/'
        path_app_root = path_current_file + '../../../'
        path_source_root = cls._commands['file_locations']['services_source_directory']
        path_run_root = cls._commands['file_locations']['services_run_directory_osx']


        for service_name in cls._commands['services']:
            current_service_config = cls._commands['services'][service_name]
            current_service_name = current_service_config['name']
            current_service_run_file_name = current_service_config['install']['osx']

            path_service_source_file = path_app_root + service_name + '/' + path_source_root + current_service_run_file_name
            path_service_run_file = path_run_root + current_service_run_file_name


            print 'Installing service: %s' % current_service_run_file_name

            # If the service is running, stop it

            try:
                cls.run_command('sudo launchctl list | grep %s' % current_service_name)
                cls.run_command('sudo launchctl unload %s' % path_service_run_file)

            except Exception:
                pass

            cls.run_command('sudo ln -sf %s %s' % (path_service_source_file, path_service_run_file))
            cls.run_command('sudo chown root:wheel %s' % path_service_run_file)
            cls.run_command('sudo launchctl load %s' % path_service_run_file)


    @classmethod
    def _ensure_command_library_loaded(cls):
        if not cls._commands:
            with open('/Users/andres/projects/turing/services/cli/app/commands/command_library.json') as data_file:
                cls._commands = json.load(data_file)


    @classmethod
    def run_command(cls, command_body=None):
        output = subprocess.check_output(command_body, shell=True)

        return output

    @classmethod
    def run_script(cls, file_name=None):
        cli_path = os.path.dirname(os.path.realpath(__file__))
        core_sys_path = cli_path + '/commands/'

        try:
            sys_boot_path = core_sys_path + file_name
            bash_cmd = 'sh %s' % sys_boot_path

            output = subprocess.check_output(bash_cmd, shell=True)
            print(output)

        except Exception, e:
            click.echo('[TURING.CLI] Error: %s' % str(e))


    @classmethod
    def get_env(cls):
        run_env = cls.ENV_UNKNOWN

        plat_name = platform.system().lower()
        plat_release = platform.release()
        plat_full_description = platform._syscmd_uname('-a')
        os_name = os.name.lower()

        if plat_name == 'linux':
            if 'raspberrypi' in plat_full_description.lower():
                run_env = cls.ENV_RASPBERRY_PI

            else:
                run_env = cls.ENV_UNKNOWN

        elif plat_name == 'darwin':
            run_env = cls.ENV_MACOS

        return run_env
