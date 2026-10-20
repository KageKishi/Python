import pygame

class Attack:
    def __init__(self):
        self.atk
        self.damage
    def damageATK(self , target):
        if self.atk.rect.colliderect(target.rect):
            target.hp -= self.damage
            return target.hp

