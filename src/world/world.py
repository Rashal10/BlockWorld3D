import pygame
from pygame.math import Vector3
import random


class World:
    BLOCK_SIZE = 20
    COLORS = {
        "dirt": (139, 69, 19),
        "grass": (34, 139, 34),
        "wood": (160, 82, 45),
        "leaves": (34, 180, 34),
        "air": (0, 0, 0, 0),
    }

    def __init__(self, width=32, depth=32, height=8):
        self.width = width
        self.depth = depth
        self.height = height

        # Dictionary {(x, y, z): block_type}
        self.blocks = {}

        self.generate_flat_world()
        self.generate_trees(8)

    def generate_flat_world(self):
        for x in range(self.width):
            for z in range(self.depth):
                self.blocks[(x, 0, z)] = "dirt"
                self.blocks[(x, 1, z)] = "grass"

    def generate_trees(self, count=5):
        for _ in range(count):
            x = random.randint(2, self.width - 3)
            z = random.randint(2, self.depth - 3)

            # Trunk
            for y in range(2, 5):
                self.blocks[(x, y, z)] = "wood"

            # Leaves
            for dx in range(-2, 3):
                for dz in range(-2, 3):
                    if abs(dx) + abs(dz) < 4:
                        self.blocks[(x + dx, 5, z + dz)] = "leaves"

    def get_block(self, x, y, z):
        return self.blocks.get((x, y, z), "air")

    def set_block(self, x, y, z, block_type):
        if y < 0 or y >= self.height:
            return False
        self.blocks[(x, y, z)] = block_type
        return True

    def break_block(self, player):
        """Break block at player position (simulate digging)"""
        target = player.pos + player.facing
        block_x, block_y, block_z = int(target.x), int(target.y), int(target.z)

        block_type = self.get_block(block_x, block_y, block_z)
        if block_type != "air":
            del self.blocks[(block_x, block_y, block_z)]
            return block_type
        return None

    def draw(self, player, screen):
        """Simple 2D top-down view"""
        for (x, y, z), block_type in self.blocks.items():
            if block_type == "air":
                continue

            color = self.COLORS.get(block_type, (200, 200, 200))
            rect = pygame.Rect(
                x * self.BLOCK_SIZE,
                z * self.BLOCK_SIZE,
                self.BLOCK_SIZE,
                self.BLOCK_SIZE,
            )
            pygame.draw.rect(screen, color, rect)

        # Draw player as red square
        px = int(player.pos.x * self.BLOCK_SIZE)
        pz = int(player.pos.z * self.BLOCK_SIZE)
        pygame.draw.rect(
            screen, (255, 0, 0), (px, pz, self.BLOCK_SIZE, self.BLOCK_SIZE)
        )
    