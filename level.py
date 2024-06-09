#This will contain all the sprites and manage their working in the game
import pygame
from settings import *
from player import Player
from tiles import Tile
from debug import debug
from pytmx.util_pygame import load_pygame
from supporting import *
from random import choice

class Level:
    def __init__(self):
        #display surface
        self.draw_surface = pygame.display.get_surface()

        #Group set-up of sprites
        # self.visible_sprites = pygame.sprite.Group (was changed to play around with the camera)
        self.visible_sprites = YSortCameraGroup() 
        self.obstacles_sprites = pygame.sprite.Group()

        #setup for sprite
        self.create_map()

    def create_map(self):
        layouts = {
                'boundary': import_csv_layout('graphics/tilemap/MyMap_No Move.csv'),
                'bush': import_csv_layout('graphics/tilemap/MyMap_BUSH.csv'),
                'trees and bolders': import_csv_layout('graphics/tilemap/MyMap_TREES AND BOLDERS.csv')
        }
        graphics = {
            'bushes': import_folder('graphics/bush'),
            'trees and bolders': import_folder('graphics/treesandbolders')
        }
        
        for style,layout in layouts.items():
            for row_index, row in enumerate (layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacles_sprites], 'invisible')
                        if style == 'bush': #bush tiles
                            random_bush = choice(graphics['bushes'])
                            Tile((x,y), [self.visible_sprites, self.obstacles_sprites], 'bushes', random_bush)
                        if style == 'trees and bolders': #trees and bolders
                            surface = graphics['trees and bolders'][int(col)]
                            Tile((x ,y - 60), [self.visible_sprites, self.obstacles_sprites], 'trees and bolders', surface)
                            pass

                        
        self.player = Player((500,600),[self.visible_sprites],self.obstacles_sprites, )
        
    def run(self):
        self.visible_sprites.custom_draw(self.player) #this draws from the custom draw and passes the player in so we can access it in custom_draw
        self.visible_sprites.update()
        debug(self.player.direction)

class YSortCameraGroup(pygame.sprite.Group): 
    def __init__(self):
        #init method- to initialise the attributes of an object as it is formed

        #general setups
        super().__init__()# to initialise the sprite class so we can access it
        self.draw_surface = pygame.display.get_surface() #gets the surface in which eveything is drawn, so that we can use it in the class
        self.half_width = self.draw_surface.get_size()[0] // 2 #halfing (and flooring) the size of the drawn surface (x-coords) so that the player is at the centre of the screen.
        #[0] index is used because .get_size gives us (x,y)
        self.half_height = self.draw_surface.get_size()[1] // 2 #halfing (and flooring) the size of the drawn surface (y-coords) so that the player is at the centre of the screen.
        self.offset = pygame.math.Vector2() #a vector is created, and is then added to the offset position
    
        #creating the map
        self.floor_surface = pygame.image.load('graphics/tilemap/MyMap.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))

    def custom_draw(self,player):
        #self is important for the camera, player is for the collisions

        #Offsetting the camera based on the camera
        self.offset.x = player.rect.centerx - self.half_width #geometry based drawing, by subtracting instead of adding we move towards the desired direction. 
        self.offset.y = player.rect.centery - self.half_height

        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.draw_surface.blit(self.floor_surface, floor_offset_pos)


        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset #new position, which allows for the offset. 
            self.draw_surface.blit(sprite.image, offset_pos)
