import time
import math
import os
from PIL import Image, ImageDraw, ImageFont

from libs import ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

from core.framework.interface import Interface
from core.framework.event_hook import EventHook
from core.framework.machine_system import MachineSystem
from core.framework.output_window import OutputWindow

# If running in simulated environment, include module for
# writing debug output to on-screen window.

if MachineSystem.is_simulated():
    import Tkinter
    from PIL import ImageTk


class Foreman(object):
    _screen = None
    _screen_width = 320
    _screen_height = 240
    _last_update_call = 0

    _debug_window = None

    _image = None
    _image_staged = None

    # Animation properties

    _last_frame_update = 0
    _last_second_update = 0
    _current_frame_count = 0
    _current_frame_rate = 30
    _frame_rate_max = 30

    _frame_duration_min = 1000 / _frame_rate_max
    _current_frame_multiplier = 1

    _recent_frame_perf = []
    _frame_rate_sample_size = 10

    # Typefaces

    font_futura_small = None
    font_futura_medium = None
    font_futura_large = None
    font_lekton_small = None

    # Onboard display output settings

    _DC = 18
    _RST = 23
    _SPI_PORT = 0
    _SPI_DEVICE = 0
    _REFRESH_SPEED = 64000000

    # Event hooks

    on_second = None
    on_frame = None
    on_second_half = None
    on_second_quarter = None

    # Public properties

    renderer = None

    # Public methods

    @classmethod
    def initialize(cls):
        cls.on_second = EventHook()
        cls.on_frame = EventHook()
        cls.on_second_half = EventHook()
        cls.on_second_quarter = EventHook()

        if MachineSystem.is_simulated:
            cls._debug_window = OutputWindow()

    @classmethod
    def start(cls):
        font_path = os.path.dirname(os.path.realpath(__file__))
        font_file_path = font_path+'/../fonts/futura_book.otf'

        cls.font_futura_small = ImageFont.truetype(font_file_path, 12)
        cls.font_futura_medium = ImageFont.truetype(font_file_path, 30)
        cls.font_futura_large = ImageFont.truetype(font_file_path, 45)

        cls._image = Image.new('RGBA', (cls._screen_height, cls._screen_width), Interface.COLOR_BLACK)
        cls.renderer = ImageDraw.Draw(cls._image)

        if MachineSystem.is_onboard():
            cls._disp = TFT(
                cls._DC,
                rst=cls._RST,
                spi=SPI.SpiDev(cls._SPI_PORT, cls._SPI_DEVICE, max_speed_hz=cls._REFRESH_SPEED)
            )

            cls._disp.begin()

        elif MachineSystem.is_simulated():
            cls._screen = Tkinter.Tk(className='Window')
            cls._screen.resizable(width=False, height=False)
            cls._screen.geometry('%sx%s+%s+%s' % (cls._screen_width, cls._screen_height, 50, 50))

            cls._lbl = Tkinter.Label(cls._screen)
            cls._lbl.config(borderwidth='0p')
            cls._lbl.config(background='black')
            cls._lbl.pack()
            cls._lbl.place(x=0, y=0)

            cls._debug_window.start()
            cls._debug_window.create_metric_tab('frame_rate')

    @classmethod
    def get_millis(cls):
        return time.time()*1000

    @classmethod
    def get_frame_rate(cls):
        return cls._current_frame_rate

    @classmethod
    def draw(cls, img):
        x = 0
        y = 0
        cls._image.paste(img, (y,x))

    @classmethod
    def update(cls):
        time_since_last_second_elapse = cls.get_millis() - cls._last_second_update
        time_since_last_frame_elapse = cls.get_millis() - cls._last_frame_update

        if time_since_last_second_elapse > 1000:
            cls._last_second_update = cls.get_millis()
            cls._current_frame_rate = cls._current_frame_count
            cls._current_frame_multiplier = float(cls._current_frame_rate) / float(1000)
            cls._current_frame_count = 0

            cls.on_second_half.fire()
            cls.on_second.fire()

        else:
            if int(cls._current_frame_rate/2) == int(cls._current_frame_count):
                cls.on_second_half.fire()

        cls._current_frame_count += 1

        if time_since_last_frame_elapse > cls._current_frame_multiplier:
            cls._last_frame_update = cls.get_millis()
            cls._record_frame_render_time()

            cls.on_frame.fire()

        if MachineSystem.is_onboard():
            cls._disp.display(cls._image)

        elif MachineSystem.is_simulated():
            if cls._image:
                cls._image_staged = ImageTk.PhotoImage(cls._image.rotate(90, expand=True))
                cls._lbl.config(image=cls._image_staged)
                cls._screen.update()

                # Update debug output window

                cls._debug_window.update()
                cls._debug_window.update_metric_tab('frame_rate', cls.get_frame_rate())

    @classmethod
    def debug_msg(cls, msg):
        cls._debug_window.append(msg)

    @classmethod
    def _record_frame_render_time(cls):
        if len(cls._recent_frame_perf) >= cls._frame_rate_sample_size:
            avg = 0

            for sample in cls._recent_frame_perf:
                avg += sample

            avg = avg / len(cls._recent_frame_perf)

            cls._current_frame_multiplier = avg
            cls._recent_frame_perf = []

        else:
            frame_process_time = cls.get_millis() - cls._last_frame_update

            cls._recent_frame_perf.append(frame_process_time)
