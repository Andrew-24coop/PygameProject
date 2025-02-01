import pygame
import numpy as np
from random import randint
from settings import *


class Mushroom(pygame.sprite.Sprite):
    def __init__(self, target, world, speed, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("img/Mushroom_sprites/Run/left_mushroom_stop.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.width = width
        self.height = height

        self.target = target
        self.mask = pygame.mask.from_surface(self.image)

        self.world = world

        self.hp = 10
        self.speed_x = 0
        self.speed_y = 0

        self.left_frame = 0
        self.right_frame = 0

        self.direction = "LEFT"

        self.die = False
        self.death_frame = 0

        self.attack = False
        self.attack_frame = 0

        self.is_hit = False

        self.end = False

        self.sound_of_hit = pygame.mixer.Sound("sounds/udar-priglushennyiy-reshitelnyiy (mp3cut.net).mp3")

        self.ready = False

        self.speed = speed

        self.left_run_sprites = [
            pygame.image.load(f"img/Mushroom_sprites/Run/left_mushroom_run_{i}.png").convert_alpha() for i in
            range(1, 9)]
        self.right_run_sprites = [pygame.transform.flip(self.left_run_sprites[i], True, False) for i in range(8)]
        self.right_die_sprites = [
            pygame.image.load(f"img/Mushroom_sprites/Die/right_mushroom_die_{i}.png").convert_alpha() for i in
            range(1, 9)]
        self.left_die_sprite = [pygame.transform.flip(self.right_die_sprites[i], True, False) for i in range(8)]
        self.right_attack_sprite = [
            pygame.image.load(f"img/Mushroom_sprites/Attack/right_mushroom_attack_{i}.png").convert_alpha() for i in
            range(1, 8)]
        self.left_attack_sprite = [pygame.transform.flip(self.right_attack_sprite[i], True, False) for i in range(7)]
        self.left_stun_sprites = [pygame.image.load(f"img/Mushroom_sprites/Attack/left_stun_{i}.png").convert_alpha()
                                  for i in range(1, 5)]
        self.right_stun_sprites = [pygame.transform.flip(self.left_stun_sprites[i], True, False) for i in range(4)]

    def determine_direction(self):
        if self.rect.x < self.target.rect.x:
            self.attack = False
            self.direction = "RIGHT"
            if self.rect.y < self.target.rect.y:
                self.speed_x = self.speed
                self.speed_y = self.speed
            elif self.rect.y > self.target.rect.y:
                self.speed_x = self.speed
                self.speed_y = -self.speed
            if abs(self.rect.y - self.target.rect.y) <= 5:
                self.speed_x = self.speed
                self.speed_y = 0

        elif self.rect.x > self.target.rect.x:
            self.attack = False
            self.direction = "LEFT"
            if self.rect.y < self.target.rect.y:
                self.speed_x = -self.speed
                self.speed_y = self.speed
            elif self.rect.y > self.target.rect.y:
                self.speed_x = -self.speed
                self.speed_y = -self.speed
            if abs(self.rect.y - self.target.rect.y) <= 5:
                self.speed_x = -self.speed
                self.speed_y = self.speed
        if abs(self.rect.x - self.target.rect.x) <= 5:
            if self.rect.y < self.target.rect.y:
                self.speed_x = 0
                self.speed_y = self.speed
            elif self.rect.y > self.target.rect.y:
                self.speed_x = 0
                self.speed_y = -self.speed
            if abs(self.rect.y - self.target.rect.y) <= 5:
                self.attack = True
                self.speed_x = 0
                self.speed_y = 0
        elif abs(self.rect.x - self.target.rect.x) <= 30 and abs(self.rect.y - self.target.rect.y) <= 5:
            self.attack = True
            self.speed_x = 0
            self.speed_y = 0

        if abs(self.rect.x - self.target.rect.x) <= 40 and abs(self.rect.y - self.target.rect.y) <= 20:
            self.is_hit = True

    def movement(self):
        if self.ready:
            self.determine_direction()
            self.check_hit()
            if self.die:
                self.animate_death()
            elif self.attack:
                self.animate_attack()
            else:
                self.put_sprites()
                self.rect.x += self.speed_x
                self.rect.y += self.speed_y
            self.rect.x -= self.target.map_offset[0]
            self.rect.y -= self.target.map_offset[1]

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

    def animate_death(self):
        coefficient = 0.3
        if self.death_frame > 7:
            coefficient = 0.01
        self.death_frame += coefficient
        if 0.6 < self.death_frame < 3:
            if self.direction == "LEFT":
                self.rect.x += 1
            else:
                self.rect.x -= 1
        elif 3 < self.death_frame < 4:
            if self.direction == "LEFT":
                self.rect.x -= 2
            else:
                self.rect.x += 2
        if self.death_frame > 8:
            self.die = False
            self.end = True
            self.death_frame = 0
        if self.direction == "LEFT":
            self.image = self.left_die_sprite[int(self.death_frame)]
        else:
            self.image = self.right_die_sprites[int(self.death_frame)]

    def animate_attack(self):
        self.attack_frame += 0.4
        if self.attack_frame > 6.4:
            self.attack = False
            self.attack_frame = 0
            self.target.hp -= 0.4
        if self.attack_frame < 3.2:
            if self.direction == "LEFT":
                self.rect.x -= 3
            else:
                self.rect.x += 3
        elif self.attack_frame > 3.2:
            if self.attack_frame >= 6:
                self.sound_of_hit.play()
            self.target.image = self.target.apply_red_filter(self.target.image)
            if self.direction == "LEFT":
                self.rect.x += 3
            else:
                self.rect.x -= 3
        if self.direction == "LEFT":
            self.image = self.left_attack_sprite[int(self.attack_frame)]
        else:
            self.image = self.right_attack_sprite[int(self.attack_frame)]

    def check_hit(self):
        if self.target.sword_frame > 0.8 and self.is_hit:
            self.is_hit = False
            self.hp -= self.target.damage
            self.target.sword_hit_sound.play()
            self.target.energy += 1
            if self.target.energy > 5:
                self.target.energy = 5
            self.image = apply_red_filter(self.image)
        if self.hp <= 0:
            self.die = True


class Mushrooom_group:
    def __init__(self):
        self.mushrooms = []

    def spawn(self, n, boss_coords, player, current_world, group):
        for i in range(n):
            mushroom = Mushroom(player, current_world, randint(1, 5), randint(boss_coords[0] - 50, boss_coords[0] + 50),
                                randint(boss_coords[1] - 50, boss_coords[1] + 50), WIDTH, HEIGHT)
            self.mushrooms.append(mushroom)
            group.add(mushroom)

    def move(self, screen, group):
        for mushroom in self.mushrooms:
            mushroom.ready = True
            mushroom.movement()
            screen.blit(mushroom.image, mushroom.rect)
            if mushroom.end:
                self.mushrooms.remove(mushroom)
                group.remove(mushroom)
                del mushroom

def apply_red_filter(surface):
    arr = pygame.surfarray.array3d(surface)  # Получаем цветовую составляющую

    # Убираем зеленую и синюю составляющие, оставляя красную
    red_filtered = np.copy(arr)
    red_filtered[:, :, 1] = 0  # Убираем зеленый канал
    red_filtered[:, :, 2] = 0  # Убираем синий канал

    return pygame.surfarray.make_surface(red_filtered)