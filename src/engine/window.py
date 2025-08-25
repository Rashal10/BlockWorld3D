from OpenGL.GL import *

class Window:
    def __init__(self, width, height, title):
        from OpenGL.GLUT import glutInit
        import pygame
        pygame.init()
        pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(title)

        glEnable(GL_DEPTH_TEST)

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def swap_buffers(self):
        import pygame
        pygame.display.flip()

    def draw_cube(self, x, y, z, size, color):
        """Draw cube at (x,y,z) with RGB color"""
        r, g, b = [c / 255 for c in color]
        glColor3f(r, g, b)

        hs = size / 2  # half size
        vertices = [
            (x - hs, y - hs, z - hs),
            (x + hs, y - hs, z - hs),
            (x + hs, y + hs, z - hs),
            (x - hs, y + hs, z - hs),
            (x - hs, y - hs, z + hs),
            (x + hs, y - hs, z + hs),
            (x + hs, y + hs, z + hs),
            (x - hs, y + hs, z + hs),
        ]

        faces = [
            (0, 1, 2, 3),  # back
            (4, 5, 6, 7),  # front
            (0, 1, 5, 4),  # bottom
            (2, 3, 7, 6),  # top
            (1, 2, 6, 5),  # right
            (0, 3, 7, 4),  # left
        ]

        glBegin(GL_QUADS)
        for face in faces:
            for v in face:
                glVertex3fv(vertices[v])
        glEnd()
