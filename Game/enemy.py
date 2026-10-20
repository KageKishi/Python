import pygame
import attack
from attack import Attack
from destructibleentity import DestructibleEntity

class Enemy(DestructibleEntity , Attack):
    def __init__(self, enemy, hitbox, image, hp, damage):
        self.hitpoint = hp
        self.enemyhitbox = enemy
        self.damage = damage
        self.hitbox = hitbox
        self.image = image
        self.rect = pygame.Rect(enemy)
        Attack.__init__(self, self.hitbox, self.damage)
        DestructibleEntity.__init__(self, self.hitpoint)
    def draw(self , screen):
        screen.blit(self.image , screen)
