import pygame

class Attack:
    def __init__(self, atk=None, damage=0):
        self.atk = atk
        self.damage = damage
    def damageATK(self , target):
        if self.atk.rect.colliderect(target.rect):
            target.hp -= self.damage
            return target.hp

