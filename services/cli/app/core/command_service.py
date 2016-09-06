import os
import platform
import subprocess
import click


class CommandService(object):

    ENV_MACOS = 'osx'
    ENV_RASPBERRY_PI = 'raspberry_pi'
    ENV_UNKNOWN = 'unknown'


    @classmethod
    def get_system_status(cls):
        env = cls.get_env()

        if env == cls.ENV_MACOS:
            print('Status of system services on this Mac:')
            print('-')

        elif env == cls.ENV_RASPBERRY_PI:
            print('Status of system services on this Raspberry Pi:')
            print('-')

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
