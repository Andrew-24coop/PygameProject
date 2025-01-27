import pygame

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, player, all_sprites, main_world, other_world):
        super().__init__()
        self.image = pygame.image.load("img/Portal/portal_0.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.worlds = [main_world, other_world]
        self.current_world = 0

        self.sprites = [pygame.image.load(f"img/Portal/portal_{i}.png").convert_alpha() for i in range(9)]
        self.sprites_frame = 0
        self.delay = 0

        self.player = player
        self.group = all_sprites
        self.group.add(self)
    def animation(self):
        self.rect.x -= self.player.map_offset[0]
        self.rect.y -= self.player.map_offset[1]
        self.check_collision()
        self.sprites_frame += 0.2
        if self.sprites_frame >= 9:
            self.sprites_frame = 0
        self.image = self.sprites[int(self.sprites_frame)]

    def check_collision(self):
        if self.delay == 0:
            if pygame.sprite.collide_mask(self, self.player):
                self.current_world = 1 - self.current_world
                self.delay += 0.1
        else:
            self.delay += 0.1
        if self.delay > 20:
            self.delay = 0

