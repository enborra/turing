from PIL import Image
from PIL import ImageDraw

from shape import Shape



class Eye(Shape):
    x = 0
    y = 0

    _blink_wait_count = 0
    canvas = None


    def __init__(self, source_canvas=None, x_pos=0, y_pos=0):
        self.x = x_pos
        self.y = y_pos
        self.canvas = source_canvas

    def render(self):
        print('Rendering eye.')


        if self._blink_wait_count > 23 and self._blink_wait_count <= 25:
            self._blink_wait_count += 1

        elif self._blink_wait_count > 25:
            self._blink_wait_count = 0

        else:
            circle = ImageDraw.Draw(self.canvas)
            circle.ellipse((self.y, self.x, self.y+10, self.x+10), fill=(255,255,0))

            self._blink_wait_count += 1
