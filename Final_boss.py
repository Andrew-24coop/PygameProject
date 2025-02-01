import pygame
from pygame import font
import numpy as np


class Dragon(pygame.sprite.Sprite):
    def __init__(self, target, x, y, width, height):
        super().__init__()
        font.init()
        self.image = pygame.image.load("img/Dragon_sprites/Walk1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.target = target

        self.width = width
        self.heigjt = height

        self.directions = ["RIGHT", "LEFT"]
        self.direction_index = 0
        self.walking_frame = 0
        self.speed = 2
        self.dx = 0

        self.hp = 20

        self.delay = 0

        self.spawn_mushrooms = False

        self.angry = False
        self.anger_frame = 0.2
        self.anger_coefficient = 0.1

        self.is_showing = False
        self.die = False

        self.hp_text = font.Font("fonts/PixelifySans-SemiBold.ttf", 40)
        self.hp_text = self.hp_text.render("Dragon", True, (152, 26, 26))

        self.hurt_sound = pygame.mixer.Sound("sounds/padenie-drakona-v-kompyuternoy-igre.mp3")
        self.angry_shout_sound = pygame.mixer.Sound("sounds/zlobnyiy-krik-dinozavra (mp3cut.net).mp3")
        self.breath_sound = pygame.mixer.Sound("sounds/dragon breath (mp3cut.net).mp3")

        self.right_walk_sprites = [pygame.image.load(f"img/Dragon_sprites/Walk{i}.png").convert_alpha()
                                   for i in range(1, 6)]
        self.left_walk_sprites = [pygame.transform.flip(self.right_walk_sprites[i], True, False)
                                  for i in range(len(self.right_walk_sprites))]
        self.right_attack_sprites = [pygame.image.load(f"img/Dragon_sprites/Attack{i}.png").convert_alpha()
                                     for i in range(1, 5)]
        self.left_attack_sprites = [pygame.transform.flip(self.right_attack_sprites[i], True, False)
                                    for i in range(len(self.right_attack_sprites))]
        # self.right_death_sprites = [pygame.image.load(f"img/Dragon_sprites/Death{i}.png").convert_alpha() for i in
        #                              range(1, 6)]
        # self.left_attack_sprites = [pygame.transform.flip(self.right_death_sprites[i], True, False) for i in
        #                             range(len(self.right_death_sprites))]

    def movement(self):
        self.check_collision()
        if self.angry:
            self.animate_anger()
        else:
            self.rect.x += self.speed
            self.walking_frame += 0.2
            if self.walking_frame > 4:
                self.walking_frame = 0
            if self.directions[self.direction_index] == "RIGHT":
                self.image = self.right_walk_sprites[int(self.walking_frame)]
            else:
                self.image = self.left_walk_sprites[int(self.walking_frame)]
            self.dx += self.speed
            if self.dx == 200 or self.dx == -200:
                self.speed = -self.speed
                self.direction_index = 1 - self.direction_index
        if not self.target.stop_map:
            self.rect.x -= self.target.map_offset[0]
            self.rect.y -= self.target.map_offset[1]

    def check_collision(self):
        if self.delay == 0:
            if pygame.sprite.collide_mask(self, self.target):
                if self.target.sword_attack:
                    self.hp = self.hp - 1
                    if self.hp < 0:
                        self.die = True
                    else:
                        self.hurt_sound.play()
                        if self.hp % 20 <= 3:
                            self.angry = True
                        self.target.energy += 1
                        if self.target.energy > 5:
                            self.target.energy = 5
                        self.target.sword_hit_sound.play()
                        self.delay += 0.1
                        self.target.hp -= 0.01
        else:
            self.delay += 0.2
            if self.delay > 1:
                self.delay = 0
            self.image = apply_red_filter(self.image)

    def draw(self, screen):
        if not self.die:
            screen.blit(self.image, self.rect)
            screen.blit(self.hp_text, (425, 5))
            pygame.draw.rect(screen, (152, 26, 26), (250, 55, int(self.hp * 500 / 200), 7))
            pygame.draw.rect(screen, (0, 0, 0), (248, 53, 502, 9), 2)

    def animate_anger(self):
        self.angry_shout_sound.play()
        if self.anger_frame >= 2:
            self.anger_coefficient = -0.1
        if self.anger_frame < 0:
            self.anger_frame = 0.2
            self.anger_coefficient = 0.1
            self.angry = False
            self.spawn_mushrooms = True
        else:
            if self.directions[self.direction_index] == "RIGHT":
                self.image = self.right_attack_sprites[int(self.anger_frame)]
            else:
                self.image = self.left_attack_sprites[int(self.anger_frame)]
            self.anger_frame += self.anger_coefficient


class Fire(pygame.sprite.Sprite):
    def __init__(self, parent, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.par = parent
        self.image = pygame.image.load("img/Dragon_sprites/Fire_Attack1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.target = None

        # self.rotation = {"RIGHT": [0, 35, 0], "LEFT": [180, -35, 0],
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

        # self.speed_x = 0
        # self.speed_y = 0

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
    #     #    self.explosion_sprites[i] = pygame.transform.rotate(self.explosion_sprites[i],
    #     self.rotation[direction][0])
    #     self.speed_x = self.rotation[direction][1]
    #     self.speed_y = self.rotation[direction][2]


def apply_red_filter(surface):
    arr = pygame.surfarray.array3d(surface)  # Получаем цветовую составляющую

    # Убираем зеленую и синюю составляющие, оставляя красную
    red_filtered = np.copy(arr)
    red_filtered[:, :, 1] = 0  # Убираем зеленый канал
    red_filtered[:, :, 2] = 0  # Убираем синий канал

    return pygame.surfarray.make_surface(red_filtered)
