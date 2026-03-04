from PIL import Image, ImageDraw, ImageFont

from py3d.core_ext.texture import Texture

class TextTexture(Texture):
    """
    Define a text texture by using Pillow
    """
    def __init__(self, text="Python graphics",
                 system_font_name="Arial",
                 font_file_name=None,
                 font_size=24,
                 font_color=(0, 0, 0),
                 background_color=(255, 255, 255),
                 transparent=False,
                 image_width=None,
                 image_height=None,
                 align_horizontal=0.0,
                 align_vertical=0.0,
                 image_border_width=0,
                 image_border_color=(0, 0, 0)):
        super().__init__()

        # Load font from file if available, otherwise try a system-like font, then fallback.
        if font_file_name is not None:
            font = ImageFont.truetype(font_file_name, font_size)
        else:
            try:
                font = ImageFont.truetype(system_font_name, font_size)
            except OSError:
                font = ImageFont.load_default()

        # Measure text bounds.
        scratch = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        scratch_draw = ImageDraw.Draw(scratch)
        left, top, right, bottom = scratch_draw.textbbox((0, 0), text, font=font)
        text_width = right - left
        text_height = bottom - top

        # If image dimensions are not specified,
        # use the text bounds size as default.
        if image_width is None:
            image_width = text_width
        if image_height is None:
            image_height = text_height

        # Create target image with alpha channel.
        if transparent:
            background_rgba = (0, 0, 0, 0)
        else:
            background_rgba = (*background_color, 255)
        self._surface = Image.new("RGBA", (image_width, image_height), background_rgba)
        draw = ImageDraw.Draw(self._surface)

        # Set a background color used when not transparent
        # Attributes align_horizontal, align_vertical define percentages,
        # measured from top-left corner.
        x = align_horizontal * (image_width - text_width)
        y = align_vertical * (image_height - text_height)

        # Add border (optionally)
        if image_border_width > 0:
            draw.rectangle(
                [0, 0, image_width - 1, image_height - 1],
                outline=image_border_color,
                width=image_border_width,
            )

        # Draw text at aligned location.
        draw.text((x - left, y - top), text, fill=font_color, font=font)
        self.upload_data()

