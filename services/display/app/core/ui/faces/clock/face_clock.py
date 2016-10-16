from PIL import Image
from PIL import ImageDraw

from core.ui.faces.dali.eye import Eye


class ClockFace(object):
    renderer = None
    i = 0


    def __init__(self, parent_renderer=None):
        self.renderer = parent_renderer

    def start(self):
        pass

    def render(self):
        if i>200:
            i = 0
        else:
            i += 1

        if self.renderer:
            self.renderer.rectangle((0,0,240,320), fill=(0,0,0))
            self.renderer.rectangle((i,100,150,150), fill=(0,255,0))
