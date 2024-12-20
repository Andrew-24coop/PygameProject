import pygame
import numpy as np
import noise
from settings import *


class World:
    def __init__(self, width, height, seed):
        self.width = width
        self.height = height
        self.seed = seed
        self.world_map = None  # 2D array of the terrain
        self.chunks_array = []  # Array to store all chunks
        self.generate_map()

    def generate_map(self):
        """Generate the entire world and organize it into chunks."""
        scale = 100.0
        self.world_map = np.zeros((self.height, self.width))  # Create a 2D array for the map

        # Populate the world map with height values
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

        # Create an array of chunks
        for chunk_x in range(0, self.width, CHUNK_SIZE):
            row = []
            for chunk_y in range(0, self.height, CHUNK_SIZE):
                row.append((chunk_x, chunk_y))
            self.chunks_array.append(row)

    def get_terrain_color(self, height_value):
        """Get the color for the given terrain height value."""
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

    def lighten_color(self, color, factor=1.2):
        """Lighten a given color by a factor."""
        return tuple(min(int(c * factor), 255) for c in color)

    def draw_chunk(self, screen, chunk_x, chunk_y, highlight=False):
        """Draw a specific chunk, optionally lightening it."""
        for x in range(chunk_x, min(chunk_x + CHUNK_SIZE, self.width)):
            for y in range(chunk_y, min(chunk_y + CHUNK_SIZE, self.height)):
                height_value = self.world_map[y, x]
                color = self.get_terrain_color(height_value)
                if highlight:
                    color = self.lighten_color(color)
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
