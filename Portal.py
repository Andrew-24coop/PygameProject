import pygame


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, player, main_world, other_world):
        super().__init__()
        self.image = pygame.image.load("img/Portal/portal_0.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.start_x_coord = x
        self.start_y_coord = y
        self.mask = pygame.mask.from_surface(self.image)

        self.worlds = [main_world, other_world]
        self.current_world = 0

        self.sprites = [pygame.image.load(f"img/Portal/portal_{i}.png").convert_alpha() for i in range(9)]
        self.sprites_frame = 0
        self.delay = 0

        self.player = player

        self.coords = []
        self.change_coords = True

        self.teleportation_sound = pygame.mixer.Sound("sounds/enderman_teleport.mp3")

    def animation(self, screen):
        if not self.player.stop_map:
            self.rect.x -= self.player.map_offset[0]
            self.rect.y -= self.player.map_offset[1]
        self.check_collision()
        self.sprites_frame += 0.2
        if self.sprites_frame >= 9:
            self.sprites_frame = 0
        self.image = self.sprites[int(self.sprites_frame)]
        screen.blit(self.image, self.rect)

    def check_collision(self):
        if self.delay == 0:
            if pygame.sprite.collide_mask(self, self.player):
                self.teleportation_sound.play()
                self.current_world = 1 - self.current_world
                self.delay += 0.1
        else:
            self.delay += 0.1
        if self.delay > 20:
            self.delay = 0
