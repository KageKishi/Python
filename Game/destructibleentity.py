import pygame

class DestructibleEntity:
    def __init__(self , hp):
        self.hitpoint = hp
        self.isalive = True
    def TakeDamage(self, damage):
        self.hitpoint -= damage
        if not self.hitpoint >  0:
            self.isalive = False
    def isdead(self):
        return not self.isalive
