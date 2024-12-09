import random
import pygame
import numpy as np
import noise

WIDTH, HEIGHT = 1000, 600
TILE_SIZE = 1
MAIN_TILE_SIZE = 50

COLORS = {
    "ocean": (0, 0, 255),
    "sand": (194, 178, 128),
    "grass": (34, 139, 34),
    "forest": (0, 100, 0),
    "mountain": (139, 137, 137)
}


def generate_map(width, height, seed):
    world_map = np.zeros((height, width))
    scale = 100.0
    for x in range(width):
        for y in range(height):
            world_map[y][x] = noise.pnoise2(x / scale,
                                            y / scale,
                                            octaves=6,
                                            persistence=0.5,
                                            lacunarity=2.0,
                                            repeatx=1024,
                                            repeaty=1024,
                                            base=seed)  # Используем семя
    return world_map


def get_terrain_color(height_value):
    if height_value < -0.1:
        return COLORS["ocean"]
    elif height_value < 0.01:
        return COLORS["sand"]
    elif height_value < 0.2:
        return COLORS["grass"]
    elif height_value < 0.4:
        return COLORS["forest"]
    else:
        return COLORS["mountain"]


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Realistic World Generation")
    clock = pygame.time.Clock()

    seed = random.randint(0, 255)

    world_map = generate_map(WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE, seed)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for y in range(HEIGHT // TILE_SIZE):
            for x in range(WIDTH // TILE_SIZE):
                height_value = world_map[y][x]
                color = get_terrain_color(height_value)
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        for x in range(0, WIDTH, MAIN_TILE_SIZE):
            pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, MAIN_TILE_SIZE):
            pygame.draw.line(screen, (255, 255, 255), (0, y), (WIDTH, y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
