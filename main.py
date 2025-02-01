import pygame
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
            running = False
            #sys.exit(): Removing this now, because this instantly kills the program
            #and we want to close the window first and then kill the program

    pygame.display.update()

# Quit the game: Outside the event loop
# If pygame.quit() is inside the loop, 
# it will execute as soon as the loop condition is met (when running = False). 
# However, at that point: The Pygame window will close immediately, preventing
# any remaining events or updates from completing cleanly. This can cause 
# unnecessary delays or issues when you're wrapping up the game.
pygame.quit()