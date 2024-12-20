import pygame
class Main_hero(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(file).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.make_variables()

    def make_variables(self):
        self.pos_x = 0
        self.pos_y = 0
        # Для прыжков
        # self.jump = 0
        # self.is_on_ground = False

        self.is_move = False

        self.moving_frame = 0
        self.stop_frame = 0

        self.blink = 0

        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False

        self.fast_moving = False

        self.right_moving_pictures = ['img/Main_hero_sprites/sprite_4.png', 'img/Main_hero_sprites/sprite_8.png',
                                      'img/Main_hero_sprites/sprite_10.png']
        self.left_moving_pictures = ['img/Main_hero_sprites/sprite_2.png', 'img/Main_hero_sprites/sprite_7.png',
                                     'img/Main_hero_sprites/sprite_9.png']
        self.up_moving_pictures = ['img/Main_hero_sprites/sprite_3.png', 'img/Main_hero_sprites/sprite_11.png',
                                   'img/Main_hero_sprites/sprite_12.png']
        self.down_moving_pictures = ['img/Main_hero_sprites/main_sprite.png', 'img/Main_hero_sprites/sprite_6.png',
                                     'img/Main_hero_sprites/sprite_5.png']
        self.down_stop_pictures = ['img/Main_hero_sprites/main_sprite.png', 'img/Main_hero_sprites/sprite_13.png',
                                   'img/Main_hero_sprites/sprite_14.png', 'img/Main_hero_sprites/sprite_13.png',
                                   'img/Main_hero_sprites/main_sprite.png']
        self.left_stop_pictures = ['img/Main_hero_sprites/sprite_2.png', 'img/Main_hero_sprites/sprite_15.png',
                                   'img/Main_hero_sprites/sprite_16.png', 'img/Main_hero_sprites/sprite_15.png',
                                   'img/Main_hero_sprites/sprite_2.png']
        self.right_stop_pictures = ['img/Main_hero_sprites/sprite_4.png', 'img/Main_hero_sprites/sprite_17.png',
                                    'img/Main_hero_sprites/sprite_18.png', 'img/Main_hero_sprites/sprite_17.png',
                                    'img/Main_hero_sprites/sprite_4.png']


    def movement(self, *args):
        if self.fast_moving and self.is_move:
            if self.move_right or self.move_left:
                self.pos_x = self.pos_x * 1.5
            elif self.move_up or self.move_down:
                self.pos_y = self.pos_y * 1.5
        self.rect.x += self.pos_x
        self.rect.y += self.pos_y

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

        self.put_sprites()

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
            if self.move_right:
                self.image = pygame.image.load(self.right_moving_pictures[int(self.moving_frame)]).convert_alpha()
            elif self.move_left:
                self.image = pygame.image.load(self.left_moving_pictures[int(self.moving_frame)]).convert_alpha()
            elif self.move_up:
                self.image = pygame.image.load(self.up_moving_pictures[int(self.moving_frame)]).convert_alpha()
            elif self.move_down:
                self.image = pygame.image.load(self.down_moving_pictures[int(self.moving_frame)]).convert_alpha()
        else:
            self.blink += 0.1
            self.stop_frame += low_coefficient
            if self.stop_frame > 5:
                self.stop_frame = 0
            if self.blink > 5 and self.blink < 7 or self.blink == 0.1:
                if self.move_right:
                    self.image = pygame.image.load(self.right_stop_pictures[int(self.stop_frame)]).convert_alpha()
                elif self.move_left:
                    self.image = pygame.image.load(self.left_stop_pictures[int(self.stop_frame)]).convert_alpha()
                elif self.move_up:
                    self.image = pygame.image.load(self.up_moving_pictures[0]).convert_alpha()
                elif self.move_down:
                    self.image = pygame.image.load(self.down_stop_pictures[int(self.stop_frame)]).convert_alpha()
            elif self.blink > 7:
                self.stop_frame = 0
                self.blink = 0
            self.moving_frame = 2

    def make_right_true(self):
        self.pos_x = 5
        self.is_move = True

        self.move_right = True
        self.move_left = False
        self.move_up = False
        self.move_down = False

    def make_left_true(self):
        self.pos_x = -5
        self.is_move = True

        self.move_right = False
        self.move_left = True
        self.move_up = False
        self.move_down = False

    def make_up_true(self):
        self.pos_y = -5
        self.is_move = True

        self.move_right = False
        self.move_left = False
        self.move_up = True
        self.move_down = False

    def make_down_true(self):
        self.pos_y = 5
        self.is_move = True

        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = True

    def make_fast_moving(self):
        self.fast_moving = True

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
        # Для прыжков
        # if key[pygame.K_SPACE]:
        #     if player.is_on_ground:
        #         player.jump = -20
        #
        #         player.is_on_ground = False
        # player.movement(height - player.rect.height)
        self.movement()

if __name__ == '__main__':
    pygame.init()
    size = width, height = (1000, 500)
    screen = pygame.display.set_mode(size)
    running = True
    clock = pygame.time.Clock()
    player = Main_hero('img/Main_hero_sprites/main_sprite.png', 100, 400)
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                player.is_move = False
                player.frame = 2
        player.check_keyboard()
        screen.blit(player.image, player.rect)
        pygame.display.flip()
        clock.tick(30)