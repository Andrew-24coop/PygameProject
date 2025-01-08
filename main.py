from worldgen import World
from settings import *
import pygame


def draw_grid(screen, zoom=1, offset=(0, 0)):
    grid_size = CHUNK_SIZE * TILE_SIZE * zoom
    for x in range(-offset[0], WIDTH, grid_size):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
    for y in range(-offset[1], HEIGHT, grid_size):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))


def main():
    pygame.init()
    pygame.display.set_caption("Rise of Empire")
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    world = World(WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE, SEED)

    zoom = 1
    zoom_chunk = None
    offset = (0, 0)
    prev_chunk = None

    def draw_world():
        screen.fill((0, 0, 0))
        if zoom == 1:
            for chunk_row in world.chunks_array:
                for chunk in chunk_row:
                    cx, cy = chunk
                    world.draw_chunk(screen, cx, cy)
            draw_grid(screen)
        else:
            chunk_x, chunk_y = zoom_chunk
            start_x = max(0, chunk_x - CHUNK_SIZE)
            end_x = min(world.width, chunk_x + 2 * CHUNK_SIZE)
            start_y = max(0, chunk_y)
            end_y = min(world.height, chunk_y + CHUNK_SIZE)

            for x in range(start_x, end_x):
                for y in range(start_y, end_y):
                    if 0 <= x < world.width and 0 <= y < world.height:
                        height_value = world.world_map[y, x]
                        color = world.get_terrain_color(height_value)
                        pygame.draw.rect(
                            screen,
                            color,
                            (
                                (x - start_x) * TILE_SIZE * zoom - offset[0],
                                (y - start_y) * TILE_SIZE * zoom - offset[1],
                                TILE_SIZE * zoom,
                                TILE_SIZE * zoom,
                            ),
                        )
            draw_grid(screen, zoom, offset)

    draw_world()
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    zoom = 1
                    zoom_chunk = None
                    offset = (0, 0)
                    prev_chunk = None
                    draw_world()
                    pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if zoom == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        chunk_x = (mouse_pos[0] // (CHUNK_SIZE * TILE_SIZE)) * CHUNK_SIZE
                        chunk_y = (mouse_pos[1] // (CHUNK_SIZE * TILE_SIZE)) * CHUNK_SIZE
                        zoom_chunk = (chunk_x, chunk_y)
                        zoom = HEIGHT // (CHUNK_SIZE * TILE_SIZE)
                        center_offset_x = WIDTH // 2 - CHUNK_SIZE * TILE_SIZE * zoom // 2
                        offset = (center_offset_x, 0)
                        prev_chunk = None
                        draw_world()
                        pygame.display.flip()
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0] and zoom > 1:
                    dx, dy = event.rel
                    offset = (offset[0] + dx, offset[1] + dy)
                    draw_world()
                    pygame.display.flip()

        if zoom == 1:
            mouse_pos = pygame.mouse.get_pos()
            chunk_x = (mouse_pos[0] // (CHUNK_SIZE * TILE_SIZE)) * CHUNK_SIZE
            chunk_y = (mouse_pos[1] // (CHUNK_SIZE * TILE_SIZE)) * CHUNK_SIZE
            current_chunk = (chunk_x, chunk_y)
            if current_chunk != prev_chunk:
                if prev_chunk:
                    world.draw_chunk(screen, prev_chunk[0], prev_chunk[1])
                world.draw_chunk(screen, chunk_x, chunk_y, highlight=True)
                draw_grid(screen)
                prev_chunk = current_chunk
                pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
