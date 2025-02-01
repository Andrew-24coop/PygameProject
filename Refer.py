import pygame
from pygame import font

from settings import *


class ReferBackground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        super().__init__()
        self.image = pygame.image.load("img/Main_menu_background/Refer_background/1.jpeg")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.frame = 0
        self.background_sprites = [pygame.image.load(f"img/Main_menu_background/Refer_background/{i}.jpeg")
                                   for i in range(1, 9)]

    def change_sprite(self):
        self.frame += 0.1
        if self.frame > 7.8:
            self.frame = 0
        self.image = self.background_sprites[int(self.frame)]


class Refer:
    def __init__(self):
        font.init()
        self.screen = pygame.display.set_mode(SIZE)

        self.pygame_text = font.Font("fonts/RobotoSlab-Medium.ttf", 20)
        self.text = []
        self.coefficient = 10
        with open("refer", 'r', encoding="utf-8") as refer:
            self.text = refer.readlines()

        self.background = ReferBackground()
        self.showing_refer = False

    def draw_text(self, screen):
        for line in self.text:
            line = line.strip()
            text = self.pygame_text.render(line, True, (236, 180, 8))
            if self.coefficient == 350:
                text = self.pygame_text.render(line, True, (240, 10, 5))
            screen.blit(text, (20, self.coefficient))
            self.coefficient += 20
        self.coefficient = 10

    def show_refer(self, screen):
        pygame.init()

        screen.fill((0, 0, 0))
        self.background.change_sprite()
        screen.blit(self.background.image, self.background.rect)
        self.draw_text(screen)
