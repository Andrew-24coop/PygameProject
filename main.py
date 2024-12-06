import pygame
import numpy as np
import random
from noise import pnoise2

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 10
WORLD_WIDTH = WIDTH // TILE_SIZE
WORLD_HEIGHT = HEIGHT // TILE_SIZE

TERRAIN_COLORS = {
    "water": (0, 0, 255),
    "sand": (255, 255, 100),
    "grass": (0, 255, 0),
    "forest": (0, 100, 0),
    "mountain": (139, 137, 137),
}


class Biome:
    def __init__(self, seed):
        self.world = self.generate_world(seed)

    def generate_world(self, seed):
        world = np.zeros((WORLD_HEIGHT, WORLD_WIDTH))
        for y in range(WORLD_HEIGHT):
            for x in range(WORLD_WIDTH):
                noise_value = pnoise2((x + seed) / 20, (y + seed) / 20, octaves=6)
                world[y][x] = noise_value
        return world

    def get_biome(self, value):
        print(value)
        if value < -0.05:
            return 'water'
        elif value < 0:
            return 'sand'
        elif value < 0.3:
            return 'grass'
        elif value < 0.5:
            return 'forest'
        else:
            return 'mountain'

    def draw(self, screen):
        for y in range(WORLD_HEIGHT):
            for x in range(WORLD_WIDTH):
                value = self.world[y][x]
                biome = self.get_biome(value)
                color = TERRAIN_COLORS[biome]
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("World Generation with Biomes")
    clock = pygame.time.Clock()

    seed = random.randint(0, 10000)
    biome = Biome(seed)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        biome.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
