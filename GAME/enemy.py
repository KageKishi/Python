import pygame
import attack
from attack import Attack
from destructibleentity import DestructibleEntity

class Enemy(DestructibleEntity , Attack):
    def _init_(self , enemy , hitbox , image , hp , damage):
        self.hitpoint = hp
        self.enemyhitbox = enemy
        self.damage = damage
        self.hitbox = hitbox
        self.image = image
        self.rect = pygame.rect(enemy)
        Attack._init_(self.hitbox , self.damage)
        DestructibleEntity(self.hitpoint)
    def draw(self , screen):
        screen.bilt(self.image , screen)
