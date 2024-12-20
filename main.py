# import random
from worldgen import World
from settings import *
import pygame


def draw_grid(screen):
    """Draw grid lines across the map."""
    for x in range(0, WIDTH, CHUNK_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))  # Vertical lines
    for y in range(0, HEIGHT, CHUNK_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))  # Horizontal lines


def main():
    pygame.init()
    pygame.display.set_caption("Rise of Empire")
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    world = World(WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE, SEED)

    # Draw the entire map and grid at the start
    for chunk_row in world.chunks_array:
        for chunk in chunk_row:
            cx, cy = chunk
            world.draw_chunk(screen, cx, cy)
    draw_grid(screen)
    pygame.display.flip()  # Ensure the initial map is displayed

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
            # Redraw the previous chunk
            if prev_chunk:
                world.draw_chunk(screen, prev_chunk[0], prev_chunk[1])

            # Redraw the current chunk with a highlight
            world.draw_chunk(screen, chunk_x, chunk_y, highlight=True)

            # Redraw the grid to ensure it's on top
            draw_grid(screen)

            # Update the previous chunk to the current one
            prev_chunk = current_chunk

        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
