from time import perf_counter
import tkinter as tk

import OpenGL.GL as GL
from pyopengltk import OpenGLFrame

from py3d.core.input import Input
from py3d.core.utils import Utils


class _BaseOpenGLFrame(OpenGLFrame):
    def __init__(self, parent, owner):
        super().__init__(parent)
        self._owner = owner

    def initgl(self):
        self._owner._on_gl_initialize()

    def redraw(self):
        self._owner._on_gl_redraw(self.winfo_width(), self.winfo_height())


class Base:
    def __init__(self, screen_size=(512, 512)):
        width = max(1, int(screen_size[0]))
        height = max(1, int(screen_size[1]))
        self._screen_size = (width, height)
        # Determine if main loop is active
        self._running = True
        # Manage user input
        self._input = Input()
        # number of seconds application has been running
        self._time = 0.0
        self._delta_time = 0.0
        self._last_time = None
        self._initialized = False

        self._root = tk.Tk()
        self._root.title("Graphics Window")
        self._root.geometry(f"{width}x{height}")
        self._root.protocol("WM_DELETE_WINDOW", self._request_quit)

        self._gl_frame = _BaseOpenGLFrame(self._root, owner=self)
        self._gl_frame.pack(fill=tk.BOTH, expand=True)
        self._gl_frame.animate = 1
        self._screen = self._gl_frame  # legacy compatibility

        self._root.bind_all("<KeyPress>", self._on_key_press)
        self._root.bind_all("<KeyRelease>", self._on_key_release)

    @property
    def delta_time(self):
        return self._delta_time

    @property
    def input(self):
        return self._input

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    def initialize(self):
        """ Implement by extending class """
        pass

    def update(self):
        """ Implement by extending class """
        pass

    def run(self):
        self._gl_frame.focus_set()
        self._root.mainloop()

    def _on_gl_initialize(self):
        if self._initialized:
            return
        Utils.print_system_info()
        self.initialize()
        self._last_time = perf_counter()
        self._initialized = True

    def _on_gl_redraw(self, width, height):
        if not self._initialized:
            return

        # Keep viewport in sync with widget size.
        GL.glViewport(0, 0, max(1, int(width)), max(1, int(height)))

        current_time = perf_counter()
        self._delta_time = current_time - self._last_time
        self._last_time = current_time
        self._time += self._delta_time

        self._input.update()
        if self._input.quit:
            self._shutdown()
            return

        self.update()

    def _request_quit(self):
        self._input.set_quit(True)

    def _shutdown(self):
        if not self._running:
            return
        self._running = False
        self._gl_frame.animate = 0
        self._root.after(0, self._root.destroy)

    def _on_key_press(self, event):
        key_name = self._normalize_key(event.keysym)
        self._input.register_key_down(key_name)

    def _on_key_release(self, event):
        key_name = self._normalize_key(event.keysym)
        self._input.register_key_up(key_name)

    @staticmethod
    def _normalize_key(keysym):
        if not keysym:
            return None
        return keysym.lower()
