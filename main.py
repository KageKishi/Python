import pygame
import mapBuilder
from mapBuilder import *
import player
from player import *

WIDTH, HEIGHT = 800 , 800
Frames = [
    pygame.Rect(0, 0, 5, HEIGHT - 5), 
    pygame.Rect(0, HEIGHT - 5, WIDTH - 5, 5), 
    pygame.Rect(WIDTH - 5, 0, 5, HEIGHT), 
    pygame.Rect(5, 0, WIDTH - 10, 5)
]

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
background = pygame.transform.smoothscale(pygame.image.load("assets/background.jpg").convert(), screen.get_size())
Player = player.Player(20, 20, 40, 50, asset_dir="assets")
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Player.getJump(True)
            if event.key == pygame.K_i:
                Player.Attack()
    
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    Player.move(Frames)
    for frame in Frames:
        pygame.draw.rect(screen, (255, 255, 255), frame)
    Player.draw(screen)
    
    for wall in mapBuilder.walls:
        wall.W_draw(screen)
    for door in mapBuilder.doors:
        door[0].D_draw(screen)
    for enemy in mapBuilder.enemies:
        enemy[0].E_draw(screen)
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()