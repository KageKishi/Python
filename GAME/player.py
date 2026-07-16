import pygame
import mapBuilder
from mapBuilder import *
import screenanimation
from attack import Attack
from destructibleentity import DestructibleEntity

class Player(Attack , DestructibleEntity):
    def __init__(self, x, y, w, h, asset_dir="."):
        self.player = pygame.Rect(x, y, w, h)
        self.speed = 5
        self.gravity = 0.5
        self.hitpoint = 100
        self.damage = 7
        self.jump_count = 2
        self.on_ground = False
        self.animation_state = "idle"
        self.face_left = False
        self.firstAttack = True
        self.animation = screenanimation.ScreenAnimation(x, y, w, h, asset_dir=asset_dir , spritesheet="SpriteSheet.png" , spritesheet2="SpriteSheet2.png")
        self.damage = 7
        if self.face_left:
            self.weaponhitbox = pygame.Rect(x-5 , y , 20 , 20)
        else:
            self.weaponhitbox = pygame.Rect(x + 5 , y , 20 , 20)
        self.atk = self.weaponhitbox
        
    def Attack(self):
        if self.firstAttack:
            self.animation_state = "attack1"
            self.firstAttack = False
        else:
            self.animation_state = "attack2"
            self.firstAttack = True

    
    def move(self, Frames):
        dx = 0
        dv = 0
        was_on_ground = self.on_ground
        self.gravity += 0.3
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            dv += 5
        if keys[pygame.K_d]:
            dx += self.speed + dv
            self.face_left = False
        if keys[pygame.K_a]:
            dx -= self.speed + dv
            self.face_left = True
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
                self.gravity = 0
                self.on_ground = False
                self.jump_count = 2
                self.animation.sync(self.player)
                return

        for frame in Frames:
            if self.player.colliderect(frame):
                if dx > 0:
                    self.player.right = frame.left
                elif dx < 0:
                    self.player.left = frame.right

        self.on_ground = False
                    
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

        grounded = self.on_ground or was_on_ground

        if self.gravity < 0:
            self.animation_state = "jump"
        elif not grounded:
            self.animation_state = "fall"
        elif dx != 0:
            self.animation_state = "run"
        elif(self.animation_state != "attack1" and self.animation_state != "attack2"):
            self.animation_state = "idle"

        self.animation.set_state(self.animation_state)
        self.animation.set_facing_left(self.face_left)
        self.animation.sync(self.player)

    def getJump(self, isJump):
        if isJump and self.jump_count > 0:
            self.gravity = -10
            self.jump_count -= 1
            self.on_ground = False

    def draw(self, screen):
        self.animation.update(screen, self.player)
        if(self.animation.animations["attack1"] == self.animation._extract_frames_from_y("320")[3]):
            self.animation_state = "idle"
        if(self.animation.animations["attack2"] == self.animation._extract_frames_from_y("320")[6]):
            self.animation_state = "idle"