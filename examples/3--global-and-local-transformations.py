#!/usr/bin/python3

# """
# Original Code (Preserved)
# from math import pi
#
# import OpenGL.GL as GL
#
# from py3d.core.base import Base
# from py3d.core.utils import Utils
# from py3d.core.attribute import Attribute
# from py3d.core.uniform import Uniform
# from py3d.core.matrix import Matrix
#
#
# class Example(Base):
#     """
#     Move a triangle around the screen: global and local transformations.
#     Use keys WASDZXQE and IJKLUO respectively.
#     """
#     def initialize(self):
#         print('Initializing program...')
#         ### Initialize program ###
#         vs_code = """
#             in vec3 position;
#             uniform mat4 projectionMatrix;
#             uniform mat4 modelMatrix;
#             void main()
#             {
#                 gl_Position = projectionMatrix * modelMatrix * vec4(position, 1.0);
#             }
#         """
#         fs_code = """
#             out vec4 fragColor;
#             void main()
#             {
#                 fragColor = vec4(1.0, 1.0, 0.0, 1.0);
#             }
#         """
#         self.program_ref = Utils.initialize_program(vs_code, fs_code)
#         ### Render settings ###
#         GL.glClearColor(0.0, 0.0, 0.0, 1.0)
#         GL.glEnable(GL.GL_DEPTH_TEST)
#         ### Set up vertex array object ###
#         vao_ref = GL.glGenVertexArrays(1)
#         GL.glBindVertexArray(vao_ref)
#         ### Set up vertex attribute: three points of triangle ###
#         position_data = [[0.0,   0.2,  0.0], [0.1,  -0.2,  0.0], [-0.1, -0.2,  0.0]]
#         self.vertex_count = len(position_data)
#         position_attribute = Attribute('vec3', position_data)
#         position_attribute.associate_variable(self.program_ref, 'position')
#         ### Set up uniforms ###
#         m_matrix = Matrix.make_translation(0, 0, -1)
#         self.model_matrix = Uniform('mat4', m_matrix)
#         self.model_matrix.locate_variable(self.program_ref, 'modelMatrix')
#         p_matrix = Matrix.make_perspective()
#         self.projection_matrix = Uniform('mat4', p_matrix)
#         self.projection_matrix.locate_variable(self.program_ref, 'projectionMatrix')
#         # movement speed, units per second
#         self.move_speed = 0.5
#         # rotation speed, radians per second
#         self.turn_speed = 90 * (pi / 180)
#
#     def update(self):
#         """ Update data """
#         move_amount = self.move_speed * self.delta_time
#         turn_amount = self.turn_speed * self.delta_time
#         # global translation
#         if self.input.is_key_pressed('w'):
#             m = Matrix.make_translation(0, move_amount, 0)
#             self.model_matrix.data = m @ self.model_matrix.data
#         if self.input.is_key_pressed('s'):
#             m = Matrix.make_translation(0, -move_amount, 0)
#             self.model_matrix.data = m @ self.model_matrix.data
#         if self.input.is_key_pressed('a'):
#             m = Matrix.make_translation(-move_amount, 0, 0)
#             self.model_matrix.data = m @ self.model_matrix.data
#         if self.input.is_key_pressed('d'):
#             m = Matrix.make_translation(move_amount, 0, 0)
#             self.model_matrix.data = m @ self.model_matrix.data
#         if self.input.is_key_pressed('z'):
#             m = Matrix.make_translation(0, 0, move_amount)
#             self.model_matrix.data = m @ self.model_matrix.data
#         if self.input.is_key_pressed('x'):
#             m = Matrix.make_translation(0, 0, -move_amount)
#             self.model_matrix.data = m @ self.model_matrix.data
#         # global rotation (around the origin)
#         if self.input.is_key_pressed('q'):
#             m = Matrix.make_rotation_z(turn_amount)
#             self.model_matrix.data = m @ self.model_matrix.data
#         if self.input.is_key_pressed('e'):
#             m = Matrix.make_rotation_z(-turn_amount)
#             self.model_matrix.data = m @ self.model_matrix.data
#         # local translation
#         if self.input.is_key_pressed('i'):
#             m = Matrix.make_translation(0, move_amount, 0)
#             self.model_matrix.data = self.model_matrix.data @ m
#         if self.input.is_key_pressed('k'):
#             m = Matrix.make_translation(0, -move_amount, 0)
#             self.model_matrix.data = self.model_matrix.data @ m
#         if self.input.is_key_pressed('j'):
#             m = Matrix.make_translation(-move_amount, 0, 0)
#             self.model_matrix.data = self.model_matrix.data @ m
#         if self.input.is_key_pressed('l'):
#             m = Matrix.make_translation(move_amount, 0, 0)
#             self.model_matrix.data = self.model_matrix.data @ m
#         # local rotation (around object center)
#         if self.input.is_key_pressed('u'):
#             m = Matrix.make_rotation_z(turn_amount)
#             self.model_matrix.data = self.model_matrix.data @ m
#         if self.input.is_key_pressed('o'):
#             m = Matrix.make_rotation_z(-turn_amount)
#             self.model_matrix.data = self.model_matrix.data @ m
#         ### Render scene ###
#         GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
#         GL.glUseProgram(self.program_ref)
#         self.projection_matrix.upload_data()
#         self.model_matrix.upload_data()
#         GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertex_count)
#
#
# # Instantiate this class and run the program
# Example().run()
# """

from datetime import datetime
from math import cos, pi, sin, tan
from time import perf_counter
import tkinter as tk
from tkinter import ttk

import numpy as np
from OpenGL import GL
from OpenGL.GL.shaders import compileProgram, compileShader
from pyopengltk import OpenGLFrame


class GLFrame(OpenGLFrame):
    def __init__(self, parent, logger, input_api):
        super().__init__(parent)
        self._logger = logger
        self._input_api = input_api
        self._last_time = perf_counter()
        self._started = False
        self._viewport_size = (1, 1)
        self._program_ref = None
        self._vao_ref = None
        self._vertex_count = 0
        self._projection_loc = -1
        self._model_loc = -1
        self._model_matrix = self._make_translation(0.0, 0.0, -1.0)
        self._projection_matrix = np.identity(4, dtype=np.float32)
        self._move_speed = 0.5
        self._turn_speed = 90.0 * (pi / 180.0)

    def initgl(self):
        self._init_shader_program()
        self._init_geometry()
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        self._projection_loc = GL.glGetUniformLocation(self._program_ref, "projectionMatrix")
        self._model_loc = GL.glGetUniformLocation(self._program_ref, "modelMatrix")
        self.on_resize(self.winfo_width(), self.winfo_height())
        self._logger("INFO", "OpenGL initialized")
        self._logger("INFO", "Controls: WASDZXQE (global), IJKLUO (local)")

    def redraw(self):
        now = perf_counter()
        dt = now - self._last_time
        self._last_time = now

        width, height = self._viewport_size
        GL.glViewport(0, 0, width, height)

        self.update_scene(dt)
        self.draw_scene()
        self._input_api.end_frame()

    def on_resize(self, width, height):
        width = max(1, int(width))
        height = max(1, int(height))
        new_size = (width, height)
        if new_size == self._viewport_size:
            return

        self._viewport_size = new_size
        aspect_ratio = width / float(height)
        self._projection_matrix = self._make_perspective(
            fov_degrees=60.0,
            aspect_ratio=aspect_ratio,
            near=0.1,
            far=100.0,
        )
        self._logger("INFO", f"GL viewport resized: {width}x{height}")

    def update_scene(self, dt):
        if not self._started:
            self._logger("INFO", f"Render loop started (dt={dt:.4f}s)")
            self._started = True

        move_amount = self._move_speed * dt
        turn_amount = self._turn_speed * dt

        if self._input_api.is_key_pressed("w"):
            m = self._make_translation(0.0, move_amount, 0.0)
            self._model_matrix = m @ self._model_matrix
        if self._input_api.is_key_pressed("s"):
            m = self._make_translation(0.0, -move_amount, 0.0)
            self._model_matrix = m @ self._model_matrix
        if self._input_api.is_key_pressed("a"):
            m = self._make_translation(-move_amount, 0.0, 0.0)
            self._model_matrix = m @ self._model_matrix
        if self._input_api.is_key_pressed("d"):
            m = self._make_translation(move_amount, 0.0, 0.0)
            self._model_matrix = m @ self._model_matrix
        if self._input_api.is_key_pressed("z"):
            m = self._make_translation(0.0, 0.0, move_amount)
            self._model_matrix = m @ self._model_matrix
        if self._input_api.is_key_pressed("x"):
            m = self._make_translation(0.0, 0.0, -move_amount)
            self._model_matrix = m @ self._model_matrix
        if self._input_api.is_key_pressed("q"):
            m = self._make_rotation_z(turn_amount)
            self._model_matrix = m @ self._model_matrix
        if self._input_api.is_key_pressed("e"):
            m = self._make_rotation_z(-turn_amount)
            self._model_matrix = m @ self._model_matrix

        if self._input_api.is_key_pressed("i"):
            m = self._make_translation(0.0, move_amount, 0.0)
            self._model_matrix = self._model_matrix @ m
        if self._input_api.is_key_pressed("k"):
            m = self._make_translation(0.0, -move_amount, 0.0)
            self._model_matrix = self._model_matrix @ m
        if self._input_api.is_key_pressed("j"):
            m = self._make_translation(-move_amount, 0.0, 0.0)
            self._model_matrix = self._model_matrix @ m
        if self._input_api.is_key_pressed("l"):
            m = self._make_translation(move_amount, 0.0, 0.0)
            self._model_matrix = self._model_matrix @ m
        if self._input_api.is_key_pressed("u"):
            m = self._make_rotation_z(turn_amount)
            self._model_matrix = self._model_matrix @ m
        if self._input_api.is_key_pressed("o"):
            m = self._make_rotation_z(-turn_amount)
            self._model_matrix = self._model_matrix @ m

    def draw_scene(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glUseProgram(self._program_ref)
        GL.glBindVertexArray(self._vao_ref)
        GL.glUniformMatrix4fv(self._projection_loc, 1, GL.GL_TRUE, self._projection_matrix)
        GL.glUniformMatrix4fv(self._model_loc, 1, GL.GL_TRUE, self._model_matrix)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self._vertex_count)

    def _init_shader_program(self):
        vertex_shader_code = """
            #version 120
            attribute vec3 position;
            uniform mat4 projectionMatrix;
            uniform mat4 modelMatrix;
            void main()
            {
                gl_Position = projectionMatrix * modelMatrix * vec4(position, 1.0);
            }
        """
        fragment_shader_code = """
            #version 120
            void main()
            {
                gl_FragColor = vec4(1.0, 1.0, 0.0, 1.0);
            }
        """
        self._program_ref = compileProgram(
            compileShader(vertex_shader_code, GL.GL_VERTEX_SHADER),
            compileShader(fragment_shader_code, GL.GL_FRAGMENT_SHADER),
        )
        self._logger("INFO", "Shader program compiled")

    def _init_geometry(self):
        position_data = np.array(
            [
                [0.0, 0.2, 0.0],
                [0.1, -0.2, 0.0],
                [-0.1, -0.2, 0.0],
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

    @staticmethod
    def _make_translation(x, y, z):
        matrix = np.identity(4, dtype=np.float32)
        matrix[0, 3] = x
        matrix[1, 3] = y
        matrix[2, 3] = z
        return matrix

    @staticmethod
    def _make_rotation_z(angle_radians):
        c = cos(angle_radians)
        s = sin(angle_radians)
        return np.array(
            [
                [c, -s, 0.0, 0.0],
                [s, c, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            dtype=np.float32,
        )

    @staticmethod
    def _make_perspective(fov_degrees, aspect_ratio, near, far):
        f = 1.0 / tan((fov_degrees * pi / 180.0) * 0.5)
        matrix = np.zeros((4, 4), dtype=np.float32)
        matrix[0, 0] = f / aspect_ratio
        matrix[1, 1] = f
        matrix[2, 2] = (far + near) / (near - far)
        matrix[2, 3] = (2.0 * far * near) / (near - far)
        matrix[3, 2] = -1.0
        return matrix


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
        self.title("3 Global and Local Transformations")
        self.geometry("1000x700")
        self.minsize(640, 480)
        self._last_window_size = (0, 0)
        self._pressed_keys = set()
        self._down_keys = set()
        self._up_keys = set()
        self._create_layout()
        self.bind("<Configure>", self._on_window_resize)
        self.bind_all("<KeyPress>", self._on_key_press)
        self.bind_all("<KeyRelease>", self._on_key_release)
        self.log_panel.log("INFO", "Application started")

    def _create_layout(self):
        paned = ttk.PanedWindow(self, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True)

        gl_host = ttk.Frame(paned)
        log_host = ttk.Frame(paned)
        paned.add(gl_host, weight=7)
        paned.add(log_host, weight=3)

        self.gl_frame = GLFrame(gl_host, logger=self._log, input_api=self)
        self.gl_frame.pack(fill=tk.BOTH, expand=True)
        self.gl_frame.animate = 1

        self.log_panel = LogPanel(log_host)
        self.log_panel.pack(fill=tk.BOTH, expand=True)

        self.after(100, lambda: paned.sashpos(0, int(self.winfo_height() * 0.7)))
        self.after(120, self.gl_frame.focus_set)

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

    def _on_key_press(self, event):
        key = self._normalize_key(event.keysym)
        if key is None:
            return

        if key not in self._pressed_keys:
            self._down_keys.add(key)
        self._pressed_keys.add(key)

    def _on_key_release(self, event):
        key = self._normalize_key(event.keysym)
        if key is None:
            return

        if key in self._pressed_keys:
            self._pressed_keys.remove(key)
            self._up_keys.add(key)

    def is_key_down(self, key):
        return key in self._down_keys

    def is_key_up(self, key):
        return key in self._up_keys

    def is_key_pressed(self, key):
        return key in self._pressed_keys

    def end_frame(self):
        self._down_keys.clear()
        self._up_keys.clear()

    @staticmethod
    def _normalize_key(keysym):
        if not keysym:
            return None
        key = keysym.lower()
        valid_keys = {"w", "a", "s", "d", "z", "x", "q", "e", "i", "j", "k", "l", "u", "o"}
        return key if key in valid_keys else None

    def _log(self, level, message):
        if hasattr(self, "log_panel"):
            self.log_panel.log(level, message)


def main():
    app = GLApp()
    app.mainloop()


if __name__ == "__main__":
    main()
