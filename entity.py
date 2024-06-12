import pygame

class Entity(pygame.sprite.Sprite):
    def __init__ (self,groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.10
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #when moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #when moving left
                        self.hitbox.left = sprite.rect.right
                    
        if direction == 'vertical':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  #when moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #when moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def dealing_dmg(self, other_entity):
        other_entity.taking_dmg(self.damage)