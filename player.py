import pygame
from settings import *
from supporting import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacles_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/egg.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)

        #graphic setup
        self.import_player_assets()
        self.status = 'down'

        #movement
        self.speed = 5
        self.attack = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacles_sprites = obstacles_sprites

        #statistics of player
        self.stats = {'health': 50, 'energy': 20, 'attack' : 5, 'speed' : 2}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']

    def import_player_assets(self):
        character_path = 'graphics/playeranimations/'
        self.animations = {
            'up':[],'down':[],'left':[],'right':[],
            'up_idle':[],'down_idle':[],'left_idle':[],'right_idle':[],
            'up_attack':[],'down_attack':[],'left_attack':[],'right_attack':[],
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
        #Moving   
        
    def input(self):
        if not self.attack:
            keys = pygame.key.get_pressed()
            #Move Inputs
            if keys[pygame.K_w]: #up
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]: #down
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            
            if keys[pygame.K_a]: #left
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]: #right
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0
            
            #Attack Inputs
            if keys[pygame.K_LSHIFT] and not self.attack:
                self.attack = True
                self.attack_time = pygame.time.get_ticks()
                print('Attack')
                


            #Magic Inputs
            if keys[pygame.K_LCTRL] and not self.attack:
                self.attack = True
                self.attack_time = pygame.time.get_ticks()
                print('Magic')

    def status_get(self):

        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not '_idle' in self.status and not '_attack' in self.status:

                self.status = self.status + '_idle'

        if self.attack:
            self.direction.x = 0
            self.direction.y = 0
            if not '_attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if '_attack' in self.status:
                self.status = self.status.replace('_attack','')
    
    def cooldowns(self):
        currently = pygame.time.get_ticks()

        if self.attack:
            if currently - self.attack_time >= self.attack_cooldown:
                self.attack = False

    def animate(self):
        animations = self.animations[self.status]

        #looping over fram indeces
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animations):
            self.frame_index = 0
        
        #setting image
        self.image = animations[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.status_get()
        self.animate()
        self.move(self.speed)