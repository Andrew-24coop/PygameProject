from worldgen import World
from settings import *
from person import *
from mushroom import *
import pygame


def draw_grid(screen, zoom=1, offset=(0, 0)):
    grid_size = CHUNK_SIZE * TILE_SIZE * zoom
    start_x = -offset[0] % grid_size
    start_y = -offset[1] % grid_size
    for x in range(start_x, WIDTH, grid_size):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
    for y in range(start_y, HEIGHT, grid_size):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))


def main():
    pygame.init()
    pygame.display.set_caption("Rise of Empire")
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    world = World(WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE, SEED)

    # Initialize player and mushroom
    player = MainHero(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)
    mushroom = Mushroom(player, 800, 400, WIDTH, HEIGHT)
    player.lightning.target = mushroom

    sprites_all = pygame.sprite.Group(player, mushroom)

    zoom = 1
    zoom_chunk = None
    offset = (0, 0)
    prev_chunk = None

    def draw_world():
        screen.fill((0, 0, 0))
        if zoom == 1:
            # Draw the entire map in zoomed-out view
            for chunk_row in world.chunks_array:
                for chunk in chunk_row:
                    cx, cy = chunk
                    world.draw_chunk(screen, cx, cy)
            draw_grid(screen)
        else:
            # Draw only the zoomed-in region
            x_chunk, y_chunk = zoom_chunk
            start_x = max(0, x_chunk - CHUNK_SIZE)
            end_x = min(world.width, x_chunk + CHUNK_SIZE * 2)
            start_y = max(0, y_chunk - CHUNK_SIZE)
            end_y = min(world.height, y_chunk + CHUNK_SIZE * 2)

            for x in range(start_x, end_x):
                for y in range(start_y, end_y):
                    if 0 <= x < world.width and 0 <= y < world.height:
                        height_value = world.world_map[y, x]
                        color = world.get_terrain_color(height_value)
                        screen_x = (x * TILE_SIZE * zoom - offset[0])
                        screen_y = (y * TILE_SIZE * zoom - offset[1])
                        pygame.draw.rect(
                            screen,
                            color,
                            (
                                screen_x,
                                screen_y,
                                TILE_SIZE * zoom,
                                TILE_SIZE * zoom,
                            ),
                        )
            draw_grid(screen, zoom, offset)

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

                        # Center the selected chunk
                        center_x = chunk_x * TILE_SIZE + (CHUNK_SIZE * TILE_SIZE) // 2
                        center_y = chunk_y * TILE_SIZE + (CHUNK_SIZE * TILE_SIZE) // 2
                        offset = (
                            center_x * zoom - WIDTH // 2,
                            center_y * zoom - HEIGHT // 2,
                        )

                        prev_chunk = None
                        draw_world()
                        pygame.display.flip()
            elif event.type == pygame.KEYUP:
                player.is_move = False
                player.moving_frame = 2
                player.keyboard_up = True

        player.check_keyboard()

        # Center the player
        if zoom > 1:
            offset = (
                player.rect.centerx * zoom - WIDTH // 2,
                player.rect.centery * zoom - HEIGHT // 2,
            )

        # Draw the world
        draw_world()

        # Draw player and mushroom only if zoomed in
        if zoom > 1:
            sprites_all.update()
            sprites_all.draw(screen)

        # Highlight the chunk under the player
        if zoom == 1:
            chunk_x = (player.rect.centerx // (CHUNK_SIZE * TILE_SIZE)) * CHUNK_SIZE
            chunk_y = (player.rect.centery // (CHUNK_SIZE * TILE_SIZE)) * CHUNK_SIZE
            current_chunk = (chunk_x, chunk_y)
            if current_chunk != prev_chunk:
                if prev_chunk:
                    world.draw_chunk(screen, prev_chunk[0], prev_chunk[1])
                world.draw_chunk(screen, chunk_x, chunk_y, highlight=True)
                draw_grid(screen)
                prev_chunk = current_chunk
                pygame.display.flip()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
