


class BaseController(object):
    _class_output_id = ''


    def __init__(self):
        pass

    def output(self, msg):
        print '[' + self._class_output_id.upper() + '] ' + msg
