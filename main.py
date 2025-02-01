import pygame
import sys
import math
import random

pygame.init()

#Screen
W = 800
H = 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space Invaders: The Game")
pygame.display.set_icon(pygame.image.load('Game-Dev-1/images/gameicon.png'))

#Now we will start the Event/Game loop
running = True
#EventLoop
while running:

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            sys.exit()

    pygame.display.update()