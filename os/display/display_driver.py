import sys
import tkinter as tk
import threading

from framework import Settings


class DisplayDriver(object):
    _environment = Settings.ENVIRONMENT_SIMULATED
    _canvas = None
    # _i = 0

    def __init__(self):
        pass


    def start(self):
        print('[DISPLAY] Starting.')

        # d = tk.Tk()
        # d.geometry('450x450')

        renderer = tk.Tk()
        # renderer.geometry('450x450')

        self._canvas = tk.Canvas(renderer, width=200, height=100)
        self._canvas.coords(0, 500)
        self._canvas.pack()

        self._canvas.create_line(0, 0, 200, 100)
        self._canvas.create_line(0, 100, 200, 0, fill='red', dash=(4, 4))
        self._canvas.create_rectangle(50, 25, 150, 75, fill='blue')


        window_main = tk.Frame(master=renderer)
        window_main.master.title('Testing')
        window_main.master.maxsize(1000, 450)
        window_main.master.minsize(450, 450)
        window_main.mainloop()


    def update(self):
        print('[DISPLAY] Updating.')

        # _i = i + 1

        import time
        time.sleep(1)
