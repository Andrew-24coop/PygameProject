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
        self.frame = 0

        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False

        self.fast_moving = False

        self.right_moving_pictures = ['Main_hero_sprites/sprite_4.png', 'Main_hero_sprites/sprite_8.png',
                                      'Main_hero_sprites/sprite_10.png']
        self.left_moving_pictures = ['Main_hero_sprites/sprite_2.png', 'Main_hero_sprites/sprite_7.png',
                                     'Main_hero_sprites/sprite_9.png']
        self.up_moving_pictures = ['Main_hero_sprites/sprite_3.png', 'Main_hero_sprites/sprite_11.png',
                                   'Main_hero_sprites/sprite_12.png']
        self.down_moving_pictures = ['Main_hero_sprites/main_sprite.png', 'Main_hero_sprites/sprite_6.png',
                                     'Main_hero_sprites/sprite_5.png']

    def movement(self, *args):
        if self.fast_moving:
            self.pos_x = self.pos_x * 2
            self.pos_y = self.pos_y * 2
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
        if self.fast_moving:
            coefficient = 0.3
        if self.is_move:
            self.frame += coefficient
            if self.frame > 3:
                self.frame = 0

            if self.move_right:
                self.image = pygame.image.load(self.right_moving_pictures[int(self.frame)]).convert_alpha()
            elif self.move_left:
                self.image = pygame.image.load(self.left_moving_pictures[int(self.frame)]).convert_alpha()
            elif self.move_up:
                self.image = pygame.image.load(self.up_moving_pictures[int(self.frame)]).convert_alpha()
            elif self.move_down:
                self.image = pygame.image.load(self.down_moving_pictures[int(self.frame)]).convert_alpha()
        else:
            if self.move_right:
                self.image = pygame.image.load(self.right_moving_pictures[0]).convert_alpha()
            elif self.move_left:
                self.image = pygame.image.load(self.left_moving_pictures[0]).convert_alpha()
            elif self.move_up:
                self.image = pygame.image.load(self.up_moving_pictures[0]).convert_alpha()
            elif self.move_down:
                self.image = pygame.image.load(self.down_moving_pictures[0]).convert_alpha()
            self.frame = 2


def move():
    key = pygame.key.get_pressed()

    if key[pygame.K_d]:
        player.pos_x = 5
        player.is_move = True

        player.move_right = True
        player.move_left = False
        player.move_up = False
        player.move_down = False

    if key[pygame.K_a]:
        player.pos_x = -5
        player.is_move = True

        player.move_right = False
        player.move_left = True
        player.move_up = False
        player.move_down = False

    if key[pygame.K_w]:
        player.pos_y = -5

        player.is_move = True

        player.move_right = False
        player.move_left = False
        player.move_up = True
        player.move_down = False

    if key[pygame.K_s]:
        player.pos_y = 5

        player.is_move = True

        player.move_right = False
        player.move_left = False
        player.move_up = False
        player.move_down = True

    if key[pygame.K_LCTRL]:
        player.fast_moving = True
    # Для прыжков
    # if key[pygame.K_SPACE]:
    #     if player.is_on_ground:
    #         player.jump = -20
    #
    #         player.is_on_ground = False
    # player.movement(height - player.rect.height)
    player.movement()


if __name__ == '__main__':
    pygame.init()
    size = width, height = (1000, 500)
    screen = pygame.display.set_mode(size)
    running = True
    clock = pygame.time.Clock()
    player = Main_hero('Main_hero_sprites/main_sprite.png', 100, 400)
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                player.is_move = False
                player.frame = 2
        move()
        screen.blit(player.image, player.rect)
        pygame.display.flip()
        clock.tick(30)
