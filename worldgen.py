import pygame
import numpy as np
import noise
from settings import *


class World:
    def __init__(self, width, height, seed, colors):
        """

        :param width:
        :param height:
        :param seed:
        :param colors:
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.world_map = None
        self.chunks_array = []
        self.colors = colors
        self.generate_map()

    def generate_map(self):
        scale = 100.0
        self.world_map = np.zeros((self.height, self.width))

        for x in range(self.width):
            for y in range(self.height):
                self.world_map[y, x] = noise.pnoise2(
                    x / scale,
                    y / scale,
                    octaves=6,
                    persistence=0.5,
                    lacunarity=2.0,
                    repeatx=1024,
                    repeaty=1024,
                    base=self.seed
                )

        for chunk_x in range(0, self.width, CHUNK_SIZE):
            row = []
            for chunk_y in range(0, self.height, CHUNK_SIZE):
                row.append((chunk_x, chunk_y))
            self.chunks_array.append(row)

    def get_terrain_color(self, height_value):
        if height_value < -0.15:
            return self.colors["ocean"]
        elif height_value < 0.01:
            return self.colors["sand"]
        elif height_value < 0.15:
            return self.colors["grass"]
        elif height_value < 0.35:
            return self.colors["forest"]
        else:
            return self.colors["mountain"]

    def draw_chunk(self, screen, chunk_x, chunk_y, highlight=False):
        for x in range(chunk_x, min(chunk_x + CHUNK_SIZE, self.width)):
            for y in range(chunk_y, min(chunk_y + CHUNK_SIZE, self.height)):
                height_value = self.world_map[y, x]
                color = self.get_terrain_color(height_value)
                if highlight:
                    color = lighten_color(color)
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


def lighten_color(color, factor=1.2):
    return tuple(min(int(c * factor), 255) for c in color)
