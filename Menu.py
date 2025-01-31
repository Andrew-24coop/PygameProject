import pygame

from pygame import font
import pygame_widgets
from pygame_widgets.button import Button


from main import main

from settings import *
from Refer import *

from random import choice
class Main_background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/Main_menu_background/menu_background.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.coefficient = 1
        self.delay = 0
    def movement(self):
        self.delay += 1
        if self.delay == 3:
            self.delay = 0
            if self.rect.x + WIDTH == 800 or self.rect.x == 0:
                self.coefficient = -self.coefficient
            self.rect.x += self.coefficient

class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode(SIZE)
        font.init()
        self.background = Main_background()
        self.title = font.Font("fonts/PixelifySans-SemiBold.ttf", 100)
        self.title = self.title.render("Rise of Empire", True, (200, 201, 8))
        self.refer = Refer(self)
        self.running = True

        #self.game = Game()
        #self.show_game = False

        self.button_click_sound = pygame.mixer.Sound("sounds/knopka-vyiklyuchatelya1.mp3")

    def showing_refer(self):
        self.button_click_sound.play()
        self.refer.showing_refer = True
        self.show_game = False

    def make_game_true(self):
        self.button_click_sound.play()
        self.running = False
        pygame.time.wait(100)
        #self.show_game = True
        print("INTO")
        self.button1.hide()
        self.button2.hide()
        self.button3.hide()
        main()
        #self.refer.showing_refer = False

    def exit(self):
        self.button_click_sound.play()
        pygame.time.wait(1000)
        self.running = False

    def Game(self):
        self.button1 = Button(
            # Mandatory Parameters
            self.screen,  # Surface to place button on
            385,  # X-coordinate of top left corner
            150,  # Y-coordinate of top left corner
            200,  # Width
            80,  # Height

            # Optional Parameters
            text='Играть',  # Text to display
            fontSize=50,  # Size of font
            margin=20,  # Minimum distance between text/image and edge of button
            inactiveColour=(248, 237, 176),  # Colour of button when not being interacted with
            hoverColour=(252, 227, 88),  # Colour of button when being hovered over
            pressedColour=(236, 180, 8),  # Colour of button when being clicked
            radius=5,  # Radius of border corners (leave empty for not curved)
            onClick=lambda: self.make_game_true()  # Function to call when clicked on
        )
        self.button2 = Button(
            # Mandatory Parameters
            self.screen,  # Surface to place button on
            385,  # X-coordinate of top left corner
            250,  # Y-coordinate of top left corner
            200,  # Width
            80,  # Height

            # Optional Parameters
            text='Справка',  # Text to display
            fontSize=50,  # Size of font
            margin=20,  # Minimum distance between text/image and edge of button
            inactiveColour=(248, 237, 176),  # Colour of button when not being interacted with
            hoverColour=(252, 227, 88),  # Colour of button when being hovered over
            pressedColour=(236, 180, 8),  # Colour of button when being clicked
            radius=5,  # Radius of border corners (leave empty for not curved)
            onClick=lambda: self.showing_refer()  # Function to call when clicked on
        )
        self.button3 = Button(
            # Mandatory Parameters
            self.screen,  # Surface to place button on
            385,  # X-coordinate of top left corner
            350,  # Y-coordinate of top left corner
            200,  # Width
            80,  # Height

            # Optional Parameters
            text='Выход',  # Text to display
            fontSize=50,  # Size of font
            margin=20,  # Minimum distance between text/image and edge of button
            inactiveColour=(248, 237, 176),  # Colour of button when not being interacted with
            hoverColour=(252, 227, 88),  # Colour of button when being hovered over
            pressedColour=(236, 180, 8),  # Colour of button when being clicked
            radius=5,  # Radius of border corners (leave empty for not curved)
            onClick=lambda: self.exit()  # Function to call when clicked on
        )
        pygame.init()
        pygame.display.set_caption("Rise of Empire")
        clock = pygame.time.Clock()
        self.screen.fill((0, 0, 0))
        musics = ["sounds/1-09_-oxygene.mp3", "sounds/1-10_-equinoxe.mp3", "sounds/1-12_-dry-hands.mp3"]
        pygame.mixer.music.load(choice(musics))
        pygame.mixer.music.play(-1)
        while self.running:
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            if keys[pygame.K_ESCAPE] and self.refer.showing_refer:
               self.button_click_sound.play()
               pygame.time.wait(50)
               self.refer.showing_refer = False
            if self.refer.showing_refer:
                self.refer.show_refer(self.screen)
            # elif self.show_game:
            #     self.game.main()
            else:
                self.screen.fill((0, 0, 0))
                self.background.movement()
                self.screen.blit(self.background.image, self.background.rect)
                self.screen.blit(self.title, (165, 10))
                pygame_widgets.update(events)
            pygame.display.update()
            clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    menu = Menu()
    menu.Game()
