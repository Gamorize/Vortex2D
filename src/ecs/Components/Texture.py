from OpenGL.GL import *
from PIL import Image
from base import Component

class Texture(Component):
    def __init__(self, texture_path):
        self.texture_path = texture_path
        self.image_width = None
        self.image_height = None
        self.texture_id = self.load_texture(texture_path)

    def load_texture(self, path):
        # Load image using PIL
        image = Image.open(path).convert('RGBA')
        self.image_width, self.image_height = image.size
        image_data = image.tobytes()

        # Generate and bind texture
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Upload image data to GPU
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.image_width, self.image_height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        return texture_id

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

    def __del__(self):
        # Cleanup GPU resource
        if hasattr(self, 'texture_id') and self.texture_id:
            glDeleteTextures([self.texture_id])
