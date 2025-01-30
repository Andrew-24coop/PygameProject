import pygame
import numpy as np

from random import choice, randint


class Mob(pygame.sprite.Sprite):
    def __init__(self, player, x, y, mob):
        super().__init__()
        self.player = player
        self.mob = mob

        if mob == "cow":
            self.make_cow(x, y)
        elif mob == "pig":
            self.make_pig(x, y)
        # else:
        #     self.make_chicken(x, y)

        self.speed_x = 0
        self.speed_y = 0

        self.direction = "LEFT"

        self.die = False

        self.actions = {"stop": lambda: self.animate_stop(), "move": lambda: self.animate_move(), "eat": lambda: self.animate_eat()}
        self.current_action = None

        self.eat_frame = 0
        self.eat_coefficient = 0.2

        self.change_speed = True
        self.moving_frame = 0

        self.delay = 0
        self.hit_delay = 0
    def make_cow(self, x, y):
        self.image = pygame.image.load("img/Mobs/Cow/cow_1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.right_walk_sprites = [pygame.image.load(f"img/Mobs/Cow/cow_{i}.png").convert_alpha() for i in range(1, 9)]
        self.left_walk_sprites = [pygame.transform.flip(i, True, False) for i in self.right_walk_sprites]

        self.right_eat_sprites = [pygame.image.load(f"img/Mobs/Cow/cow_eats_{i}.png").convert_alpha() for i in range(1, 3)]
        self.left_eat_sprites = [pygame.transform.flip(i, True, False) for i in self.right_eat_sprites]

        self.mask = pygame.mask.from_surface(self.image)

        self.hp = 5

        self.food = "beef"

        self.death_sound = pygame.mixer.Sound("sounds/cow_death.mp3")
        self.hurt_sound = pygame.mixer.Sound("sounds/cow_hurt.mp3")

    def make_pig(self, x, y):
        self.image = pygame.image.load("img/Mobs/Pig/pig_1.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.right_walk_sprites = [pygame.image.load(f"img/Mobs/Pig/pig_{i}.png").convert_alpha() for i in range(1, 10)]
        self.left_walk_sprites = [pygame.transform.flip(i, True, False) for i in self.right_walk_sprites]

        self.right_eat_sprites = [pygame.image.load(f"img/Mobs/Pig/pig_eats_{i}.png").convert_alpha() for i in range(1, 3)]
        self.left_eat_sprites = [pygame.transform.flip(i, True, False) for i in self.right_eat_sprites]

        self.mask = pygame.mask.from_surface(self.image)

        self.hp = 5

        self.food = "pork"

        self.death_sound = pygame.mixer.Sound("sounds/pig_death.mp3")
        self.hurt_sound = pygame.mixer.Sound("sounds/pig_hurt (mp3cut.net).mp3")

    def animate_stop(self):
        self.eat_frame = 0
        self.eat_coefficient = 0.2
        self.moving_frame = 0
        self.speed_x = 0
        self.speed_y = 0
        self.change_speed = True

        if self.direction == "RIGHT":
            self.image = self.right_walk_sprites[0]
        else:
            self.image = self.left_walk_sprites[0]

    def animate_move(self):
        self.eat_frame = 0
        self.eat_coefficient = 0.2
        if self.change_speed:
            self.speed_x = choice([-2, -1, 1, 2])
            self.speed_y = choice([-2, -1, 1, 2])
            if self.speed_x > 0:
                self.direction = "RIGHT"
            else:
                self.direction = "LEFT"
            self.change_speed = False
        self.moving_frame += 0.2
        if self.moving_frame > len(self.right_walk_sprites) - 1:
            self.moving_frame = 0
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.direction == "RIGHT":
            self.image = self.right_walk_sprites[int(self.moving_frame)]
        else:
            self.image = self.left_walk_sprites[int(self.moving_frame)]

    def animate_eat(self):
        self.speed_x = 0
        self.speed_y = 0
        self.moving_frame = 0
        self.change_speed = True

        if self.eat_frame >= 2 or self.eat_frame <= 0:
            self.eat_coefficient = -self.eat_coefficient
        self.eat_frame += self.eat_coefficient
        if self.direction == "RIGHT":
            self.image = self.right_eat_sprites[int(self.eat_frame)]
        else:
            self.image = self.left_eat_sprites[int(self.eat_frame)]

    def check_hit(self):
        if self.hit_delay == 0:
            if pygame.sprite.collide_mask(self, self.player):
                if self.player.sword_attack:
                    self.hp = self.hp - 1
                    self.hurt_sound.play()
                    self.player.energy += 1
                    if self.player.energy > 5:
                        self.player.energy = 5
                    self.player.sword_hit_sound.play()
                    self.hit_delay += 0.1
        else:
            self.hit_delay += 0.2
            if self.hit_delay > 1:
                self.hit_delay = 0
            self.image = self.apply_red_filter(self.image)

    def apply_red_filter(self, surface):
        arr = pygame.surfarray.array3d(surface)

        red_filtered = np.copy(arr)
        red_filtered[:, :, 1] = 0
        red_filtered[:, :, 2] = 0

        return pygame.surfarray.make_surface(red_filtered)

    def movement(self):
        if not self.die:
            if self.delay == 0:
                self.delay += 1
                self.current_action = choice(["stop", "move", "move", "eat"])
            else:
                self.delay += 0.5
                if self.delay >= 30:
                    self.delay = 0
            self.actions[self.current_action]()
            self.check_hit()
            self.rect.x -= self.player.map_offset[0]
            self.rect.y -= self.player.map_offset[1]
            if self.hp < 0:
                self.die = True
                self.death_sound.play()


class Food(pygame.sprite.Sprite):
    def __init__(self, player, mob):
        super().__init__()
        if mob.mob == "cow":
            self.image = pygame.image.load("img/Mobs/Cow/beef_sprite.png").convert_alpha()
        else:
            self.image = pygame.image.load("img/Mobs/Pig/pork_sprite.png").convert_alpha()
        self.rect = self.image.get_rect(center=(mob.rect.x + 5, mob.rect.y + 5))
        self.mask = pygame.mask.from_surface(self.image)

        self.player = player
        self.end = False

        self.eating_sound = pygame.mixer.Sound("sounds/eating_sound.mp3")
    def check_collision(self):
        self.rect.x -= self.player.map_offset[0]
        self.rect.y -= self.player.map_offset[1]
        if pygame.sprite.collide_mask(self, self.player):
            self.player.food += 2
            if self.player.food > 5:
                self.player.food = 5
            self.end = True
            self.eating_sound.play()



class Mob_group:
    def __init__(self, mob, player, group):
        if mob == "cow":
            self.mob = "cow"
        elif mob == "pig":
            self.mob = "pig"
        else:
            self.mob = "chicken"
        self.mobs = []
        self.food = []
        self.player = player
        self.group = group

    def spawn(self, n):
        for i in range(n):
            mob = Mob(self.player, randint(10, 3000), randint(10, 3000), self.mob)
            self.mobs.append(mob)
            self.group.add(mob)
            self.food.append(Food(self.player, mob))
    def move(self, screen):
        for i in range(len(self.mobs)):
            self.mobs[i].movement()
            if self.mobs[i].die:
                screen.blit(self.food[i].image, self.food[i].rect)
                self.food[i].check_collision()
                if self.food[i].end:
                    self.mobs.pop(i)
                    self.food.pop(i)
                    break
            else:
                screen.blit(self.mobs[i].image, self.mobs[i].rect)


