import pygame


class Mushroom(pygame.sprite.Sprite):
    def __init__(self, target, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.end = None
        self.death_frame = None
        self.die = None
        self.direction = None
        self.right_frame = None
        self.left_frame = None
        self.speed_y = None
        self.speed_x = None
        self.left_die_sprite = None
        self.right_die_sprites = None
        self.right_stop_sprite = None
        self.right_run_sprites = None
        self.left_stop_sprite = None
        self.left_run_sprites = None
        self.is_move = None
        self.image = pygame.image.load("img/Main_hero_sprites/main_sprite.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.width = width
        self.height = height

        self.target = target
        self.mask = pygame.mask.from_surface(self.image)

        self.make_image_lists()
        self.make_variables()

    def make_image_lists(self):
        self.left_run_sprites = [pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_run_1.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_run_2.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_run_3.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_run_4.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_run_5.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_run_6.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_run_7.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_run_8.png").convert_alpha()]
        self.left_stop_sprite = pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_stop.png").convert_alpha()

        self.right_run_sprites = [
            pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_run_1.png").convert_alpha(),
            pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_run_2.png").convert_alpha(),
            pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_run_3.png").convert_alpha(),
            pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_run_4.png").convert_alpha(),
            pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_run_5.png").convert_alpha(),
            pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_run_6.png").convert_alpha(),
            pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_run_7.png").convert_alpha(),
            pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_run_8.png").convert_alpha()]
        self.right_stop_sprite = pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_stop.png").convert_alpha()

        self.right_die_sprites = [
            pygame.image.load("img/Mushroom_sprites/Die/right_mushroom_die_1.png").convert_alpha(),
            pygame.image.load("img/Mushroom_sprites/Die/right_mushroom_die_5.png").convert_alpha(),
            pygame.image.load("img/Mushroom_sprites/Die/right_mushroom_die_6.png").convert_alpha(),
            pygame.image.load("img/Mushroom_sprites/Die/right_mushroom_die_7.png").convert_alpha(),
            pygame.image.load("img/Mushroom_sprites/Die/right_mushroom_die_8.png").convert_alpha(),
            pygame.image.load("img/Mushroom_sprites/Die/right_mushroom_die_8.png").convert_alpha(),
            pygame.image.load("img/Mushroom_sprites/Die/right_mushroom_die_8.png").convert_alpha()]
        self.left_die_sprite = [pygame.image.load("img/Mushroom_sprites/Die/left_mushroom_die_1.png").convert_alpha(),
                                pygame.image.load("img/Mushroom_sprites/Die/left_mushroom_die_5.png").convert_alpha(),
                                pygame.image.load("img/Mushroom_sprites/Die/left_mushroom_die_6.png").convert_alpha(),
                                pygame.image.load("img/Mushroom_sprites/Die/left_mushroom_die_7.png").convert_alpha(),
                                pygame.image.load("img/Mushroom_sprites/Die/left_mushroom_die_8.png").convert_alpha(),
                                pygame.image.load("img/Mushroom_sprites/Die/left_mushroom_die_8.png").convert_alpha(),
                                pygame.image.load("img/Mushroom_sprites/Die/left_mushroom_die_8.png").convert_alpha()]

    def make_variables(self):
        self.is_move = True

        self.speed_x = 0
        self.speed_y = 0

        self.left_frame = 0
        self.right_frame = 0

        self.direction = "LEFT"

        self.die = False
        self.death_frame = 0

        self.end = False

    def determine_direction(self):
        if self.rect.x < self.target.rect.x:
            self.is_move = True
            self.direction = "RIGHT"
            if self.rect.y < self.target.rect.y:
                self.speed_x = 2
                self.speed_y = 2
            elif self.rect.y > self.target.rect.y:
                self.speed_x = 2
                self.speed_y = -2
            if abs(self.rect.y - self.target.rect.y) <= 5:
                self.speed_x = 2
                self.speed_y = 0

        elif self.rect.x > self.target.rect.x:
            self.is_move = True
            self.direction = "LEFT"
            if self.rect.y < self.target.rect.y:
                self.speed_x = -2
                self.speed_y = 2
            elif self.rect.y > self.target.rect.y:
                self.speed_x = -2
                self.speed_y = -2
            if abs(self.rect.y - self.target.rect.y) <= 5:
                self.speed_x = -2
                self.speed_y = 0
        if abs(self.rect.x - self.target.rect.x) <= 5:
            if self.rect.y < self.target.rect.y:
                self.speed_x = 0
                self.speed_y = 2
            elif self.rect.y > self.target.rect.y:
                self.speed_x = 0
                self.speed_y = -2
            if abs(self.rect.y - self.target.rect.y) <= 5:
                self.is_move = False
                self.speed_x = 0
                self.speed_y = 0

    def movement(self):
        self.determine_direction()
        self.put_sprites()
        if self.die:
            self.animate_death()
        else:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

    def put_sprites(self):
        if self.is_move:
            if self.direction == "LEFT":
                self.right_frame = 0
                self.left_frame += 0.3
                if self.left_frame >= 8:
                    self.left_frame = 0
                self.image = self.left_run_sprites[int(self.left_frame)]
            else:
                self.left_frame = 0
                self.right_frame += 0.3
                if self.right_frame >= 8:
                    self.right_frame = 0
                self.image = self.right_run_sprites[int(self.right_frame)]
        else:
            if self.direction == "LEFT":
                self.image = self.left_stop_sprite
            else:
                self.image = self.right_stop_sprite

    def animate_death(self):
        coefficient = 0.3
        if self.death_frame > 4:
            coefficient = 0.05
        self.death_frame += coefficient
        if self.death_frame > 6:
            self.die = False
            self.end = True
        if self.direction == "LEFT":
            self.image = self.left_die_sprite[int(self.death_frame)]
        else:
            self.image = self.right_die_sprites[int(self.death_frame)]
