from PIL import Image
from PIL import ImageDraw

from core.ui.faces.dali.eye import Eye


class DaliFace(object):
    renderer = None
    _eye_left = None
    _eye_right = None


    def __init__(self, parent_renderer=None):
        self.renderer = parent_renderer

        self._eye_left = Eye(self.renderer, 50, 100)
        self._eye_right = Eye(self.renderer, 200, 100)


    def start(self):
        pass

    def blink(self):
        self._eye_left.blink()
        self._eye_right.blink()

    def render(self):
        self.renderer.rectangle((0,0,240,320), fill=(0,0,0))

        e_left = self._eye_left.render()
        e_right = self._eye_right.render()
