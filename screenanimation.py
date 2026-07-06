import json
import os

import pygame


class ScreenAnimation:
    def __init__(self, x, y, w, h, asset_dir=".", spritesheet="SpriteSheet.png" ,spritesheet2 = "SpriteSheet.png"):
        self.size = (w, h)
        self.player = pygame.Rect(x, y, w, h)
        self.frame_delay = 10
        self.frame_timer = 0
        self.frame_index = 0
        self.state = "idle"
        self.face_left = False
        self.animations = {}
        self.asset_dir = asset_dir
        self.spritesheet2 = self._load_spritesheet(spritesheet2)
        self.spritesheet = self._load_spritesheet(spritesheet)
        self.sprites = self._load_sprites_json("grouped_arrays.json")
        self.sprites2 = self._load_sprites_json("sprites.json")

        idle_frames = self._extract_frames_from_y(self.sprites.get("784")[:8])
        self.animations["idle"] = idle_frames if idle_frames else [self._load_fallback_frame()]
        self.animations["run"] = self._extract_frames_from_y(self.sprites.get("0")[:9]) or self.animations["idle"]
        self.animations["jump"] = self._extract_frames_from_y(self.sprites.get("504")[:4]) or self.animations["idle"][:1]
        self.animations["fall"] = self._extract_frames_from_y(self.sprites.get("504")[4:8]) or self.animations["idle"][:1]
        self.animations["attack1"] = self._extract_frames_from_y2(self.sprites2.get("320")[:3]) or self.animations["idle"]
        self.animations["attack2"] = self._extract_frames_from_y2(self.sprites2.get("320")[3:6]) or self.animations["idle"]
        #self.animations["hit"] = self._extract_frames_from_y(self.sprites.get("400")) or self.animations["idle"][:1]
        #self.animations["death"] = self._extract_frames_from_y(self.sprites.get("480")) or self.animations["idle"][:1]
        #self.animations["dodge"] = self._extract_frames_from_y(self.sprites.get("800")) or self.animations["idle"]

    def _load_spritesheet(self, filename):
        path = os.path.join(self.asset_dir, filename)
        if os.path.exists(path):
            return pygame.image.load(path).convert_alpha()
        raise FileNotFoundError(f"Spritesheet not found: {path}")

    def _load_sprites_json(self, filename):
        path = os.path.join(self.asset_dir, filename)
        if not os.path.exists(path):
            path = filename
        with open(path, "r") as f:
            return json.load(f)

    def _extract_frames_from_y(self, y):
        frames = []
        if isinstance(y, list):
            rects = y
        else:
            y_key = str(y)
            if y_key not in self.sprites:
                return frames
            rects = self.sprites[y_key]

        for rect in rects:
            x, sprite_y, w, h = rect
            cropped = self.spritesheet.subsurface(pygame.Rect(x, sprite_y, w, h))
            frames.append(pygame.transform.smoothscale(cropped.copy(), self.size))

        return frames
    
    def _extract_frames_from_y2(self, y):
        frames = []
        if isinstance(y, list):
            rects = y
        else:
            y_key = str(y)
            if y_key not in self.sprites2:
                return frames
            rects = self.sprites2[y_key]

        for rect in rects:
            x, sprite_y, w, h = rect
            cropped = self.spritesheet2.subsurface(pygame.Rect(x, sprite_y, w, h))
            frames.append(pygame.transform.smoothscale(cropped.copy(), self.size))

        return frames
    
    def _load_fallback_frame(self):
        image = self._extract_frames_from_y(self.sprites.get("960"))[0] if self._extract_frames_from_y(self.sprites.get("960")) else pygame.Surface(self.size, pygame.SRCALPHA)
        return pygame.transform.smoothscale(image, self.size)

    def set_state(self, state):
        if state not in self.animations:
            state = "idle"

        if self.state != state:
            self.state = state
            self.frame_index = 0
            self.frame_timer = 0

    def sync(self, rect):
        self.player.topleft = rect.topleft

    def set_facing_left(self, face_left):
        self.face_left = face_left

    def draw(self, screen):
        frames = self.animations[self.state]
        if not frames:
            return
        if len(frames) > 1:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0
                self.frame_index += 1
                if self.frame_index >= len(frames):
                    self.frame_index = 0

        frame = frames[self.frame_index]
        if self.face_left:
            frame = pygame.transform.flip(frame, True, False)

        screen.blit(frame, self.player)

    def update(self, screen, rect=None):
        if rect is not None:
            self.sync(rect)
        self.draw(screen)

    def idle_ani(self, screen):
        self.set_state("idle")
        self.draw(screen)
            