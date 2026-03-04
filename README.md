# 책 부록 소스 프로젝트 입니다

- 진행중( WIP, Work on Progress ).  
  + pygame 의존성 제거 중.  
  + ...


## 책 관련 링크  

<img src="https://image.aladin.co.kr/product/34472/32/cover500/1032021462_2.jpg" alt="" height="256px" align="right">

- [ Developing Graphics Frameworks with Python and OpenGL [ YouTube ]](https://www.youtube.com/watch?v=Uy7sFJMulIE&list=PLxpdybrffYlPqkCyvvLfvwsaB7CB1r0pV)  

- [Developing Graphics Frameworks with Python and OpenGL [ 원서 ]](https://library.oapen.org/handle/20.500.12657/48838)  

- [Developing Graphics Frameworks with Python and OpenGL [ 번역서, 없음 ]](https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=344723270)  


## 개발 환경 구축

- 파이썬 ( Python 3.12 )  

  - [Python Download](https://www.python.org/downloads/)  
    - [v3.12.0 for Windows](https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe)  
    - [v3.11.9 for Windows](https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe)  

- ...  


## 의존 패키지

**tkinter 패키지는 내장되어 있어 설치가 불필요합니다.**

```
$ (.venv) pip install PyOpenGL PyOpenGL_accelerate pyopengltk numpy pillow watchdog
```

- PyOpenGL
  - [pypi](https://pypi.org/project/PyOpenGL/)  
    ```
    $ (.venv) pip install PyOpenGL PyOpenGL_accelerate
    ```
  - Standard OpenGL bindings for Python

- pyopengltk
  - [pypi](https://pypi.org/project/pyopengltk/)  
    ```
    $ (.venv) pip install pyopengltk
    ```
  - An opengl frame for pyopengl-tkinter based on ctype

- numpy
  - [pypi](https://pypi.org/project/numpy/)  
    ```
    $ (.venv) pip install numpy
    ```
  - Fundamental Package for Array Computing in Python

- pillow
  - [pypi](https://pypi.org/project/pillow/)  
    ```
    $ (.venv) pip install pillow
    ```
  - Python Imaging Library (fork)

- watchdog  
  - [pypi](https://pypi.org/project/watchdog/)  
    ```
    $ (.venv) pip install watchdog
    ```
  - Filesystem events monitoring

- ...
  - [pypi]()  
    ```
    $ (.venv) pip install ...
    ```
  - [...]()
  - ...  



# OpenGL examples with PyOpenGL and Pygame
The OpenGL examples are based on the book *"Developing Graphics Frameworks with Python and OpenGL"* by Lee Stemkoski and Michael Pascale published by *CRC Press* in 2021. 

The examples cover all the book chapters with code, 2 through 6, with some code changes and demonstrate **GLSL** programming using **PyOpenGL**. **Pygame** is mainly used for control, windowing, and image loading.

You find the examples in the `examples` folder. Just read a class description in a script and run it. Since the object-oriented approach is used, auxiliary classes are logically separated in other folders (packages).

My environment was Python 3.8 with the following packages (without specifying their dependencies here):
```
numpy==1.22.4
pygame==2.1.2
PyOpenGL==3.1.6
PyOpenGL-accelerate==3.1.6
```

The code was tested on the same machine with two operating systems, more precisely:

- OS: Windows 11; Vendor: ATI Technologies Inc.; Renderer: AMD Radeon(TM) Graphics; OpenGL version supported: 4.6.14761 Compatibility Profile Context 21.30.44.03 30.0.13044.3001; GLSL version supported: 4.60

- OS: Ubuntu 20.04.3 LTS; Vendor: AMD; Renderer: AMD RENOIR (DRM 3.41.0, 5.13.0-48-generic, LLVM 12.0.0); OpenGL version supported: 4.6 (Compatibility Profile) Mesa 21.2.6; GLSL version supported: 4.60

Update:

- On Ubuntu, you may encounter the error `OpenGL.error.Error: Attempt to retrieve context when no valid context`.
  See a bug report and suggestions to resolve it: https://github.com/pygame/pygame/issues/3110
