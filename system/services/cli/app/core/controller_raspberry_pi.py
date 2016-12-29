import os
import json

from .controller_base import BaseController


class RaspberryPiController(BaseController):
    def __init__(self):
        self._path_run_directory = '/lib/systemd/system/'
        self._path_current_file = os.path.dirname(os.path.realpath(__file__)) + '/'
        self._path_app_root = self._path_current_file + '../../../'

    def stop_service(self, service_name, config_obj):
        output_msg = None

        current_name = config_obj['service_name']
        current_run_file_name = config_obj['install']['raspberry_pi']

        # If the service is running, stop it

        try:
            self.run_command('sudo systemctl status %s' % (self._path_run_directory + current_run_file_name))
            self.run_command('sudo systemctl stop %s' % (self._path_run_directory + current_run_file_name))

            output_msg = '{{RED}}Stopped service:{{WHITE}} %s' % current_name

        except Exception as e:
            output_msg = '{{YELLOW}}Service was not running:{{WHITE}} %s' % current_name

        return output_msg

    def start_service(self, service_name, config_obj):
        output_msg = None

        current_name = config_obj['service_name']
        current_run_file_name = config_obj['install']['raspberry_pi']

        try:
            self.run_command('sudo systemctl status %s' % current_name)

            output_msg = '{{YELLOW}}Service already running:{{WHITE}} %s' % current_name

        except Exception as e:
            self.run_command('sudo systemctl start %s' % (self._path_run_directory + current_run_file_name))

            output_msg = '{{GREEN}}Service started:{{WHITE}} %s' % service_name

        return output_msg

    def get_service_status(self, service_name, config_obj):
        is_enabled = True
        output_msg = None

        current_name = config_obj['service_name']
        current_run_file_name = config_obj['install']['raspberry_pi']

        try:
            self.run_command('sudo systemctl status ' + current_run_file_name)
            output_msg = '{{GREEN}}Service running: {{WHITE}}%s' % service_name

        except Exception as e:
            output_msg = '{{RED}}Service not running: {{WHITE}}%s' % service_name

        if not is_enabled:
            output_msg += ' {{DARKGRAY}}(disabled)'

        return output_msg

    def update_source(self):
        super().update_source()
        self.stop_service()

        output_msg = '{{GREEN}}Pulling new code down from origin/master{{DARKGRAY}}'

        subprocess.check_output('cd $TURING_APP_DIR', shell=True)
        subprocess.check_output('git pull origin master', shell=True)
        subprocess.check_output('cd /home/pi/projects/turing/services/central_station', shell=True)

        output_msg += '{{WHITE}}'

        output_msg += '\n' + self.start_service()

        return output_msg

    def install_service(self, service_name, dir_services, config_obj):
        output_msg = ''

        current_service_name = config_obj['service_name']
        current_service_run_file_name = config_obj['install']['raspberry_pi']

        path_service_source_file = dir_services + service_name + '/' + current_service_run_file_name
        path_service_run_file = self._path_run_directory + current_service_run_file_name

        output_msg += '{{GREEN}}Installing service:{{WHITE}} %s\n' % current_service_run_file_name

        # If the service is running, stop it

        try:
            is_active = self.run_command('systemctl is-active %s >/dev/null 2>&1 && echo 1 || echo 0' % current_service_run_file_name)

            if str(is_active) == '1':
                self.run_command('sudo systemctl stop %s' % current_service_run_file_name)
                self.run_command('sudo systemctl disable %s' % current_service_run_file_name)

            print('successfully uninstalled.')

        except Exception as e:
            output_msg += 'Had a problem uninstalling service: %s\n' % str(e)

        # Now install new service and load it

        self.run_command('sudo cp -f %s %s' % (path_service_source_file, path_service_run_file))
        self.run_command('sudo chmod +x %s' % path_service_run_file)
        self.run_command('sudo systemctl enable %s' % current_service_run_file_name)
        self.run_command('sudo systemctl start %s' % current_service_run_file_name)

        return output_msg
