import pygame
import numpy as np


class Mob(pygame.sprite.Sprite):
    def __init__(self, target, x, y, width, height, mob):
        self.mob = mob
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(f"img/{self.mob.capitalize()}_sprites/Run/left_{self.mob}_stop.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.width = width
        self.height = height

        self.target = target
        self.mask = pygame.mask.from_surface(self.image)

        self.make_image_lists()
        self.make_variables()

        self.sound_of_hit = None
        self.end = None
        self.is_hit = None
        self.attack_frame = None
        self.attack = None
        self.death_frame = None
        self.die = None
        self.direction = None
        self.right_frame = None
        self.left_frame = None
        self.speed_y = None
        self.speed_x = None
        self.hp = None
        self.right_stun_sprites = None
        self.left_stun_sprites = None
        self.left_attack_sprite = None
        self.right_attack_sprite = None
        self.left_die_sprite = None
        self.right_die_sprites = None
        self.right_run_sprites = None
        self.left_run_sprites = None
        self.stun = None

    def make_image_lists(self):
        self.left_run_sprites = [
            pygame.image.load(f"img/{self.mob.capitalize()}/Run/left_{self.mob}_run_{i}.png").convert_alpha() for i in
            range(1, 9)]
        self.right_run_sprites = [pygame.transform.flip(self.left_run_sprites[i], True, False) for i in range(8)]
        self.right_die_sprites = [
            pygame.image.load(f"img/{self.mob.capitalize()}_sprites/Die/right_{self.mob}_die_{i}.png").convert_alpha() for i in
            range(1, 9)]
        self.left_die_sprite = [pygame.transform.flip(self.right_die_sprites[i], True, False) for i in range(8)]
        self.right_attack_sprite = [
            pygame.image.load(f"img/{self.mob.capitalize()}_sprites/Attack/right_{self.mob}_attack_{i}.png").convert_alpha() for i in
            range(1, 8)]
        self.left_attack_sprite = [pygame.transform.flip(self.right_attack_sprite[i], True, False) for i in range(7)]
        self.left_stun_sprites = [pygame.image.load(f"img/{self.mob.capitalize()}_sprites/Attack/left_stun_{i}.png").convert_alpha()
                                  for i in range(1, 5)]
        self.right_stun_sprites = [pygame.transform.flip(self.left_stun_sprites[i], True, False) for i in range(4)]

    def make_variables(self):
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

    def determine_direction(self):
        if self.rect.x < self.target.rect.x:
            self.attack = False
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
            self.attack = False
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
            self.stun = True
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
            self.image = self.apply_red_filter(self.image)
        if self.hp <= 0:
            self.die = True

    def apply_red_filter(self, surface):
        arr = pygame.surfarray.array3d(surface)

        red_filtered = np.copy(arr)
        red_filtered[:, :, 1] = 0
        red_filtered[:, :, 2] = 0

        return pygame.surfarray.make_surface(red_filtered)
