from core import BaseController
from core.event_hook import EventHook


class MotorController(BaseController):
    on_move = None
    on_drive = None
    on_turn = None

    DRIVE_FORWARD = 'motor_drive_forward'
    DRIVE_BACKWARD = 'motor_drive_backward'
    TURN_LEFT = 'motor_turn_left'
    TURN_RIGHT = 'motor_turn_right'


    def __init__(self):
        BaseController.__init__(self)

        self._class_output_id = 'turing.os.motor'

        on_move = EventHook()
        on_drive = EventHook()
        on_turn = EventHook()

        self.output('Booting')


    def turn(self, direction, amount):
        self.on_move.fire({
            'direction': direction,
            'amount': amount,
        })

    def drive(self, direction, duration):
        self.on_drive.fire({
            'direction': direction,
            'duration': duration,
        })
