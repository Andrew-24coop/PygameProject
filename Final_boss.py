import pygame
from random import choice

class Dragon(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("img/Dragon_sprites/Walk1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.width = width
        self.heigjt = height

        self.make_sprite_lists()

    def make_sprite_lists(self):
        self.right_walk_sprites = [pygame.image.load(f"img/Dragon_sprites/Walk{i}.png").convert_alpha()
                                   for i in range(1, 6)]
        self.left_walk_sprites = [pygame.transform.flip(self.right_walk_sprites[i], True, False)
                                  for i in range(len(self.right_walk_sprites))]
        self.right_attack_sprites = [pygame.image.load(f"img/Dragon_sprites/Attack{i}.png").convert_alpha()
                                     for i in range(1, 5)]
        self.left_attack_sprites = [pygame.transform.flip(self.right_attack_sprites[i], True, False)
                                    for i in range(len(self.right_walk_sprites))]
        self.right_death_sprites = [pygame.image.load(f"img/Dragon_sprites/Death{i}.png").convert_alpha() for i in
                                     range(1, 6)]
        self.left_attack_sprites = [pygame.transform.flip(self.right_death_sprites[i], True, False) for i in
                                    range(len(self.right_death_sprites))]



class Fire(pygame.sprite.Sprite):
    def __init__(self, parent, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.par = parent
        self.image = pygame.image.load("img/Dragon_sprites/Fire_Attack1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.target = None

        #self.rotation = {"RIGHT": [0, 35, 0], "LEFT": [180, -35, 0],
        #                 "UP": [90, 0, -35], "DOWN": [270, 0, 35]}

        self.width = width
        self.height = height

        self.attack = False

        self.right_fire_sprites = [pygame.image.load(f"img/Dragon_sprites/Attack{i}.png").convert_alpha()
                                   for i in range(1, 7)]
        self.left_fire_sprites = [pygame.transform.flip(self.right_fire_sprites[i], True, False)
                                  for i in range(len(self.right_fire_sprites))]

        self.attack_frame = 0
        self.attack_time = 0

        #self.speed_x = 0
        #self.speed_y = 0

    def fire_attack(self):
        self.rect.x = self.par.rect.x
        self.rect.y = self.par.rect.y
        self.attack_frame += 0.2
        if self.attack_frame > 5.8:
            self.attack = False
        else:
            if self.par.direction == "LEFT":
                self.image = self.left_fire_sprites[int(self.attack_frame)]
            else:
                self.image = self.right_fire_sprites[int(self.attack_frame)]

    # def animate_explosion(self):
    #     self.explosion_frame += 0.4
    #     if self.explosion_frame > 3:
    #         self.explosion_frame = 0
    #         self.explosion = False
    #         self.attack_animation = False
    #         all_sprites.remove(self)
    #         self.par.lightning_attack = False
    #         self.speed_x = 0
    #         self.speed_y = 0
    #         return True
    #     else:
    #         self.image = self.explosion_sprites[int(self.explosion_frame)]
    #         return False
    #
    # def rotate_lightning(self, direction):
    #     self.image = pygame.image.load("img/Attack/lightning.png").convert_alpha()
    #     self.image = pygame.transform.rotate(self.image,
    #                                                    self.rotation[direction][0])
    #     #for i in range(3):
    #     #    self.explosion_sprites[i] = pygame.transform.rotate(self.explosion_sprites[i], self.rotation[direction][0])
    #     self.speed_x = self.rotation[direction][1]
    #     self.speed_y = self.rotation[direction][2]
