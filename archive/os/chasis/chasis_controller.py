from framework import BaseController
from motor_controller import MotorController



class ChasisController(BaseController):
    motor = None

    def __init__(self):
        BaseController.__init__(self)

        self._class_output_id = 'turing.chasis'

        self.motor = MotorController()
