import pygame
from pygame.math import Vector3


class Player:
    def __init__(self, x=0, y=2, z=0):
        self.pos = Vector3(x, y, z)
        self.speed = 0.15

        # Inventory
        self.inventory = {"dirt": 0, "grass": 0, "wood": 0, "leaves": 0}

        # Facing direction (for placing blocks)
        self.facing = Vector3(0, 0, 1)

    def update(self, keys, world):
        """Basic WASD + space movement"""
        move = Vector3(0, 0, 0)

        if keys[pygame.K_w]:
            move.z -= 1
        if keys[pygame.K_s]:
            move.z += 1
        if keys[pygame.K_a]:
            move.x -= 1
        if keys[pygame.K_d]:
            move.x += 1

        if move.length() > 0:
            move = move.normalize() * self.speed

        # Apply move but prevent going underground
        new_pos = self.pos + move
        if new_pos.y < 2:
            new_pos.y = 2
        self.pos = new_pos

    def add_to_inventory(self, block_type):
        if block_type in self.inventory:
            self.inventory[block_type] += 1

    def remove_from_inventory(self, block_type):
        if block_type in self.inventory and self.inventory[block_type] > 0:
            self.inventory[block_type] -= 1
            return block_type
        return None

    def place_block(self, world):
        """Place block one step in front of player"""
        target = self.pos + self.facing
        block_x, block_y, block_z = int(target.x), int(target.y), int(target.z)

        # Try to place dirt by default (can be expanded later)
        for block_type in self.inventory:
            if self.inventory[block_type] > 0:
                if world.set_block(block_x, block_y, block_z, block_type):
                    return block_type
        return None
