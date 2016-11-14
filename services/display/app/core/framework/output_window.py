from PIL import Image, ImageDraw, ImageFont

from core.framework.interface import Interface
from core.framework.machine_system import MachineSystem

# If working in a simulated environment, include
# needed packages for drawing window-based display
# output emulation.

if MachineSystem.is_simulated():
    import Tkinter
    from PIL import ImageTk
    import tkFont
    from core.framework.metric_tab import MetricTab


class OutputWindow(object):
    _width = 640
    _height = 480

    # Render management internal properties

    _screen = None
    _image = None
    _renderer = None
    _text = ''
    _full_text = ''

    # Font internal properties

    _font_helvetica = None
    _font_helvetica_large = None

    # Metrics tabs

    _metrics_tabs = {}


    def __init__(self):
        pass

    def start(self):
        self._image = Image.new(
            'RGB',
            (self._width, self._height),
            Interface.COLOR_BLACK
        )

        self._renderer = ImageDraw.Draw(self._image)

        if MachineSystem.is_simulated():
            self._screen = Tkinter.Toplevel()
            self._screen.title('Debug')
            self._screen.resizable(width=False, height=False)
            self._screen.geometry('%sx%s+%s+%s' % (self._width, self._height, 50, 350))
            self._screen.config(background='black')

            self._font_helvetica = tkFont.Font(size=12)
            self._font_helvetica_large = tkFont.Font(size=30)

            # TODO: The width/height measurements are in lines, not pixels. Need
            #       to build a converter, rather than this guess & check

            self._text = Tkinter.Text(
                self._screen,
                width=59,
                height=23,
                font=self._font_helvetica
            )

            self._text.config(highlightbackground='black')
            self._text.config(background='black')
            self._text.config(foreground='white')
            self._text.config(borderwidth='0p')

            self._text.pack()
            self._text.place(x=20, y=20)

    def update(self):
        if self._screen:
            if self._text:
                if self._text.get('1.0', 'end') != self._full_text:
                    self._text.delete(1.0, 'end')
                    self._text.insert(1.0, self._full_text + '\n')



            self._screen.update()

    def append(self, msg):
        self._full_text = ('%s\n' + self._full_text) % msg

    def create_metric_tab(self, tab_name):
        self._metrics_tabs[tab_name] = MetricTab(
            title='Framerate',
            parent_screen=self._screen,
            x=20+(70*len(self._metrics_tabs)),
            y=self._height-60
        )

    def update_metric_tab(self, tab_name, metric):
        if self._metrics_tabs[tab_name]:
            self._metrics_tabs[tab_name].update(metric)
