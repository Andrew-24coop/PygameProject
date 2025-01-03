# import random
from worldgen import World
from settings import *
import pygame


def draw_grid(screen):
    """Draw grid lines across the map."""
    for x in range(0, WIDTH, CHUNK_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CHUNK_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))


def main():
    pygame.init()
    pygame.display.set_caption("Rise of Empire")
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    world = World(WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE, SEED)
    for chunk_row in world.chunks_array:
        for chunk in chunk_row:
            cx, cy = chunk
            world.draw_chunk(screen, cx, cy)
    draw_grid(screen)
    pygame.display.flip()

    prev_chunk = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_pos = pygame.mouse.get_pos()
        chunk_x = (mouse_pos[0] // CHUNK_SIZE) * CHUNK_SIZE
        chunk_y = (mouse_pos[1] // CHUNK_SIZE) * CHUNK_SIZE
        current_chunk = (chunk_x, chunk_y)

        if current_chunk != prev_chunk:
            if prev_chunk:
                world.draw_chunk(screen, prev_chunk[0], prev_chunk[1])
            world.draw_chunk(screen, chunk_x, chunk_y, highlight=True)
            draw_grid(screen)
            prev_chunk = current_chunk

        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
