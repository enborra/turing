import os

from .controller_base import BaseController


class RaspberryPiController(BaseController):

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

    def stop_service(self):
        super().stop_service()

        for service_name in self._commands['services']:
            current_config = self._commands['services'][service_name]
            current_name = current_config['name']
            current_run_file_name = current_config['install']['osx']

            # If the service is running, stop it

            try:
                self.run_command('sudo systemctl status %s' % self._commands['services'][service_name]['install']['raspberry_pi'])
                self.run_command('sudo systemctl stop %s' % self._commands['services'][service_name]['install']['raspberry_pi'])

                self.display('{{RED}}Stopped service:{{WHITE}} %s' % current_name)

            except Exception as e:
                self.display('{{YELLOW}}Service was not running:{{WHITE}} %s' % current_name)

        self._cleanup()

    def start_service(self):
        super().start_service()

        for service_name in self._commands['services']:
            current_config = self._commands['services'][service_name]
            current_name = current_config['name']
            current_run_file_name = current_config['install']['osx']

            # If the service is running, stop it

            try:
                self.run_command('sudo systemctl status %s' % self._commands['services'][service_name]['install']['raspberry_pi'])

                self.display('{{YELLOW}}Service already running:{{WHITE}} %s' % current_name)

            except Exception as e:
                self.run_command('sudo systemctl start %s' % self._commands['services'][service_name]['install']['raspberry_pi'])

                self.display('{{GREEN}}Service started:{{WHITE}} %s' % current_name)

        self._cleanup()

    def get_service_status(self):
        for item in self._commands['services']:
            try:
                self.run_command('sudo systemctl status ' + self._commands['services'][item]['install']['raspberry_pi'])
                self.display('{{GREEN}}Service running: {{WHITE}}%s' % item)

            except Exception as e:
                self.display('{{RED}}Service not running: {{WHITE}}%s' % item)

        print()

    def update_source(self):
        super().update_source()
        self.stop_service()

        self.display('{{GREEN}}Pulling new code down from origin/master{{DARKGRAY}}')

        subprocess.check_output('cd $TURING_APP_DIR', shell=True)
        subprocess.check_output('git pull origin master', shell=True)
        subprocess.check_output('cd /home/pi/projects/turing/services/central_station', shell=True)

        self.display('{{WHITE}}')

        self.start_service()

    def install_service(self):
        super().install_service()

        print('INSTALL RASPBERRYPI SERVICE.')

        for service_name in self._commands['services']:
            current_service_config = self._commands['services'][service_name]
            current_service_name = current_service_config['name']
            current_service_run_file_name = current_service_config['install']['raspberry_pi']

            path_service_source_file = self._path_app_root + service_name + '/' + self._path_source_root + current_service_run_file_name
            path_service_run_file = self._path_run_root + current_service_run_file_name


            self.display('{{GREEN}}Installing service:{{WHITE}} %s' % current_service_run_file_name)

            # If the service is running, stop it

            try:
                self.run_command('sudo systemctl stop %s' % current_service_run_file_name)
                self.run_command('sudo systemctl disable %s' % path_service_run_file)

                print('successfully uninstalled.')

            except Exception as e:
                print('Had a problem uninstalling service: %s' % str(e))

            # Now install new service and load it

            # self.run_command('sudo cp -f %s %s' % (path_service_source_file, path_service_run_file))
            # self.run_command('sudo chmod +x %s' % path_service_run_file)
            # self.run_command('sudo systemctl enable %s' % path_service_run_file)
            # self.run_command('sudo systemctl start %s' % path_service_source_file)

        self._cleanup()
