import pygame

class Attack:
    def __init__(self, hitbox , damage):
        self.atk = hitbox
        self.damage = damage
    def damageATK(self , target):
        if self.atk.rect.colliderect(target.rect):
            target.hp -= self.damage
            return target.hp

