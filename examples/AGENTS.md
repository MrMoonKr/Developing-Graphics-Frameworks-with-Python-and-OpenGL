# AGENTS.md

## Project Overview

This repository contains educational OpenGL examples written in Python.

The original examples use **pygame + OpenGL**.

The goal of this project is to **refactor the examples to use**:

- tkinter
- pyopengltk
- OpenGL
- GLSL shaders

while **preserving the original code for learning comparison**.

This repository is intended for **repeated learning of OpenGL concepts**.

---

## Scope

This file applies **only to the `examples/` directory**.

Do not modify other parts of the repository unless explicitly requested.

---

## Refactoring Goal

Convert pygame-based OpenGL examples into a structure using:

- tkinter
- pyopengltk
- OpenGL
- GLSL

while keeping the original example code inside the file.

---

## Critical Rule

**NEVER delete original example code.**

The original code must always remain in the file inside a preserved block.

Example format:

```python
# """
# Original Code (Preserved)
# <original pygame example code here>
# """
```

---

## Required File Structure

Each example must follow this structure.

`examples/template-example.py` is the canonical class template and must be preserved during refactoring.

Required order:

1. Original Code (comment block)
2. imports
3. `GLFrame` class
4. `LogPanel` class
5. `GLApp` class
6. `main()` function

Example layout:

```python
# Original Code

# imports

class GLFrame:
    ...

class LogPanel:
    ...

class GLApp:
    ...

def main():
    ...

if __name__ == "__main__":
    main()
```

Class signatures and method names must match `template-example.py`:

- `class GLFrame(OpenGLFrame)`
- `class LogPanel(ttk.Frame)`
- `class GLApp(tk.Tk)`
- `GLFrame` methods: `initgl()`, `redraw()`, `on_resize(width, height)`, `update_scene(dt)`, `draw_scene()`
- `GLApp` methods: `__init__()`, `_create_layout()`, `_on_window_resize(event)`, `on_window_resized(width, height)`

---

## GUI Architecture

Each example must implement this GUI layout:

```text
GLApp (tk.Tk)
└─ PanedWindow (vertical)
   ├─ OpenGL Frame (70%)
   └─ Log Panel (30%)
```

The OpenGL area should occupy approximately **70% of the window height**.

The log panel should occupy approximately **30%**.

---

## Log Panel Requirements

The log panel must use:

- `ttk.Treeview`

Required columns:

- `Time`
- `Level`
- `Message`

Example:

| Time | Level | Message |
|------|-------|---------|
| 12:01:10 | INFO | Application Started |
| 12:01:11 | INFO | OpenGL Initialized |

The log panel must support automatic scrolling.

---

## OpenGL Frame Requirements

OpenGL rendering must use:

- `pyopengltk.OpenGLFrame`

Rendering methods must follow this pattern:

- `initgl()`
- `redraw()`
- `update_scene(dt)`
- `draw_scene()`

Example render loop:

- `initgl()` -> initialize OpenGL
- `redraw()` -> frame update
- `update_scene()` -> update logic
- `draw_scene()` -> render objects

---

## Application Class

The application must use:

- `class GLApp(tk.Tk)`

Example structure:

```python
class GLApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OpenGL Example")
        self._create_layout()

    def _create_layout(self):
        ...
```

The GUI must be created inside `_create_layout()`.

---

## Entry Point

Each example must include a main function.

```python
def main():
    app = GLApp()
    app.mainloop()

if __name__ == "__main__":
    main()
```

---

## Logging Requirements

Examples should log important events such as:

- application start
- OpenGL initialization
- shader compilation
- rendering updates
- errors

Example:

```python
logger.log("INFO", "OpenGL Initialized")
```

---

## Coding Style

Always use these imports:

```python
import tkinter as tk
from tkinter import ttk
```

Avoid using:

```python
from tkinter import *
```

Class naming conventions:

- `ExampleApp`
- `GLFrame`
- `LogPanel`

---

## OpenGL Modernization

Original examples may use **fixed pipeline OpenGL**:

- `glBegin()`
- `glVertex()`
- `glEnd()`

When possible, agents may introduce **GLSL-based rendering** using:

- `VBO`
- `VAO`
- `Shaders`

However, the fixed pipeline example may remain if the purpose is educational.

---

## Educational Priority

This repository prioritizes **learning clarity over abstraction**.

Do not introduce unnecessary frameworks or engine-like layers.

Each example file should remain **self-contained and readable**.

---

## File Naming Convention

Example files should follow numbered order:

- `01_triangle.py`
- `02_square.py`
- `03_texture.py`
- `04_camera.py`
- `05_shader.py`

---

## Things Agents Must NOT Do

Agents must NOT:

- remove original code
- introduce complex frameworks
- split examples into many files
- modify unrelated folders

---

## Expected Outcome

After refactoring, each example should:

- run as a tkinter application
- display an OpenGL rendering area
- include a log panel
- preserve the original pygame code
- demonstrate OpenGL concepts clearly

---

## Example Execution

Run an example with:

```bash
python examples/01_triangle.py
```

---

## End of File
