import sys

import pygame

import pygame_widgets
from pygame_widgets.button import Button

from settings import *

class Death_window(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.death_picture = pygame.image.load("img/Final_windows/death_message.png")
        self.picture_rect = self.death_picture.get_rect(center=(500, 100))

        self.reborn = False
        self.running = True

        self.button_click_sound = pygame.mixer.Sound("sounds/knopka-vyiklyuchatelya1.mp3")

    def exit(self):
        self.button_click_sound.play()
        pygame.time.wait(1000)
        self.running = False

    def make_reborn_true(self):
        self.button_click_sound.play()
        pygame.time.wait(1000)
        self.reborn = True

    def show(self):
        self.button1 = Button(
            # Mandatory Parameters
            self.screen,  # Surface to place button on
            300,  # X-coordinate of top left corner
            200,  # Y-coordinate of top left corner
            400,  # Width
            100,  # Height

            # Optional Parameters
            text='Возрождение',  # Text to display
            fontSize=50,  # Size of font
            margin=20,  # Minimum distance between text/image and edge of button
            inactiveColour=(128, 126, 125),  # Colour of button when not being interacted with
            hoverColour=(94, 92, 91),  # Colour of button when being hovered over
            pressedColour=(200, 200, 200),  # Colour of button when being clicked
            radius=5,  # Radius of border corners (leave empty for not curved)
            onClick=lambda: self.make_reborn_true()  # Function to call when clicked on
        )
        self.button2 = Button(
            # Mandatory Parameters
            self.screen,  # Surface to place button on
            300,  # X-coordinate of top left corner
            330,  # Y-coordinate of top left corner
            400,  # Width
            100,  # Height

            # Optional Parameters
            text='Выход',  # Text to display
            fontSize=50,  # Size of font
            margin=20,  # Minimum distance between text/image and edge of button
            inactiveColour=(128, 126, 125),  # Colour of button when not being interacted with
            hoverColour=(94, 92, 91),  # Colour of button when being hovered over
            pressedColour=(200, 200, 200),  # Colour of button when being clicked
            radius=5,  # Radius of border corners (leave empty for not curved)
            onClick=lambda: self.exit()  # Function to call when clicked on
        )
        self.screen.fill((152, 26, 26))
        self.screen.blit(self.death_picture, self.picture_rect)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        pygame_widgets.update(events)
        pygame.display.update()


