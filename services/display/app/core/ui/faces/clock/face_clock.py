from PIL import Image
from PIL import ImageDraw

from core.ui.faces.dali.eye import Eye


class ClockFace(object):
    renderer = None


    def __init__(self, parent_renderer=None):
        self.renderer = parent_renderer

    def start(self):
        pass

    def render(self):
        if self.renderer:
            self.renderer.rectangle((0,0,240,320), fill=(255,0,0))
