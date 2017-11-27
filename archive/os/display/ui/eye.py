from PIL import Image
from PIL import ImageDraw

from shape import Shape



class Eye(Shape):
    x = 0
    y = 0

    _blink_wait_count = 0
    renderer = None


    def __init__(self, parent_renderer=None, x_pos=0, y_pos=0):
        self.x = x_pos
        self.y = y_pos
        self.renderer = parent_renderer

        self.width = 50
        self.height = 50

    def render(self):
        print('Rendering eye.')


        if self._blink_wait_count > 23 and self._blink_wait_count <= 25:
            self._blink_wait_count += 1

        elif self._blink_wait_count > 25:
            self._blink_wait_count = 0

        else:
            self.renderer.ellipse((self.y, self.x, self.y+self.height, self.x+self.width), fill=(255,255,255))
            self.renderer.ellipse((0, 0, 100, 100), fill=(255,255,0))

            self._blink_wait_count += 1
