#This will contain all the sprites and manage their working in the game
import pygame
from settings import *
from player import Player
from tiles import Tile
from debug import debug
from pytmx.util_pygame import load_pygame
from supporting import *
from random import choice
from random import choices
from ui import *
from enemy import *
from weapon_ import Weapon
from sideMenus import Upgrade
from elderTree import *

class Level:
    def __init__(self):
        #display surface
        self.draw_surface = pygame.display.get_surface()
        self.game_paused = False
        self.interaction_paused = False

        #Group set-up of sprites
        # self.visible_sprites = pygame.sprite.Group (was changed to play around with the camera)
        self.visible_sprites = YSortCameraGroup() 
        self.obstacles_sprites = pygame.sprite.Group()
        
        #interactable sprite (elder tree)
        self.interactable_sprites = pygame.sprite.Group()


        #attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        
        #setup for sprite
        self.create_map()

        #user interface set up
        self.ui = User_Interface()
        self.upgrade = Upgrade(self.player)
        self.gamble_screen = GambleMenu(self.player)
        self.gamble = None

    def create_map(self):
        layouts = {
                'boundary': import_csv_layout('graphics/tilemap/MyMap_No Move.csv'),
                'bush': import_csv_layout('graphics/tilemap/MyMap_BUSH.csv'),
                'trees and bolders': import_csv_layout('graphics/tilemap/MyMap_TREES AND BOLDERS.csv'),
                'entities' : import_csv_layout('graphics/tilemap/MyMap_Peeps.csv')
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
                            Tile((x,y), [self.visible_sprites, self.obstacles_sprites, self.attackable_sprites], 'bushes', random_bush)

                        if style == 'trees and bolders': #trees and bolders
                            surface = graphics['trees and bolders'][int(col)]
                            if col == '1':
                                Elder_Tree((x,y), [self.visible_sprites, self.interactable_sprites])
                            else:
                                Tile((x ,y - 60), [self.visible_sprites, self.obstacles_sprites], 'trees and bolders', surface)

                        if style == 'entities':
                            if col == '172':
                                self.player = Player(
                                    (x,y), #position
                                    [self.visible_sprites],
                                    self.obstacles_sprites, 
                                    self.create_attack,
                                    self.destroy_attack)
                                
                            elif col == '1130':
                                monster_list = ["slime", "blobby"]
                                rng = [0.7, 0.3]
                                monster_name = choices(monster_list, weights = rng, k = 1) [0]
                                Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites], self.obstacles_sprites,self.damage_player,self.xp_add)
                            else:
                                Enemy('arch-angel',(x,y),[self.visible_sprites,self.attackable_sprites], self.obstacles_sprites,self.damage_player,self.xp_add)
                                                    
    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.attack_sprites])
        
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'bushes':
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player)
                
    def damage_player(self,amount):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def check_interactions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB]:
            for sprite in self.interactable_sprites:
                if sprite.rect.colliderect(self.player.rect):
                    self.handling_interactions(sprite)
    
    def handling_interactions(self, sprite):
        if isinstance(sprite,Elder_Tree):
            if not sprite.interacted:
                sprite.interact()
                self.gambleToggle()

    def xp_add(self, amount):
        self.player.exp += amount

    def toggleMenu(self):
        self.game_paused = not self.game_paused

    def gambleToggle(self):
        self.game_paused = not self.game_paused
        self.gamble = not self.gamble

    def run(self):
        self.visible_sprites.custom_draw(self.player) #this draws from the custom draw and passes the player in so we can access it in custom_draw
        self.ui.display(self.player)
        if self.game_paused and self.gamble:
            self.gamble_screen.display()
        elif self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.update_enemy(self.player)
            self.player_attack_logic()

        self.check_interactions()
        

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

    def update_enemy(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)