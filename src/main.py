import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutInit
import random
import math

from engine.window import Window

# Block types (RGB colors for now)
BLOCK_COLORS = {
    "grass": (95, 159, 53),
    "dirt": (134, 96, 67),
    "wood": (100, 70, 40),
    "leaves": (50, 160, 50),
}


class World:
    def __init__(self, size=32):
        self.blocks = []
        self.size = size
        self.generate_flat_world()

    def generate_flat_world(self):
        """Generate flat land with random trees."""
        for x in range(self.size):
            for z in range(self.size):
                self.blocks.append(("grass", x, 0, z))   # ground
                self.blocks.append(("dirt", x, -1, z))  # dirt below

                # Random tree
                if random.random() < 0.05 and 2 < x < self.size-2 and 2 < z < self.size-2:
                    self.add_tree(x, 1, z)

    def add_tree(self, x, y, z):
        """Simple tree: trunk + leaves cube"""
        height = random.randint(3, 4)
        for i in range(height):
            self.blocks.append(("wood", x, y + i, z))
        # leaves
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                for dy in range(2, 5):
                    if abs(dx) + abs(dz) < 4:
                        self.blocks.append(("leaves", x + dx, y + height - 2 + dy, z + dz))

    def draw(self, window):
        for block_type, x, y, z in self.blocks:
            color = BLOCK_COLORS.get(block_type, (200, 200, 200))
            window.draw_cube(x, y, z, 1, color)


class Camera:
    def __init__(self, x=0, y=2, z=5):
        self.x, self.y, self.z = x, y, z
        self.pitch, self.yaw = 0, 0  # looking direction

    def move(self, dx, dy, dz):
        """Move relative to camera yaw"""
        rad = math.radians(self.yaw)
        self.x += dx * math.cos(rad) - dz * math.sin(rad)
        self.z += dx * math.sin(rad) + dz * math.cos(rad)
        self.y += dy

    def apply(self):
        """Apply camera transformation"""
        glRotatef(-self.pitch, 1, 0, 0)
        glRotatef(-self.yaw, 0, 1, 0)
        glTranslatef(-self.x, -self.y, -self.z)


def main():
    glutInit()
    window = Window(1280, 720, "BlockWorld 3D - Minecraft Style")
    world = World(32)
    camera = Camera(5, 3, 10)

    pygame.event.set_grab(True)  # lock mouse
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()
    running = True
    move_forward = move_backward = move_left = move_right = False

    while running:
        dx, dy = pygame.mouse.get_rel()  # mouse movement
        camera.yaw += dx * 0.1
        camera.pitch -= dy * 0.1
        camera.pitch = max(-89, min(89, camera.pitch))  # clamp

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_w: move_forward = True
                elif event.key == K_s: move_backward = True
                elif event.key == K_a: move_left = True
                elif event.key == K_d: move_right = True
            elif event.type == KEYUP:
                if event.key == K_w: move_forward = False
                elif event.key == K_s: move_backward = False
                elif event.key == K_a: move_left = False
                elif event.key == K_d: move_right = False

        # Movement
        speed = 0.2
        if move_forward: camera.move(0, 0, -speed)
        if move_backward: camera.move(0, 0, speed)
        if move_left: camera.move(-speed, 0, 0)
        if move_right: camera.move(speed, 0, 0)

        # Draw world
        window.clear()
        glLoadIdentity()
        camera.apply()
        world.draw(window)
        window.swap_buffers()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
