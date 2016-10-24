# import os
import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from core.framework import Foreman
from core.framework import Interface

from core.ui.faces.dali.eye import Eye


class ClockFace(object):
    # Render size properties

    _width = 0
    _height = 0
    _size_width = None
    _size_height = None

    # Public properties

    renderer = None

    # Public methods

    def __init__(self, ui_width_size=None, ui_height_size=None):
        self._size_width = ui_width_size
        self._size_height = ui_height_size

        self._width = 320
        self._height = 240

    def start(self):
        pass

    def render(self):
        resp = None

        if Foreman.renderer:
            curr_time_msg = datetime.datetime.now().strftime("%I:%M %p")
            curr_frame_rate_msg = '%s' % Foreman.get_frame_rate()

            # Set up drawing canvas and font

            canvas_img = Image.new('RGBA', (self._width,self._height), Interface.COLOR_BLACK)
            canvas_draw = ImageDraw.Draw(canvas_img)

            # Add elements to canvas

            type_width, type_height = canvas_draw.textsize(curr_time_msg, Foreman.font_futura_medium)

            canvas_draw.text(((320-type_width)/2, (240-type_height)/2), curr_time_msg, font=Foreman.font_futura_medium, fill=Interface.COLOR_WHITE)
            canvas_draw.text((10,10), curr_frame_rate_msg, font=Foreman.font_futura_small, fill=Interface.COLOR_WHITE)

            resp = canvas_img

        return resp
