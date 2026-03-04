import OpenGL.GL as GL
from PIL import Image


class Texture:
    def __init__(self, file_name=None, property_dict=None):
        # Image data source; primarily PIL.Image
        self._surface = None
        # reference of available texture from GPU
        self._texture_ref = GL.glGenTextures(1)
        # default property values
        self._property_dict = {
            "magFilter": GL.GL_LINEAR,
            "minFilter": GL.GL_LINEAR_MIPMAP_LINEAR,
            "wrap": GL.GL_REPEAT
        }
        # Overwrite default property values
        self.set_properties(property_dict or {})
        if file_name is not None:
            self.load_image(file_name)
            self.upload_data()

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, surface):
        self._surface = surface

    @property
    def texture_ref(self):
        return self._texture_ref

    def load_image(self, file_name):
        """ Load image from file """
        with Image.open(file_name) as image:
            self._surface = image.convert("RGBA")

    def set_properties(self, property_dict):
        """ Set property values """
        if property_dict:
            for name, value in property_dict.items():
                if name in self._property_dict.keys():
                    self._property_dict[name] = value
                else:  # unknown property type
                    raise Exception("Texture has no property with name: " + name)

    def upload_data(self):
        """ Upload pixel data to GPU """
        if self._surface is None:
            raise Exception("Texture surface is empty; load an image first.")

        image = self._coerce_to_pil_image(self._surface)
        # OpenGL texture origin is bottom-left, so flip once before upload.
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        # Store image dimensions
        width, height = image.size
        # Convert image data to bytes buffer
        pixel_data = image.tobytes()
        # Specify texture used by the following functions
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture_ref)
        # Send pixel data to texture buffer
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width, height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, pixel_data)
        # Generate mipmap image from uploaded pixel data
        GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
        # Specify technique for magnifying/minifying textures
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, self._property_dict["magFilter"])
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, self._property_dict["minFilter"])
        # Specify what happens to texture coordinates outside range [0, 1]
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, self._property_dict["wrap"])
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, self._property_dict["wrap"])
        # Set default border color to white; important for rendering shadows
        GL.glTexParameterfv(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_BORDER_COLOR, [1, 1, 1, 1])

    @staticmethod
    def _coerce_to_pil_image(surface):
        if isinstance(surface, Image.Image):
            return surface.convert("RGBA")
        raise TypeError("Texture surface must be PIL.Image.Image.")
