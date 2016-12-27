import os
import json

from .controller_base import BaseController


class OsxController(BaseController):
    def __init__(self):
        self._path_current_file = os.path.dirname(os.path.realpath(__file__)) + '/'
        self._path_app_root = self._path_current_file + '../../'
        self._path_current_file = os.path.dirname(os.path.realpath(__file__)) + '/'
        self._path_app_root = self._path_current_file + '../../../'
        self._path_run_directory = '/Library/LaunchDaemons/'

    def stop_service(self, service_name, config_obj):
        is_enabled = True
        output_msg = None

        current_run_file_name = config_obj['install']['osx']
        current_name = config_obj['service_name']

        try:
            self.run_command('sudo launchctl list | grep %s' % current_name)
            self.run_command('sudo launchctl unload %s' % (self._path_run_directory + current_run_file_name))

            output_msg = '{{RED}}Stopped service:{{WHITE}} %s' % service_name

        except Exception as e:
            output_msg = '{{YELLOW}}Service was not running:{{WHITE}} %s' % service_name

        return output_msg

    def start_service(self, service_name=None, config_obj=None):
        is_enabled = True
        output_msg = None

        current_run_file_name = config_obj['install']['osx']
        current_name = config_obj['service_name']

        try:
            self.run_command('sudo launchctl list | grep %s' % current_name)

            output_msg = '{{YELLOW}}Service already running:{{WHITE}} %s' % current_name

        except Exception as e:
            self.run_command('sudo launchctl load %s' % (self._path_run_directory + current_run_file_name))

            output_msg = '{{GREEN}}Started service:{{WHITE}} %s' % service_name

        return output_msg

    def get_service_status(self, service_name, config_obj):
        output_msg = ''
        current_name = config_obj['service_name']

        try:
            self.run_command('sudo launchctl list | grep %s' % current_name)
            output_msg = '{{GREEN}}Service running: {{WHITE}}%s' % service_name

        except Exception as e:
            output_msg = '{{GRAYDARK}}Service not running: {{WHITE}}%s' % service_name

        return output_msg

    def update_source(self):
        output_msg = None

        self.stop_service()
        super().update_source()

        output_msg = '{{GREEN}}Pulling new code down from origin/master{{GRAYDARK}}'

        self.run_command('cd $TURING_APP_DIR')
        self.run_command('git pull origin master')

        output_msg += '{{WHITE}}'
        output_msg += '\n' + self.start_service()

        return output_msg

    def install_service(self, service_name, config_obj):
        is_running = False
        output_msg = ''

        run_file_name = config_obj['install']['osx']
        current_name = config_obj['service_name']
        path_service_source_file = self._path_app_root + service_name + '/' + self._path_source_root + run_file_name
        path_service_run_file = self._path_run_root + run_file_name

        # If the service is running, stop it

        try:
            self.run_command('sudo launchctl list | grep %s' % current_name)
            output_msg = '{{YELLOW}}Service already installed:{{WHITE}} %s' % current_name

        except Exception as e:
            is_running = False

        if not is_stopped:
            try:
                self.run_command('sudo launchctl list | grep %s' % current_name)
                self.run_command('sudo launchctl unload %s' % current_name)
                is_running = False

            except Exception:
                is_running = True

        if not is_running:
            # Now install new service and load it

            self.run_command('sudo ln -sf %s %s' % (path_service_source_file, path_service_run_file))
            self.run_command('sudo chown root:wheel %s' % path_service_run_file)
            self.run_command('sudo launchctl load %s' % path_service_run_file)

            output_msg = '{{GREEN}}Installing service:{{WHITE}} %s' % service_name

        else:
            output_msg = '{{RED}}Had a problem stopping %s' % current_name

        return output_msg
