from core.framework.machine_system import MachineSystem

# If working in a simulated environment, include
# needed packages for drawing window-based display
# output emulation.

if MachineSystem.is_simulated():
    import Tkinter
    from PIL import ImageTk
    import tkFont


class MetricTab(object):
    _obj = None
    _obj_title = None
    _screen = None
    _title = ''

    _font_helvetica = None
    _font_helvetica_large = None


    def __init__(self, parent_screen=None, title=None, x=None, y=None):
        self._font_helvetica = tkFont.Font(size=10)
        self._font_helvetica_large = tkFont.Font(size=30)

        self._title = title
        self._x = x
        self._y = y

        self._screen = parent_screen

        self._obj = Tkinter.Text(
            self._screen,
            width=20,
            height=10,
            font=self._font_helvetica_large
        )

        self._obj.config(foreground='white')
        self._obj.config(background='black')
        self._obj.config(highlightbackground='black')

        self._obj.pack()
        self._obj.place(x=self._x, y=self._y)

        # Create title object

        self._obj_title = Tkinter.Text(
            self._screen,
            width=20,
            height=1,
            font=self._font_helvetica,
        )

        self._obj_title.config(foreground='#444')
        self._obj_title.config(background='black')
        self._obj_title.config(highlightbackground='black')

        self._obj_title.pack()
        self._obj_title.place(x=self._x, y=self._y-20)

        self._obj_title.insert(1.0, self._title.upper())

    def update(self, metric):
        self._obj.delete(1.0, 'end')
        self._obj.insert(1.0, str(metric))
