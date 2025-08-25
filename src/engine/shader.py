from OpenGL.GL import *


class Shader:
    """Very simple shader manager (fixed pipeline replacement)."""

    def __init__(self):
        # We are using fixed pipeline OpenGL (no custom GLSL yet)
        pass

    def use(self):
        # No custom shader binding required
        pass

    def set_uniform(self, name, value):
        # Placeholder for future GLSL shader support
        pass
