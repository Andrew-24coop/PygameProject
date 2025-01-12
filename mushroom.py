import pygame
class Mushroom(pygame.sprite.Sprite):
    def __init__(self, target, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("img/Main_hero_sprites/main_sprite.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.width = width
        self.height = height

        self.make_image_lists()
        self.make_variables()

        self.target = target

    def make_image_lists(self):
        self.left_run_sprites = [pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_run_1.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_run_2.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_run_3.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_run_4.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_run_5.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_run_6.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_run_7.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_run_8.png").convert_alpha()]

        self.right_run_sprites = [pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_run_1.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_run_2.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_run_3.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_run_4.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_run_5.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_run_6.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_run_7.png").convert_alpha(),
                                 pygame.image.load("img/Mushroom_sprites/Run/right_mushroom_run_8.png").convert_alpha()]
    def make_variables(self):
        self.speed_x = 0
        self.speed_y = 0

        self.left_frame = 0
        self.right_frame = 0

        self.direction = "LEFT"

    def determine_direction(self):
        if self.rect.x < self.target.rect.x:
            self.direction = "RIGHT"
            if self.rect.y < self.target.rect.y:
                self.speed_x = 2
                self.speed_y = 2
            elif self.rect.y > self.target.rect.y:
                self.speed_x = 2
                self.speed_y = -2
            elif self.rect.y == self.target.rect.y:
                self.speed_x = 2
                self.speed_y = 0

        elif self.rect.x > self.target.rect.x:
            self.direction = "LEFT"
            if self.rect.y < self.target.rect.y:
                self.speed_x = -2
                self.speed_y = 2
            elif self.rect.y > self.target.rect.y:
                self.speed_x = -2
                self.speed_y = -2
            elif self.rect.y == self.target.rect.y:
                self.speed_x = -2
                self.speed_y = 0
        elif self.rect.x == self.target.rect.x:
            self.direction = "LEFT"
            if self.rect.y < self.target.rect.y:
                self.speed_x = 0
                self.speed_y = 2
            elif self.rect.y > self.target.rect.y:
                self.speed_x = 0
                self.speed_y = -2
            elif self.rect.y == self.target.rect.y:
                self.speed_x = 0
                self.speed_y = 0
    def movement(self):
        self.determine_direction()
        self.put_sprites()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def put_sprites(self):
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



