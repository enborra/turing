from PIL import Image
from PIL import ImageDraw

from core.framework import Foreman
from core.framework import Interface

from core.ui.faces.dali.eye import Eye


class DaliFace(object):
    _width = 0
    _height = 0
    _size_width = 0
    _size_height = 0
    _eye_left = None
    _eye_right = None


    def __init__(self, ui_width_size=None, ui_height_size=None):
        self._size_width = ui_width_size
        self._size_height = ui_height_size

        self._width = 320
        self._height = 240

        self._eye_left = Eye(
            parent_renderer=None,
            x=50,
            y=100,
        )

        self._eye_right = Eye(
            parent_renderer=None,
            x=200,
            y=100,
        )

    def start(self):
        Foreman.debug_msg('Starting Dali face.')

    def blink(self):
        self._eye_left.blink()
        self._eye_right.blink()

    def render(self):
        resp = None

        if Foreman.renderer:
            Foreman.renderer.rectangle((0,0,240,320), fill=(0,0,0))

        if Foreman.renderer:
            # Set up drawing canvas

            canvas_img = Image.new('RGB', (self._width,self._height), Interface.COLOR_BLACK)
            canvas_draw = ImageDraw.Draw(canvas_img)

            # Add elements to canvas

            type_width, type_height = canvas_draw.textsize('asdf', Foreman.font_futura_medium)

            # canvas_draw.text(((320-type_width)/2, (240-type_height)/2), 'asdf', font=Foreman.font_futura_medium, fill=Interface.COLOR_WHITE)
            # canvas_draw.text((10,10), 'asdf', font=Foreman.font_futura_small, fill=Interface.COLOR_WHITE)

            self._eye_left.render(canvas_draw)
            self._eye_right.render(canvas_draw)


            resp = canvas_img

        return resp
