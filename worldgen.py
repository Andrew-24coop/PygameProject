import numpy as np
import noise
import pygame
from settings import *


class World:
    def __init__(self, width, height, seed):
        self.width = width
        self.height = height
        self.seed = seed
        self.world_map = self.generate_map()

    def generate_map(self):
        world_map = np.zeros((self.height, self.width))
        scale = 100.0
        for x in range(self.width):
            for y in range(self.height):
                world_map[y][x] = noise.pnoise2(x / scale,
                                                y / scale,
                                                octaves=6,
                                                persistence=0.5,
                                                lacunarity=2.0,
                                                repeatx=1024,
                                                repeaty=1024,
                                                base=self.seed)
        return world_map

    def get_terrain_color(self, height_value):
        if height_value < -0.1:
            return COLORS["ocean"]
        elif height_value < 0.01:
            return COLORS["sand"]
        elif height_value < 0.15:
            return COLORS["grass"]
        elif height_value < 0.35:
            return COLORS["forest"]
        else:
            return COLORS["mountain"]

    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                height_value = self.world_map[y][x]
                color = self.get_terrain_color(height_value)
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
