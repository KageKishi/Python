import json
import pygame


class Block:
    def __init__(self, x, y, w, h):
        self.new_wall = pygame.Rect(x, y, w, h)
        self.new_door = pygame.Rect(x, y, w, h)
        self.W_color = 'White'
        self.D_color = 'Red'

    def W_draw(self, screen):
        pygame.draw.rect(screen, self.W_color, self.new_wall)

    def D_draw(self, screen):
        pygame.draw.rect(screen, self.D_color, self.new_door)
    def E_draw(self , screen):
        pygame.draw.rect(screen , self.D_color , self.new_wall)

def load_map(map_name):
    map_data = data[map_name]
    walls = [Block(*w) for w in map_data["Walls"]]
    doors = [(Block(*d["wall"]), d["leadsTo"], d["spawn"]) for d in map_data["Doors"]]
    enemies = [(Block(*e["Hitbox"]), e["Hp"], e["Damage"])for e in map_data["Enemies"]]
    return walls, doors , enemies

with open('maps.json', 'r') as file:
    data = json.load(file)
    
walls, doors , enemies = load_map("Map1")