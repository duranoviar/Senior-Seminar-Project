import pygame
import random
from pygame.locals import *

from globals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, speed=3):
        pygame.sprite.Sprite.__init__(self)

        # get the display surface
        self.game_display = pygame.display.get_surface()

        # load image
        self.player_img = pygame.image.load('player/player.gif')
        self.rect = self.player_img.get_rect()

        # define attributes of Player
        self.rect.x = (DISPLAY_WIDTH * 0.45)
        self.rect.y = (DISPLAY_HEIGHT * 0.8)
        self.change_x = 0
        self.speed = speed
        # display original position of player
        self.game_display.blit(self.player_img, (self.rect.x, self.rect.y))

    def update(self):
        # update the position of the player
        self.rect.x += self.change_x
        self.game_display.blit(self.player_img, (self.rect.x, self.rect.y))

class Missile(pygame.sprite.Sprite):
    def __init__(self, sprite, missile_img, down=True, speed=4):
        pygame.sprite.Sprite.__init__(self)

        # get the display surface
        self.game_display = pygame.display.get_surface()

        # load image
        self.missile_img = pygame.image.load(missile_img)
        self.rect = self.missile_img.get_rect()

        # define attributes of Missile
        self.rect.x = sprite.rect.x + 17
        self.rect.y = sprite.rect.y
        if down:
            self.speed = speed
        else:
            self.speed = -speed

    def update(self):
        # fire missile from where the player is
        self.rect.y -= self.speed
        self.game_display.blit(self.missile_img, (self.rect.x, self.rect.y))


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed=2, pu_type=None):
        pygame.sprite.Sprite.__init__(self)

        # define the type of powerup
        self.pu_type = pu_type

        # get the display surface
        self.game_display = pygame.display.get_surface()

        # load image
        self.power_up_image = pygame.image.load(PU_TYPE_IMAGE[self.pu_type])
        self.rect = self.power_up_image.get_rect()

        # define attributes of the powerup
        self.rect.x = random.randrange(0, DISPLAY_WIDTH)
        self.rect.y = -DISPLAY_HEIGHT
        self.speed = speed


    def update(self):
        # update the position of the powerup
        self.rect.y += self.speed
        self.game_display.blit(self.power_up_image, (self.rect.x, self.rect.y))

    def reset(self):
        # reset the powerup position
        self.rect.x = random.randrange(0, DISPLAY_WIDTH)
        self.rect.y = -50


class BasicEnemy(pygame.sprite.Sprite):
    def __init__(self, speed=2):
        pygame.sprite.Sprite.__init__(self)

        # get the display surface
        self.game_display = pygame.display.get_surface()

        # load image
        self.basic_enemy_img = pygame.image.load('enemies/basic_enemy.gif')
        self.rect = self.basic_enemy_img.get_rect()

        # define attributes of the enemy
        self.rect.x = random.randrange(0, DISPLAY_WIDTH)
        self.rect.y = -DISPLAY_HEIGHT
        self.speed = speed

    def update(self):
        # update the position of the enemy
        self.rect.y += self.speed
        self.game_display.blit(self.basic_enemy_img, (self.rect.x, self.rect.y))

    def reset(self):
        # reset the enemy position
        self.rect.x = random.randrange(0, DISPLAY_WIDTH)
        self.rect.y = -50


class Button(pygame.sprite.Sprite):
    """Class used to create a button, use setCords to set 
        position of topleft corner. Method pressed() returns
        a boolean and should be called inside the input loop."""
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game_display = pygame.display.get_surface()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = x,y

    def pressed(self,mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False

    def update(self):
        self.game_display.blit(self.image, (self.rect.x, self.rect.y))


def get_high_score():
    with open(SCORE_FILE, 'r') as score_file:
        return score_file.read().split(" ")

def write_high_score(name, score):
    with open(SCORE_FILE, 'w') as score_file:
        string = name + " " + str(score)
        score_file.write(string)
