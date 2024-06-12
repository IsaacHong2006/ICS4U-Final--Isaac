import pygame
from player import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        direction = player.status.split('_')[0]



        #graphic
        self.image = pygame.Surface((30,30))

        #placing
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright)
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft)
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom)
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop)