import pygame
import mapBuilder
from mapBuilder import *

class Player:
    def __init__(self, x, y, w, h):
        self.player = pygame.Rect(x, y, w, h)
        self.color = 'Blue'
        self.speed = 5
        self.gravity = 0.5
        self.jump_count = 2
        self.on_ground = False

    def move(self, Frames):
        dx = 0
        dy = 0
        dv = 0
        self.gravity += 0.3
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            dv += 5
        if keys[pygame.K_d]:
            dx += self.speed + dv
        if keys[pygame.K_a]:
            dx -= self.speed + dv
        if keys[pygame.K_s]:
            self.gravity = min(self.gravity + 1, 15)
        
        self.player.x += dx
        
        for wall in mapBuilder.walls:
            if self.player.colliderect(wall.new_wall):
                if dx > 0:
                    self.player.right = wall.new_wall.left
                elif dx < 0:
                    self.player.left = wall.new_wall.right
            
        for door in mapBuilder.doors:
            if self.player.colliderect(door[0].new_door):
                mapBuilder.walls, mapBuilder.doors = mapBuilder.load_map(door[1])
                self.player.x, self.player.y = door[2]
                break

        for frame in Frames:
            if self.player.colliderect(frame):
                if dx > 0:
                    self.player.right = frame.left
                elif dx < 0:
                    self.player.left = frame.right
                    
        self.player.y += self.gravity    
               
        for frame in Frames:
            if self.player.colliderect(frame):
                if self.gravity > 0:
                    self.player.bottom = frame.top
                    self.gravity = 0
                    self.on_ground = True
                    self.jump_count = 2
                elif self.gravity < 0:
                    self.player.top = frame.bottom
                    self.gravity = 0
                    
        for wall in mapBuilder.walls:
            if self.player.colliderect(wall.new_wall):
                if self.gravity > 0:
                    self.player.bottom = wall.new_wall.top
                    self.gravity = 0
                    self.on_ground = True
                    self.jump_count = 2
                elif self.gravity < 0:
                    self.player.top = wall.new_wall.bottom
                    self.gravity = 0

    def getJump(self, isJump):
        if isJump and self.jump_count > 0:
            self.gravity = -10
            self.jump_count -= 1
            self.on_ground = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.player)