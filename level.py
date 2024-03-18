#This will contain all the sprites and manage their working in the game
import pygame
from settings import *
from player import Player
from tiles import Tile
from debug import debug

class Level:
    def __init__(self):
        #display surface
        self.draw_surface = pygame.display.get_surface()

        #Group set-up of sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        #setup for sprite
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for straight_index, straight in enumerate(row):
                x = straight_index * TILESIZE
                y = row_index * TILESIZE
                if straight == 'x':
                    Tile((x,y),[self.visible_sprites, self.obstacles_sprites])
                if straight == 'p':
                    self.player = Player((x,y),[self.visible_sprites],self.obstacles_sprites)
        
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.direction)

class YSortCameraGroup(pygame.sprite.Group): 
    def __init__(self):

        #general setups
        super().__init__()
        self.draw_surface = pygame.display.get_surface()
        self.half_width = self.draw_surface.get_size()[0] // 2
        self.half_height = self.draw_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
    
    
    def custom_draw(self,player):
        #Offsetting the camera
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.draw_surface.blit(sprite.image, offset_pos)