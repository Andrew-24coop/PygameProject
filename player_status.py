import pygame


class Bars(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.health_bar = pygame.image.load("img/Bars/Health/health_bar_1.png").convert_alpha()
        self.food_bar = pygame.image.load("img/Bars/Food/food_bar_1.png").convert_alpha()
        self.energy_bar = pygame.image.load("img/Bars/Energy/energy_bar_1.png").convert_alpha()
        self.protection_bar = pygame.image.load("img/Bars/Protection/protection_bar_1.png").convert_alpha()

        self.health_rect = self.health_bar.get_rect(center=(x, y))
        self.food_rect = self.food_bar.get_rect(center=(x, y + 15))
        self.energy_rect = self.energy_bar.get_rect(center=(x, y + 30))
        self.protection_rect = self.protection_bar.get_rect(center=(x, y + 45))

        self.health_bar_sprites = [pygame.image.load(f"img/Bars/Health/health_bar_{i}.png").convert_alpha()
                                   for i in range(6)]
        self.food_bar_sprites = [pygame.image.load(f"img/Bars/Food/food_bar_{i}.png").convert_alpha()
                                 for i in range(6)]
        self.energy_bar_sprites = [pygame.image.load(f"img/Bars/Energy/energy_bar_{i}.png").convert_alpha()
                                   for i in range(6)]
        self.protection_bar_sprites = [pygame.image.load(f"img/Bars/Protection/protection_bar_{i}.png").convert_alpha()
                                       for i in range(6)]

        self.sound_of_energy = pygame.mixer.Sound(
            "sounds/korotkie-spetseffektyi-nakopleniya-energii-40430 (mp3cut.net).mp3")
        self.sound = True

    def draw(self, screen, health, food, energy, protection):
        self.health_bar = self.health_bar_sprites[int(round(health, 0))]
        screen.blit(self.health_bar, self.health_rect)

        self.food_bar = self.food_bar_sprites[food]
        screen.blit(self.food_bar, self.food_rect)

        self.energy_bar = self.energy_bar_sprites[energy]
        screen.blit(self.energy_bar, self.energy_rect)
        if energy == 5 and self.sound:
            self.sound_of_energy.play()
            self.sound = False
        if energy < 5:
            self.sound = True

        self.protection_bar = self.protection_bar_sprites[protection]
        screen.blit(self.protection_bar, self.protection_rect)


class Hearts(pygame.sprite.Sprite):
    def __init__(self, x, y, player, all_sprites):
        super().__init__()
        self.image = pygame.image.load("img/Healing_hearts/heart_1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.heal = 1

        self.sprites = [pygame.image.load(f"img/Healing_hearts/heart_{i}.png").convert_alpha() for i in range(1, 10)]
        self.frame = 0

        self.player = player
        self.group = all_sprites
        self.group.add(self)

    def animation(self):
        self.check_collision()
        self.frame += 0.2
        if self.frame >= 9:
            self.frame = 0
        self.image = self.sprites[int(self.frame)]

    def check_collision(self):
        if self in self.group:
            if pygame.sprite.collide_mask(self, self.player):
                self.player.hp += self.heal
                if self.player.hp > 5:
                    self.player.hp = 5
                self.group.remove(self)
