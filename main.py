import random
import pygame
from worldgen import World
from settings import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Realistic World Generation")
    clock = pygame.time.Clock()

    seed = random.randint(0, 255)
    world = World(WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE, seed)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        world.draw(screen)

        for x in range(0, WIDTH, 50):
            pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 50):
            pygame.draw.line(screen, (255, 255, 255), (0, y), (WIDTH, y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
