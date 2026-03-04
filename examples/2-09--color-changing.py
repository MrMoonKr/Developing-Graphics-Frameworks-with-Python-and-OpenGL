#!/usr/bin/python3

# """
# Original Code (Preserved)
# import math
#
# import OpenGL.GL as GL
#
# from py3d.core.base import Base
# from py3d.core.utils import Utils
# from py3d.core.attribute import Attribute
# from py3d.core.uniform import Uniform
#
#
# class Example(Base):
#     """ Animate a triangle changing its color """
#     def initialize(self):
#         print("Initializing program...")
#         # Initialize program #
#         vs_code = """
#             in vec3 position;
#             uniform vec3 translation;
#             void main()
#             {
#                 vec3 pos = position + translation;
#                 gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
#             }
#         """
#         fs_code = """
#             uniform vec3 baseColor;
#             out vec4 fragColor;
#             void main()
#             {
#                 fragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1.0);
#             }
#         """
#         self.program_ref = Utils.initialize_program(vs_code, fs_code)
#         # render settings (optional) #
#         # Specify color used when clearly
#         GL.glClearColor(0.0, 0.0, 0.0, 1.0)
#         # Set up vertex array object #
#         vao_ref = GL.glGenVertexArrays(1)
#         GL.glBindVertexArray(vao_ref)
#         # Set up vertex attribute #
#         position_data = [[ 0.0,  0.2,  0.0],
#                          [ 0.2, -0.2,  0.0],
#                          [-0.2, -0.2,  0.0]]
#         self.vertex_count = len(position_data)
#         position_attribute = Attribute('vec3', position_data)
#         position_attribute.associate_variable(self.program_ref, 'position')
#         # Set up uniforms #
#         self.translation = Uniform('vec3', [-0.5, 0.0, 0.0])
#         self.translation.locate_variable(self.program_ref, 'translation')
#         self.base_color = Uniform('vec3', [1.0, 0.0, 0.0])
#         self.base_color.locate_variable(self.program_ref, 'baseColor')
#
#     def update(self):
#         """ Update data """
#         # self.base_color.data[0] = (math.sin(3 * self.time) + 1) / 2
#         self.base_color.data[0] = (math.sin(self.time) + 1) / 2
#         self.base_color.data[1] = (math.sin(self.time + 2.1) + 1) / 2
#         self.base_color.data[2] = (math.sin(self.time + 4.2) + 1) / 2
#         # Reset color buffer with specified color
#         GL.glClear(GL.GL_COLOR_BUFFER_BIT)
#         GL.glUseProgram(self.program_ref)
#         self.translation.upload_data()
#         self.base_color.upload_data()
#         GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)
#
#
# # Instantiate this class and run the program
# Example().run()
# """

from datetime import datetime
import math
from time import perf_counter
import tkinter as tk
from tkinter import ttk

import numpy as np
from OpenGL import GL
from OpenGL.GL.shaders import compileProgram, compileShader
from pyopengltk import OpenGLFrame


class GLFrame(OpenGLFrame):
    def __init__(self, parent, logger):
        super().__init__(parent)
        self._logger = logger
        self._start_time = perf_counter()
        self._last_time = self._start_time
        self._elapsed_time = 0.0
        self._started = False
        self._viewport_size = (1, 1)
        self._program_ref = None
        self._vao_ref = None
        self._vertex_count = 0
        self._translation_loc = -1
        self._base_color_loc = -1
        self._translation = [-0.5, 0.0, 0.0]
        self._base_color = [1.0, 0.0, 0.0]

    def initgl(self):
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        self._build_shader_program()
        self._setup_geometry()
        self._translation_loc = GL.glGetUniformLocation(self._program_ref, "translation")
        self._base_color_loc = GL.glGetUniformLocation(self._program_ref, "baseColor")
        self.on_resize(self.winfo_width(), self.winfo_height())
        self._logger("INFO", "OpenGL initialized")

    def redraw(self):
        now = perf_counter()
        dt = now - self._last_time
        self._last_time = now
        self._elapsed_time = now - self._start_time

        width, height = self._viewport_size
        GL.glViewport(0, 0, width, height)

        self.update_scene(dt)
        self.draw_scene()

    def on_resize(self, width, height):
        width = max(1, int(width))
        height = max(1, int(height))
        new_size = (width, height)
        if new_size == self._viewport_size:
            return

        self._viewport_size = new_size
        self._logger("INFO", f"GL viewport resized: {width}x{height}")

    def update_scene(self, dt):
        if not self._started:
            self._logger("INFO", f"Render loop started (dt={dt:.4f}s)")
            self._started = True

        self._base_color[0] = (math.sin(self._elapsed_time) + 1.0) / 2.0
        self._base_color[1] = (math.sin(self._elapsed_time + 2.1) + 1.0) / 2.0
        self._base_color[2] = (math.sin(self._elapsed_time + 4.2) + 1.0) / 2.0

    def draw_scene(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glUseProgram(self._program_ref)
        GL.glBindVertexArray(self._vao_ref)
        GL.glUniform3f(self._translation_loc, *self._translation)
        GL.glUniform3f(self._base_color_loc, *self._base_color)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self._vertex_count)

    def _build_shader_program(self):
        vertex_shader_code = """
            #version 120
            attribute vec3 position;
            uniform vec3 translation;
            void main()
            {
                vec3 pos = position + translation;
                gl_Position = vec4(pos.x, pos.y, pos.z, 1.0);
            }
        """
        fragment_shader_code = """
            #version 120
            uniform vec3 baseColor;
            void main()
            {
                gl_FragColor = vec4(baseColor.r, baseColor.g, baseColor.b, 1.0);
            }
        """
        self._program_ref = compileProgram(
            compileShader(vertex_shader_code, GL.GL_VERTEX_SHADER),
            compileShader(fragment_shader_code, GL.GL_FRAGMENT_SHADER),
        )
        self._logger("INFO", "Shader program compiled")

    def _setup_geometry(self):
        position_data = np.array(
            [
                [0.0, 0.2, 0.0],
                [0.2, -0.2, 0.0],
                [-0.2, -0.2, 0.0],
            ],
            dtype=np.float32,
        )
        self._vertex_count = len(position_data)

        self._vao_ref = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao_ref)

        position_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, position_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, position_data.nbytes, position_data, GL.GL_STATIC_DRAW)
        position_loc = GL.glGetAttribLocation(self._program_ref, "position")
        GL.glEnableVertexAttribArray(position_loc)
        GL.glVertexAttribPointer(position_loc, 3, GL.GL_FLOAT, False, 0, None)
        self._logger("INFO", f"Geometry created (vertices={self._vertex_count})")


class LogPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.tree = ttk.Treeview(self, columns=("time", "level", "message"), show="headings", height=8)
        self.tree.heading("time", text="Time")
        self.tree.heading("level", text="Level")
        self.tree.heading("message", text="Message")
        self.tree.column("time", width=90, anchor=tk.CENTER, stretch=False)
        self.tree.column("level", width=70, anchor=tk.CENTER, stretch=False)
        self.tree.column("message", width=600, anchor=tk.W, stretch=True)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def log(self, level, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.tree.insert("", tk.END, values=(timestamp, level, message))
        self.tree.yview_moveto(1.0)


class GLApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2-09 Color Changing")
        self.geometry("1000x700")
        self.minsize(640, 480)
        self._last_window_size = (0, 0)
        self._create_layout()
        self.bind("<Configure>", self._on_window_resize)
        self.log_panel.log("INFO", "Application started")

    def _create_layout(self):
        paned = ttk.PanedWindow(self, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True)

        gl_host = ttk.Frame(paned)
        log_host = ttk.Frame(paned)
        paned.add(gl_host, weight=7)
        paned.add(log_host, weight=3)

        self.gl_frame = GLFrame(gl_host, logger=self._log)
        self.gl_frame.pack(fill=tk.BOTH, expand=True)
        self.gl_frame.animate = 1

        self.log_panel = LogPanel(log_host)
        self.log_panel.pack(fill=tk.BOTH, expand=True)

        self.after(100, lambda: paned.sashpos(0, int(self.winfo_height() * 0.7)))

    def _on_window_resize(self, event):
        if event.widget is not self:
            return

        new_size = (event.width, event.height)
        if new_size == self._last_window_size:
            return

        self._last_window_size = new_size
        self.on_window_resized(event.width, event.height)

    def on_window_resized(self, width, height):
        self._log("INFO", f"Window resized: {width}x{height}")
        self.gl_frame.on_resize(self.gl_frame.winfo_width(), self.gl_frame.winfo_height())

    def _log(self, level, message):
        if hasattr(self, "log_panel"):
            self.log_panel.log(level, message)


def main():
    app = GLApp()
    app.mainloop()


if __name__ == "__main__":
    main()
