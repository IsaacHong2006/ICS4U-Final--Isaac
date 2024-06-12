import pygame
from settings import *
from entity import Entity
from supporting import *

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups,obstacles_sprites):
        
        #inheretance for setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        #graphic set ups
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        #moving
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacles_sprites = obstacles_sprites

        #stats
        self.monster_name = monster_name
        thingymabobs_data = thingymabobs[self.monster_name]
        self.health = thingymabobs_data['health']
        self.exp = thingymabobs_data['exp']
        self.speed = thingymabobs_data['speed']
        self.attack_damage = thingymabobs_data['damage']
        self.resistance = thingymabobs_data['resistance']
        self.attack_radius = thingymabobs_data['attack_radius']
        self.notice_radius = thingymabobs_data['notice_radius']

        #interacting with the player
        self.can_attack = True
        self.attacking_time = 0
        self.cooldown_attack = 1000

    def import_graphics(self,name):
        self.animations = {'idle': [],
                           'move': [],
                           'attack': []}
        main_ = f'graphics/mobs/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_ + animation)

    def get_player_distance_with_direction(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)

        distance = (player_vector - enemy_vector).magnitude() #vector math and making it into distance

        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_with_direction(player)[0]
        
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'

        elif distance <= self.notice_radius:
            self.status = 'move'

        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attacking_time = pygame.time.get_ticks()
            print('attacking')

        elif self.status == 'move':
            self.direction = self.get_player_distance_with_direction(player)[1]


        else:
            self.direction = pygame.math.Vector2()
    
    def animating(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation): 
            if self.status == 'attack':
                self.can_attack = False

            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def cooldown_time(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attacking_time >= self.cooldown_attack:
                self.can_attack = True

    def attack(self, targ): 
        if pygame.sprite.collide_rect(self, targ):
            self.dealing_dmg(targ)

    def update(self):
        self.move(self.speed) 
        self.animating()
        self.cooldown_time()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
