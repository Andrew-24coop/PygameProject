import random
import pygame
from worldgen import World
from settings import *


def main():
    pygame.init()
    pygame.display.set_caption("Rise of Empire")
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    world = World(WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE, SEED)

    world.draw(screen)
    """
    for x in range(0, WIDTH, CHUNK_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CHUNK_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (0, y), (WIDTH, y))
    """

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_pos = pygame.mouse.get_pos()
        mouse_x = (mouse_pos[0] // CHUNK_SIZE) * CHUNK_SIZE
        mouse_y = (mouse_pos[1] // CHUNK_SIZE) * CHUNK_SIZE
        # world.draw(screen)
        # pygame.draw.rect(screen, (255, 0, 0, 10), (mouse_x + 1, mouse_y + 1, CHUNK_SIZE - 1, CHUNK_SIZE - 1))

        for x in range(0, WIDTH, CHUNK_SIZE):
            pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CHUNK_SIZE):
            pygame.draw.line(screen, (255, 255, 255), (0, y), (WIDTH, y))

        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
