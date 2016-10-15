import os

from .controller_base import BaseController


class OsxController(BaseController):

    def __init__(self):
        self._ensure_command_library_loaded()

        self._path_current_file = os.path.dirname(os.path.realpath(__file__)) + '/'
        self._path_app_root = self._path_current_file + '../../'
        self._path_source_root = self._commands['file_locations']['services_source_directory']
        self._path_run_directory = self._commands['file_locations']['services_run_directory_osx']
        self._path_current_file = os.path.dirname(os.path.realpath(__file__)) + '/'
        self._path_app_root = self._path_current_file + '../../../'
        self._path_source_root = self._commands['file_locations']['services_source_directory']
        self._path_run_root = self._commands['file_locations']['services_run_directory_osx']

    def stop_service(self, service_name):
        is_enabled = True
        output_msg = None

        current_config = self._commands['services'][service_name]
        current_run_file_name = current_config['install']['osx']
        current_name = current_config['name']

        if 'enabled' in current_config:
            if current_config['enabled'] == False:
                is_enabled = False

        # If the service is running, stop it

        try:
            self.run_command('sudo launchctl list | grep %s' % current_name)
            self.run_command('sudo launchctl unload %s' % (self._path_run_directory + current_run_file_name))

            output_msg = '{{RED}}Stopped service:{{WHITE}} %s' % current_name

        except Exception as e:
            output_msg = '{{YELLOW}}Service was not running:{{WHITE}} %s' % current_name

        if not is_enabled:
            output_msg += ' {{DARKGRAY}}(disabled)'

        return output_msg

    def start_service(self, service_name=None):
        is_enabled = True
        output_msg = None

        current_config = self._commands['services'][service_name]
        current_run_file_name = current_config['install']['osx']
        current_name = current_config['name']

        if 'enabled' in current_config:
            if current_config['enabled'] == False:
                is_enabled = False

        if is_enabled:
            # If the service is running, stop it

            try:
                self.run_command('sudo launchctl list | grep %s' % current_name)

                output_msg = '{{YELLOW}}Service already running:{{WHITE}} %s' % current_name

            except Exception as e:
                self.run_command('sudo launchctl load %s' % (self._path_run_directory + current_run_file_name))

                output_msg = '{{GREEN}}Started service:{{WHITE}} %s' % current_name

        else:
            output_msg = '{{DARKGRAY}}Skipping disabled service:{{WHITE}} %s' % current_name

        return output_msg

    def get_service_status(self, service_name):
        is_enabled = True
        output_msg = None

        current_config = self._commands['services'][service_name]
        current_name = current_config['name']
        current_run_file_name = current_config['install']['osx']

        if 'enabled' in current_config:
            if current_config['enabled'] == False:
                is_enabled = False

        try:
            self.run_command('sudo launchctl list | grep ' + current_name)
            output_msg = '{{GREEN}}Service running: {{WHITE}}%s' % service_name

        except Exception as e:
            output_msg = '{{RED}}Service not running: {{WHITE}}%s' % service_name

        if not is_enabled:
            output_msg += ' {{DARKGRAY}}(disabled)'

        return output_msg

    def get_service_status_OLD(self):
        for service_name in self._commands['services']:
            is_enabled = True

            current_config = self._commands['services'][service_name]
            current_name = current_config['name']

            if 'enabled' in current_config:
                if current_config['enabled'] == False:
                    is_enabled = False

            if is_enabled:
                current_run_file_name = current_config['install']['osx']

                try:
                    self.run_command('sudo launchctl list | grep ' + self._commands['services'][service_name]['name'])
                    self.display('{{GREEN}}Service running: {{WHITE}}%s' % service_name)

                except Exception as e:
                    self.display('{{RED}}Service not running: {{WHITE}}%s' % service_name)

            else:
                self.display('{{DARKGRAY}}Service disabled: %s' % current_name)

        print()

    def update_source(self):
        self.stop_service()
        super().update_source()

        self.display('{{GREEN}}Pulling new code down from origin/master{{DARKGRAY}}')

        self.run_command('cd $TURING_APP_DIR')
        self.run_command('git pull origin master')

        self.display('{{WHITE}}')

        self.start_service()

    def install_service(self):
        super().install_service()

        for service_name in self._commands['services']:

            is_enabled = True

            current_config = self._commands['services'][service_name]
            current_name = current_config['name']

            if 'enabled' in current_config:
                if current_config['enabled'] == False:
                    is_enabled = False

            if is_enabled:
                current_run_file_name = current_config['install']['osx']

                current_service_config = self._commands['services'][service_name]
                current_service_name = current_service_config['name']
                current_service_run_file_name = current_service_config['install']['osx']

                path_service_source_file = self._path_app_root + service_name + '/' + self._path_source_root + current_service_run_file_name
                path_service_run_file = self._path_run_root + current_service_run_file_name


                self.display('{{GREEN}}Installing service:{{WHITE}} %s' % current_service_run_file_name)

                # If the service is running, stop it

                try:
                    self.run_command('sudo launchctl list | grep %s' % current_service_name)
                    self.run_command('sudo launchctl unload %s' % path_service_run_file)

                except Exception:
                    pass

                # Now install new service and load it

                self.run_command('sudo ln -sf %s %s' % (path_service_source_file, path_service_run_file))
                self.run_command('sudo chown root:wheel %s' % path_service_run_file)
                self.run_command('sudo launchctl load %s' % path_service_run_file)

            else:
                self.display('{{DARKGRAY}}Skipping disabled service: %s' % current_name)

        self._cleanup()
