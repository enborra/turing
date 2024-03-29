import os
import json

from .controller_base import BaseController


class OsxController(BaseController):
    def __init__(self):
        self._path_run_directory = '/Library/LaunchDaemons/'
        self._path_current_file = os.path.dirname(os.path.realpath(__file__)) + '/'
        self._path_app_root = self._path_current_file + '../../../../../services/'

    def stop_service(self, service_name, config_obj):
        output_msg = None

        current_run_file_name = config_obj['install']['osx']
        current_name = config_obj['service-name']

        # If the service is running, stop it

        try:
            self.run_command('sudo launchctl list | grep %s' % current_name)
            self.run_command('sudo launchctl unload %s' % (self._path_run_directory + current_run_file_name))

            output_msg = '{{RED}}Stopped service:{{WHITE}} %s' % service_name

        except Exception as e:
            output_msg = '{{YELLOW}}Service was not running:{{WHITE}} %s' % service_name

        return output_msg

    def start_service(self, service_name=None, config_obj=None):
        output_msg = None

        current_name = config_obj['service-name']
        current_run_file_name = config_obj['install']['osx']

        try:
            self.run_command('sudo launchctl list | grep %s' % current_name)

            output_msg = '{{YELLOW}}Service already running:{{WHITE}} %s' % current_name

        except Exception as e:
            self.run_command('sudo launchctl load %s' % (self._path_run_directory + current_run_file_name))

            output_msg = '{{GREEN}}Started service:{{WHITE}} %s' % service_name

        return output_msg

    def get_service_status(self, service_name, config_obj):
        output_msg = ''
        current_name = config_obj['service-name']

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

    def install_service(self, service_name, dir_services, config_obj):
        is_running = False
        output_msg = ''

        run_file_name = config_obj['install']['osx']
        current_name = config_obj['service-name']

        path_service_source_file = os.path.join(
            dir_services,
            service_name,
            'system',
            run_file_name
        )

        path_service_run_file = os.path.join(
            self._path_run_directory,
            run_file_name
        )

        # If the service is running, stop it

        try:
            self.run_command('sudo launchctl list | grep %s' % current_name)
            is_running = True

        except PermissionError as e:
            print('{{RED}}Elevated permissions required.{{WHITE}}')

        except Exception as e:
            is_running = False

        if is_running:
            try:
                self.run_command('sudo launchctl unload %s' % path_service_run_file)
                is_running = False

            except Exception:
                is_running = True

        if not is_running:
            is_install_success = True

            # Now install new service and load it, starting with symlink install.

            cmd_resp = self.run_command('sudo ln -sf %s %s' % (path_service_source_file, path_service_run_file))

            # Set permissions of service run file

            cmd_resp = self.run_command('sudo chown root:wheel %s' % path_service_run_file)

            # Now that service is installed, boot it up

            cmd_resp = self.run_command('sudo launchctl load %s' % path_service_run_file)

            if cmd_resp != '':
                if 'service already loaded' in cmd_resp:
                    is_install_success = False
                    output_msg = '{{YELLOW}}System reported service already running: {{WHITE}}%s' % current_name

                else:
                    is_install_success = False
                    output_msg = '{{RED}}Service failed to install (%s): %s' % (service_name, cmd_resp)

            if is_install_success:
                output_msg = '{{GREEN}}Installing service:{{WHITE}} %s' % service_name

        else:
            output_msg = '{{RED}}Had a problem stopping %s' % current_name

        return output_msg

    def elevate_privileges(self):
        self.run_command('sudo printf "Priviledges elevated."')
