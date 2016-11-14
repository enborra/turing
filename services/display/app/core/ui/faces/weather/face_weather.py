import datetime

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from astral import Astral

from core.framework import Foreman
from core.framework import Interface
from core.ui.faces.dali.eye import Eye


class WeatherFace(object):
    # Render size properties

    _width = 0
    _height = 0
    _size_width = None
    _size_height = None
    _astral_mgr = None

    _sun_data = None

    # Public properties

    renderer = None

    # Public methods

    def __init__(self, ui_width_size=None, ui_height_size=None):
        self._size_width = ui_width_size
        self._size_height = ui_height_size

        self._width = 320
        self._height = 240

        self._astral_mgr = Astral()
        self._astral_mgr.solar_depression = 'civil'

        city = self._astral_mgr['San Francisco']
        self._sun_data = city.sun(date=datetime.datetime.now(), local=True)

        print str(self._sun_data['dawn'])

    def start(self):
        Foreman.debug_msg('Starting ClockFace')

    def stop(self):
        Foreman.debug_msg('Stopping Clock face.')

    def render(self):
        resp = None

        if Foreman.renderer:
            # Set up drawing canvas and font

            canvas_img = Image.new('RGB', (self._width,self._height), Interface.COLOR_BLACK)
            canvas_draw = ImageDraw.Draw(canvas_img)

            # Add elements to canvas

            render_str = 'Sunset: ' + str(self._sun_data['dusk'].strftime("%I:%M %p"))

            type_width, type_height = canvas_draw.textsize(render_str, Foreman.font_futura_medium)

            canvas_draw.text(((320-type_width)/2, (240-type_height)/2), render_str, font=Foreman.font_futura_medium, fill=Interface.COLOR_WHITE)

            resp = canvas_img

        return resp
