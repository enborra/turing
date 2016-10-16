import os
import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from core.ui.faces.dali.eye import Eye


class ClockFace(object):
    renderer = None
    i = 0


    def __init__(self, parent_renderer=None):
        self.renderer = parent_renderer

    def start(self):
        pass

    def render(self):
        if self.i>240:
            self.i = 0
        else:
            self.i += 4

        if self.renderer:
            self.renderer.rectangle((0,0,240,320), fill=(0,0,0))
            self.renderer.rectangle((100,self.i,150,self.i+50), fill=(0,255,0))

            font_path = os.path.dirname(os.path.realpath(__file__))

            print font_path

            self.renderer.text((0, 0), "Hello", (255,255,255), font=ImageFont.truetype(font_path+'../../../fonts/futura_book.otf', 16))
