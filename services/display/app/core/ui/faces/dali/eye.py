from PIL import Image
from PIL import ImageDraw


from core.framework import Foreman
from core.framework import Interface

from core.ui.shape import Shape



class Eye(Shape):
    x = 0
    y = 0

    _blink_wait_count = 0
    parent_renderer = None


    def __init__(self, parent_renderer=None, x=0, y=0):
        self.x = x
        self.y = y

        self.parent_renderer = parent_renderer

        self.width = 50
        self.height = 50

    def blink(self):
        self._blink_wait_count = 24

    def render(self, parent_renderer=None):
        self.parent_renderer = parent_renderer

        if self._blink_wait_count > 23 and self._blink_wait_count <= 25:
            self._blink_wait_count += 1

        elif self._blink_wait_count > 25:
            self._blink_wait_count = 0

        else:
            if self.parent_renderer:
                start_x = self.x
                start_y = self.y
                end_x = self.x+self.width
                end_y = self.y+self.height

                self.parent_renderer.ellipse((start_x, start_y, end_x, end_y), fill=(255,255,255))

            self._blink_wait_count += 1
