from pygame import font
from worldgen import World
from Final_boss import Dragon
from Portal import Portal
from person import *
from mob import *
from death_window import DeathWindow
from mushroom import *

def draw_grid(screen, zoom=1, offset=(0, 0)):
    grid_size = CHUNK_SIZE * TILE_SIZE * zoom
    start_x = -offset[0] % grid_size
    start_y = -offset[1] % grid_size
    for x in range(start_x, WIDTH, grid_size):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
    for y in range(start_y, HEIGHT, grid_size):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))


def main():
    try:
        # del menu.button1
        # del menu.button2
        # del menu.button3
        # del menu
        pygame.init()
        font.init()
        pygame.display.set_caption("Rise of Empire")
        pygame.mixer.music.stop()
        screen = pygame.display.set_mode(SIZE)
        clock = pygame.time.Clock()

        # pygame.mixer.init()
        # pygame.mixer.music.load("sounds/boss_fight_music.mp3")
        # pygame.mixer.music.play(-1)

        main_world = World(WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE, MAIN_SEED, MAIN_COLORS)
        boss_world = World(WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE, BOSS_SEED, BOSS_COLORS)
        current_world = main_world

        player = MainHero(500, 300, WIDTH, HEIGHT)
        mushrooms = Mushrooom_group()

        portal = Portal(randint(-2500, 2500), randint(-2500, 2500),
                        player, main_world, boss_world)
        death_window = DeathWindow(screen)
        boss = Dragon(player, randint(300, 1000), randint(300, 1000), WIDTH, HEIGHT)
        dragon.add(boss)

        cows = MobGroup("cow", player, mobs)
        pigs = MobGroup("pig", player, mobs)
        pigs.spawn(100)
        cows.spawn(100)

        zoom = 1
        zoom_chunk = None
        offset = (0, 0)
        prev_chunk = None

        fps_font = font.Font("fonts/Anta-Regular.ttf", 20)
        coords_font = font.Font("fonts/Anta-Regular.ttf", 20)
        portal_coords_font = font.Font("fonts/Anta-Regular.ttf", 20)

        def draw_world(world, dx=0, dy=0):
            screen.fill((0, 0, 0))
            if zoom == 1:
                for chunk_row in world.chunks_array:
                    for chunk in chunk_row:
                        cx, cy = chunk
                        world.draw_chunk(screen, cx, cy)
                draw_grid(screen)
            else:
                ch_x, ch_y = zoom_chunk
                start_x = max(0, ch_x - CHUNK_SIZE + dx)
                end_x = min(world.width, ch_x + CHUNK_SIZE + dx)
                start_y = max(0, ch_y - CHUNK_SIZE + dy)
                end_y = min(world.height, ch_y + CHUNK_SIZE + dy)

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
                screen.blit(player.image, player.rect)

        def calibration_of_coordinates(obj):
            x = obj.rect.x + offset[0]
            y = obj.rect.y + offset[1]
            while x < -480:
                obj.rect.x += 10
                x = obj.rect.x + offset[0]
            while x > 21480:
                obj.rect.x -= 10
                x = obj.rect.x + offset[0]
            while y < -275:
                obj.rect.x += 10
                y = obj.rect.y + offset[1]
            while y > 12870:
                obj.rect.y -= 10
                y = obj.rect.y + offset[1]
            return x - 300, y - 300

        running = True
        boss.rect.x, boss.rect.y = calibration_of_coordinates(boss)
        # portal.rect.x, portal.rect.y = calibration_of_coordinates(portal)
        # for i in cows.mobs:
        #     i.rect.x, i.rect.y = calibration_of_coordinates(i)
        # for j in pigs.mobs:
        #     j.rect.x, j.rect.y = calibration_of_coordinates(j)

        draw_world(current_world)
        while running:
            if player.hp < 0:
                death_window.show()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    # elif event.type == pygame.KEYDOWN:
                    #     if event.key == pygame.K_m:
                    #         player.dx = 0
                    #         player.dy = 0
                    #         zoom = 1
                    #         zoom_chunk = None
                    #         offset = (0, 0)
                    #         prev_chunk = None
                    #         draw_world(current_world)
                    #         portal.rect.x = portal.start_x_coord - player.map_offset[2]
                    #         portal.rect.y = portal.start_y_coord - player.map_offset[3]
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if zoom == 1:
                                mouse_pos = pygame.mouse.get_pos()
                                chunk_x = (mouse_pos[0] // (CHUNK_SIZE * TILE_SIZE)) * CHUNK_SIZE
                                chunk_y = (mouse_pos[1] // (CHUNK_SIZE * TILE_SIZE)) * CHUNK_SIZE
                                zoom_chunk = (chunk_x, chunk_y)
                                zoom = HEIGHT // (CHUNK_SIZE * TILE_SIZE) + 10

                                # Center the selected chunk
                                center_x = chunk_x * TILE_SIZE + (CHUNK_SIZE * TILE_SIZE) // 2
                                center_y = chunk_y * TILE_SIZE + (CHUNK_SIZE * TILE_SIZE) // 2
                                offset = (
                                    center_x * zoom - WIDTH // 2,
                                    center_y * zoom - HEIGHT // 2,
                                )
                                prev_chunk = None
                                draw_world(current_world)
                    elif event.type == pygame.KEYUP:
                        player.is_move = False
                        player.keyboard_up = True
                        player.moving_frame = 2
                player.check_keyboard()
                if zoom > 1:
                    if portal.change_coords:
                        portal.change_coords = False
                        x, y = calibration_of_coordinates(portal)
                        portal.coords = [x, y]

                    player_dx, player_dy = player.map_offset[0], player.map_offset[1]
                    map_dx, map_dy = player.map_offset[2], player.map_offset[3]
                    if -480 < offset[0] + player_dx < 21480 and -275 < offset[1] + player_dy < 12870:
                        offset = (offset[0] + player_dx, offset[1] + player_dy)
                        player.stop_map = False
                    else:
                        player.stop_map = True
                    draw_world(current_world, dx=map_dx, dy=map_dy)

                if zoom == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    chunk_x = (mouse_pos[0] // (CHUNK_SIZE * TILE_SIZE)) * CHUNK_SIZE
                    chunk_y = (mouse_pos[1] // (CHUNK_SIZE * TILE_SIZE)) * CHUNK_SIZE
                    current_chunk = (chunk_x, chunk_y)
                    if current_chunk != prev_chunk:
                        if prev_chunk:
                            current_world.draw_chunk(screen, prev_chunk[0], prev_chunk[1])
                        current_world.draw_chunk(screen, chunk_x, chunk_y, highlight=True)
                        draw_grid(screen)
                        prev_chunk = current_chunk
                else:
                    portal.animation(screen)
                    targets.draw(screen)
                    if current_world == boss_world:
                        cows.make_showing_false()
                        pigs.make_showing_false()
                        boss.is_showing = True
                        boss.movement()
                        # boss.breath_sound.play()
                        boss.draw(screen)
                        if boss.spawn_mushrooms:
                            mushrooms.spawn(randint(1, 15), [boss.rect.x, boss.rect.y], player,
                                            current_world, mushrooms_group)
                            boss.hp -= 1
                            boss.spawn_mushrooms = False
                        mushrooms.move(screen, mushrooms_group)
                    else:
                        cows.make_showing_true()
                        pigs.make_showing_true()
                        boss.is_showing = False
                        cows.move(screen)
                        pigs.move(screen)
                    lightning_sprite.draw(screen)
                    current_world = portal.worlds[portal.current_world]
                    player.bars.draw(screen, player.hp, player.food, player.energy, player.protection)
                    fps_text = fps_font.render(f"FPS: {round(clock.get_fps(), 1)} / 60", True, (152, 26, 26))
                    screen.blit(fps_text, (840, 7))
                    coords_text = coords_font.render(f"Coords: {offset[0] + player.map_offset[0]}; "
                                                     f"{offset[1] + player.map_offset[1]}",
                                                     True, (152, 26, 26))
                    screen.blit(coords_text, (790, 28))

                    portal_coords_text = portal_coords_font.render(f"Portal Coords: {portal.coords[0]}; "
                                                                   f"{portal.coords[1]}", True, (152, 26, 26))
                    screen.blit(portal_coords_text, (730, 50))
            if not death_window.running:
                running = False
            if death_window.reborn:
                player.hp = 5
                death_window.reborn = False
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
    except:
        pass


if __name__ == "__main__":
    main()
# class Game:
#     def __init__(self):
#         pygame.display.set_caption("Rise of Empire")
#         pygame.mixer.music.stop()
#         self.screen = pygame.display.set_mode(SIZE)
#
#         self.main_world = World(WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE, MAIN_SEED, MAIN_COLORS)
#         self.boss_world = World(WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE, BOSS_SEED, BOSS_COLORS)
#         self.current_world = self.main_world
#
#         self.player = Main_hero(500, 300, WIDTH, HEIGHT)
#
#         self.portal = Portal(500, 500, self.player, all_sprites, self.main_world, self.boss_world)
#
#         self.zoom = 1
#         self.zoom_chunk = None
#         self.offset = (0, 0)
#         self.prev_chunk = None
#     def draw_grid(self, screen, zoom=1, offset=(0, 0)):
#         grid_size = CHUNK_SIZE * TILE_SIZE * zoom
#         start_x = -offset[0] % grid_size
#         start_y = -offset[1] % grid_size
#         for x in range(start_x, WIDTH, grid_size):
#             pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
#         for y in range(start_y, HEIGHT, grid_size):
#             pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))
#
#     def draw_world(self, world, dx=0, dy=0):
#         self.screen.fill((0, 0, 0))
#         if self.zoom == 1:
#             for chunk_row in world.chunks_array:
#                 for chunk in chunk_row:
#                     cx, cy = chunk
#                     world.draw_chunk(self.screen, cx, cy)
#             self.draw_grid(self.screen)
#         else:
#             chunk_x, chunk_y = self.zoom_chunk
#             start_x = max(0, chunk_x - CHUNK_SIZE + dx)
#             end_x = min(world.width, chunk_x + CHUNK_SIZE + dx)
#             start_y = max(0, chunk_y - CHUNK_SIZE + dy)
#             end_y = min(world.height, chunk_y + CHUNK_SIZE + dy)
#
#             for x in range(start_x, end_x):
#                 for y in range(start_y, end_y):
#                     if 0 <= x < world.width and 0 <= y < world.height:
#                         height_value = world.world_map[y, x]
#                         color = world.get_terrain_color(height_value)
#                         screen_x = (x * TILE_SIZE * self.zoom - self.offset[0])
#                         screen_y = (y * TILE_SIZE * self.zoom - self.offset[1])
#                         pygame.draw.rect(
#                             self.screen,
#                             color,
#                             (
#                                 screen_x,
#                                 screen_y,
#                                 TILE_SIZE * self.zoom,
#                                 TILE_SIZE * self.zoom,
#                             ),
#                         )
#             self.screen.blit(self.player.image, self.player.rect)
#
#     def main(self):
#         self.draw_world(self.current_world)
#         for event in pygame.event.get():
#
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_m:
#                     self.player.dx = 0
#                     self.player.dy = 0
#                     self.zoom = 1
#                     self.zoom_chunk = None
#                     self.offset = (0, 0)
#                     self.prev_chunk = None
#                     self.draw_world(self.current_world)
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:
#                     if self.zoom == 1:
#                         mouse_pos = pygame.mouse.get_pos()
#                         chunk_x = (mouse_pos[0] // (CHUNK_SIZE * TILE_SIZE)) * CHUNK_SIZE
#                         chunk_y = (mouse_pos[1] // (CHUNK_SIZE * TILE_SIZE)) * CHUNK_SIZE
#                         self.zoom_chunk = (chunk_x, chunk_y)
#                         self.zoom = HEIGHT // (CHUNK_SIZE * TILE_SIZE) + 10
#
#                         # Center the selected chunk
#                         center_x = chunk_x * TILE_SIZE + (CHUNK_SIZE * TILE_SIZE) // 2
#                         center_y = chunk_y * TILE_SIZE + (CHUNK_SIZE * TILE_SIZE) // 2
#                         self.offset = (
#                             center_x * self.zoom - WIDTH // 2,
#                             center_y * self.zoom - HEIGHT // 2,
#                         )
#
#                         self.prev_chunk = None
#                         self.draw_world(self.current_world)
#             elif event.type == pygame.KEYUP:
#                 self.player.is_move = False
#                 self.player.keyboard_up = True
#                 self.player.moving_frame = 2
#         self.player.check_keyboard()
#         if self.zoom > 1:
#             player_dx, player_dy = self.player.map_offset[0], self.player.map_offset[1]
#             map_dx, map_dy = self.player.map_offset[2], self.player.map_offset[3]
#             if -480 < self.offset[0] + player_dx < 21480 and -275 < self.offset[1] + player_dy < 12870:
#                 self.offset = (self.offset[0] + player_dx, self.offset[1] + player_dy)
#             self.draw_world(self.current_world, dx=map_dx, dy=map_dy)
#
#         elif self.zoom == 1:
#             mouse_pos = pygame.mouse.get_pos()
#             chunk_x = (mouse_pos[0] // (CHUNK_SIZE * TILE_SIZE)) * CHUNK_SIZE
#             chunk_y = (mouse_pos[1] // (CHUNK_SIZE * TILE_SIZE)) * CHUNK_SIZE
#             current_chunk = (chunk_x, chunk_y)
#             if current_chunk != self.prev_chunk:
#                 if self.prev_chunk:
#                     self.current_world.draw_chunk(self.screen, self.prev_chunk[0], self.prev_chunk[1])
#                 self.current_world.draw_chunk(self.screen, chunk_x, chunk_y, highlight=True)
#                 self.draw_grid(self.screen)
#                 self.prev_chunk = current_chunk
#         else:
#             self.portal.animation()
#             all_sprites.draw(screen)
#             self.current_world = self.portal.worlds[self.portal.current_world]
#             self.player.bars.draw(self.screen, self.player.hp, self.player.food, self.player.energy,
#             self.player.protection)
#         pygame.display.flip()
