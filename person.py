import numpy as np
from player_status import *

targets = pygame.sprite.Group()
dragon = pygame.sprite.Group()
lightning_sprite = pygame.sprite.Group()
mushrooms_group = pygame.sprite.Group()
mobs = pygame.sprite.Group()
portal_sprite = pygame.sprite.Group()


class MainHero(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("img/Main_hero_sprites/main_sprite.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.width = width
        self.height = height

        self.lightning = Lightning(self, x, y, width, height)
        self.bars = Bars(30, 10)

        self.hp = 5
        self.damage = 1
        self.protection = 0
        self.food = 5
        self.energy = 0

        self.pos_x = 0
        self.pos_y = 0
        self.dx = 0
        self.dy = 0
        # Для прыжков
        # self.jump = 0
        # self.is_on_ground = False

        self.is_move = False

        self.moving_frame = 0
        self.stop_frame = 0

        self.blink = 0

        self.direction = "DOWN"

        self.fast_moving = False

        self.lightning_attack = False

        self.sword_attack = False
        self.sword_frame = 0
        self.sword_rotation = {"RIGHT": pygame.image.load("img/Attack/right_sword_attack.png").convert_alpha(),
                               "LEFT": pygame.transform.flip(
                                   pygame.image.load("img/Attack/right_sword_attack.png").convert_alpha(), True, False),
                               "UP": pygame.image.load("img/Attack/back_sword_attack.png").convert_alpha(),
                               "DOWN": pygame.image.load("img/Attack/front_sword_attack.png").convert_alpha()}
        self.keyboard_up = True

        self.map_offset = []
        self.stop_map = False

        self.sword_miss_sound = pygame.mixer.Sound("sounds/promah-pri-boe-na-mechah.mp3")
        self.sword_hit_sound = pygame.mixer.Sound("sounds/nasajivayuschiy-pronikayuschiy-udar.mp3")
        self.sounds_of_walking = [pygame.mixer.Sound("sounds/byistraya-hodba-po-graviyu-26129 (mp3cut.net).mp3"),
                                  pygame.mixer.Sound("sounds/byistraya-hodba-po-graviyu-26129 (mp3cut.net) (1).mp3"),
                                  pygame.mixer.Sound("sounds/byistraya-hodba-po-graviyu-26129 (mp3cut.net) (2).mp3"),
                                  pygame.mixer.Sound("sounds/byistraya-hodba-po-graviyu-26129 (mp3cut.net) (3).mp3"),
                                  pygame.mixer.Sound("sounds/byistraya-hodba-po-graviyu-26129 (mp3cut.net) (4).mp3")]
        self.sound_frame = 0
        self.sound_delay = 0

        self.time = 0
        self.change_food = True

        self.total_offset = None

        self.right_moving_pictures = [pygame.image.load('img/Main_hero_sprites/sprite_4.png').convert_alpha(),
                                      pygame.image.load('img/Main_hero_sprites/sprite_8.png').convert_alpha(),
                                      pygame.image.load('img/Main_hero_sprites/sprite_10.png').convert_alpha()]
        self.left_moving_pictures = [pygame.image.load('img/Main_hero_sprites/sprite_2.png').convert_alpha(),
                                     pygame.image.load('img/Main_hero_sprites/sprite_7.png').convert_alpha(),
                                     pygame.image.load('img/Main_hero_sprites/sprite_9.png').convert_alpha()]
        self.up_moving_pictures = [pygame.image.load('img/Main_hero_sprites/sprite_3.png').convert_alpha(),
                                   pygame.image.load('img/Main_hero_sprites/sprite_11.png').convert_alpha(),
                                   pygame.image.load('img/Main_hero_sprites/sprite_12.png').convert_alpha()]
        self.down_moving_pictures = [pygame.image.load('img/Main_hero_sprites/main_sprite.png').convert_alpha(),
                                     pygame.image.load('img/Main_hero_sprites/sprite_6.png').convert_alpha(),
                                     pygame.image.load('img/Main_hero_sprites/sprite_5.png').convert_alpha()]
        self.down_stop_pictures = [pygame.image.load('img/Main_hero_sprites/main_sprite.png').convert_alpha(),
                                   pygame.image.load('img/Main_hero_sprites/sprite_13.png').convert_alpha(),
                                   pygame.image.load('img/Main_hero_sprites/sprite_14.png').convert_alpha(),
                                   pygame.image.load('img/Main_hero_sprites/sprite_13.png').convert_alpha(),
                                   pygame.image.load('img/Main_hero_sprites/main_sprite.png').convert_alpha()]
        self.left_stop_pictures = [pygame.image.load('img/Main_hero_sprites/sprite_2.png').convert_alpha(),
                                   pygame.image.load('img/Main_hero_sprites/sprite_15.png').convert_alpha(),
                                   pygame.image.load('img/Main_hero_sprites/sprite_16.png').convert_alpha(),
                                   pygame.image.load('img/Main_hero_sprites/sprite_15.png').convert_alpha(),
                                   pygame.image.load('img/Main_hero_sprites/sprite_2.png').convert_alpha()]
        self.right_stop_pictures = [pygame.image.load('img/Main_hero_sprites/sprite_4.png').convert_alpha(),
                                    pygame.image.load('img/Main_hero_sprites/sprite_17.png').convert_alpha(),
                                    pygame.image.load('img/Main_hero_sprites/sprite_18.png').convert_alpha(),
                                    pygame.image.load('img/Main_hero_sprites/sprite_17.png').convert_alpha(),
                                    pygame.image.load('img/Main_hero_sprites/sprite_4.png').convert_alpha()]

    def movement(self):
        if self.fast_moving:
            if self.direction == "RIGHT" or self.direction == "LEFT":
                self.pos_x = self.pos_x * 2
            elif self.direction == "UP" or self.direction == "DOWN":
                self.pos_y = self.pos_y * 2

        # self.rect.x += self.pos_x
        # self.rect.y += self.pos_y

        if not self.stop_map:
            self.dx += self.pos_x / 22
            self.dy += self.pos_y / 22

        self.map_offset = [self.pos_x, self.pos_y, int(self.dx), int(self.dy)]

        if self.lightning_attack:
            if self.lightning.explosion:
                end = self.lightning.animate_explosion()
                if end:
                    self.lightning_attack = False
            else:
                self.lightning.update()

        # Для прыжков
        # if not self.is_on_ground:
        #     self.jump += 1
        # self.rect.y += self.jump
        #
        # self.is_on_ground = False
        #
        # if self.rect.y > args[0]:
        #     self.rect.y = args[0]
        #     self.jump = 0
        #     self.is_on_ground = True

        self.pos_x = 0
        self.pos_y = 0
        self.fast_moving = False

        if self.sword_attack:
            self.sword_animation(self.direction)
        else:
            self.put_sprites()

        self.time = int(pygame.time.get_ticks() / 1000)
        if self.time % 60 == 0:
            if self.change_food:
                self.food -= 1
                if self.food < 0:
                    self.food = 0
                    self.hp -= 1
                self.change_food = False
        else:
            self.change_food = True

        # if self.hp <= 0:
        #     main_hero_sprite.remove(self)

    def put_sprites(self):
        coefficient = 0.2
        low_coefficient = 0.3
        if self.fast_moving:
            coefficient = 0.3
        if self.is_move:
            self.blink = 0
            self.stop_frame = 0
            self.moving_frame += coefficient
            if self.moving_frame > 3:
                self.moving_frame = 0
            self.play_walking_sound()
            if self.direction == "RIGHT":
                self.image = self.right_moving_pictures[int(self.moving_frame)]
            elif self.direction == "LEFT":
                self.image = self.left_moving_pictures[int(self.moving_frame)]
            elif self.direction == "UP":
                self.image = self.up_moving_pictures[int(self.moving_frame)]
            elif self.direction == "DOWN":
                self.image = self.down_moving_pictures[int(self.moving_frame)]
        else:
            self.blink += 0.1
            self.stop_frame += low_coefficient
            if self.stop_frame > 5:
                self.stop_frame = 0
            if 5 < self.blink < 7 or self.blink == 0.1:
                if self.direction == "RIGHT":
                    self.image = self.right_stop_pictures[int(self.stop_frame)]
                elif self.direction == "LEFT":
                    self.image = self.left_stop_pictures[int(self.stop_frame)]
                elif self.direction == "UP":
                    self.image = self.up_moving_pictures[0]
                elif self.direction == "DOWN":
                    self.image = self.down_stop_pictures[int(self.stop_frame)]
            elif self.blink > 7:
                self.stop_frame = 0
                self.blink = 0
            self.moving_frame = 2
        # if mushroom.attack:
        #     self.image = self.apply_red_filter(self.image)

    def play_walking_sound(self):
        if self.sound_delay == 0:
            self.sounds_of_walking[self.sound_frame].play()
            self.sound_frame += 1
            if self.sound_frame > 4:
                self.sound_frame = 0
            self.sound_delay += 0.2
        else:
            self.sound_delay += 0.1
            if self.sound_delay > 0.5:
                self.sound_delay = 0

    def make_right_true(self):
        self.pos_x = 5
        self.is_move = True

        self.direction = "RIGHT"

    def make_left_true(self):
        self.pos_x = -5
        self.is_move = True

        self.direction = "LEFT"

    def make_up_true(self):
        self.pos_y = -5
        self.is_move = True

        self.direction = "UP"

    def make_down_true(self):
        self.pos_y = 5
        self.is_move = True

        self.direction = "DOWN"

    def make_fast_moving(self):
        self.fast_moving = True

    def sword_animation(self, direction):
        self.image = self.sword_rotation[direction]
        self.sword_frame += 0.2
        if self.sword_frame > 1:
            self.sword_frame = 0
            self.sword_attack = False
            self.blink = 5
            self.sword_miss_sound.play()
            # if self.direction == "LEFT":
            #     self.rect.x += 35

    def check_keyboard(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_d]:
            self.make_right_true()

        if key[pygame.K_a]:
            self.make_left_true()

        if key[pygame.K_w]:
            self.make_up_true()

        if key[pygame.K_s]:
            self.make_down_true()

        if key[pygame.K_LCTRL]:
            self.make_fast_moving()

        if key[pygame.K_SPACE] and self.keyboard_up:
            self.keyboard_up = False
            self.sword_attack = True
            # if self.direction == "LEFT":
            #     self.rect.x -= 35

        if key[pygame.K_f]:
            if self.energy >= 5:
                self.lightning_attack = True
                lightning_sprite.add(self.lightning)
                self.lightning.sound_of_shot.play()
                if not self.lightning.attack_animation:
                    self.lightning.rect.x = self.rect.x
                    self.lightning.rect.y = self.rect.y + 20
                    self.lightning.rotate_lightning(self.direction)

        # Для прыжков
        # if key[pygame.K_SPACE]:
        #     if player.is_on_ground:
        #         player.jump = -20
        #
        #         player.is_on_ground = False
        # player.movement(height - player.rect.height)
        self.movement()


class Lightning(pygame.sprite.Sprite):
    def __init__(self, parent, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.par = parent
        self.image = pygame.image.load("img/Attack/lightning.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.damage = 10

        self.rotation = {"RIGHT": [0, 35, 0], "LEFT": [180, -35, 0],
                         "UP": [90, 0, -35], "DOWN": [270, 0, 35]}

        self.width = width
        self.height = height

        self.explosion = False
        self.attack_animation = False

        explosion_image_1 = pygame.image.load("img/Attack/lightning_exploding1.png").convert_alpha()
        explosion_image_2 = pygame.image.load("img/Attack/lightning_exploding2.png").convert_alpha()
        explosion_image_3 = pygame.image.load("img/Attack/lightning_exploding3.png").convert_alpha()
        self.explosion_sprites = [explosion_image_1, explosion_image_2, explosion_image_3]

        self.explosion_frame = 0

        self.speed_x = 0
        self.speed_y = 0

        self.distance = 0

        self.sound_of_shot = pygame.mixer.Sound("sounds/energiya-magii-strelyaet-spetseffektami-43239 (mp3cut.net).mp3")
        self.sound_of_explosion = pygame.mixer.Sound("sounds/energeticheskiy-vzryiv-38115 (mp3cut.net) (1).mp3")

    def update(self):
        self.attack_animation = True
        if self.distance > 1000:
            self.distance = 0
            self.speed_x = 0
            self.speed_y = 0
            self.explosion = True
        for i in mobs:
            if pygame.sprite.collide_mask(self, i) and not i.die and i.is_showing:
                i.hp -= self.damage
                self.speed_x = 0
                self.speed_y = 0
                self.sound_of_explosion.play()
                self.explosion = True
        for j in dragon:
            if pygame.sprite.collide_mask(self, j) and j.is_showing and not j.die:
                j.hp -= self.damage
                self.speed_x = 0
                self.speed_y = 0
                self.sound_of_explosion.play()
                self.explosion = True
        for a in mushrooms_group:
            if pygame.sprite.collide_mask(self, a):
                a.hp -= self.damage
                self.speed_x = 0
                self.speed_y = 0
                self.sound_of_explosion.play()
                self.explosion = True
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.distance += max(abs(self.speed_x), abs(self.speed_y))

    def animate_explosion(self):
        self.explosion_frame += 0.4
        if self.explosion_frame > 3:
            self.explosion_frame = 0
            self.explosion = False
            self.attack_animation = False
            lightning_sprite.remove(self)
            self.par.lightning_attack = False
            self.speed_x = 0
            self.speed_y = 0
            self.par.energy = 0
            return True
        else:
            self.image = self.explosion_sprites[int(self.explosion_frame)]
            return False

    def rotate_lightning(self, direction):
        self.image = pygame.image.load("img/Attack/lightning.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image,
                                             self.rotation[direction][0])
        # for i in range(3):
        #    self.explosion_sprites[i] = pygame.transform.rotate(self.explosion_sprites[i], self.rotation[direction][0])
        self.speed_x = self.rotation[direction][1]
        self.speed_y = self.rotation[direction][2]


# if __name__ == '__main__':
#     pygame.init()
#     screen = pygame.display.set_mode(SIZE)
#     running = True
#     clock = pygame.time.Clock()
#     player = Main_hero(400, 400, WIDTH, HEIGHT)
#     mushroom = Mushroom(player, 800, 400, 1000, 1000)
#     heart = Hearts(400, 100, player, all_sprites)
#     player.lightning.target = mushroom
#     main_hero_sprite.add(player)
#     all_sprites.add(mushroom)
#     while running:
#         screen.fill((0, 0, 0))
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.KEYUP:
#                 player.is_move = False
#                 player.moving_frame = 2
#                 player.keyboard_up = True
#         player.check_keyboard()
#         player.bars.draw(screen, player.hp, player.food, player.energy, player.protection)
#         heart.animation()
#         if not mushroom.end:
#             mushroom.movement()
#         if mushroom.end:
#             all_sprites.remove(mushroom)
#         main_hero_sprite.draw(screen)
#         all_sprites.draw(screen)
#         pygame.display.flip()
#         clock.tick(FPS)

def apply_red_filter(surface):
    arr = pygame.surfarray.array3d(surface)  # Получаем цветовую составляющую

    # Убираем зеленую и синюю составляющие, оставляя красную
    red_filtered = np.copy(arr)
    red_filtered[:, :, 1] = 0  # Убираем зеленый канал
    red_filtered[:, :, 2] = 0  # Убираем синий канал

    return pygame.surfarray.make_surface(red_filtered)
