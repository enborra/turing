from PIL import Image
from PIL import ImageDraw

from display.ui.faces.dali.eye import Eye


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

    def render(self):
        e_left = self._eye_left.render()
        e_right = self._eye_right.render()
