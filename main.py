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

#Player
playerImg = pygame.image.load('Game-Dev-1/images/spaceship.png')
playerX = W/2 - 32
playerY = 4*H/5

def player(x, y):
    screen.blit(playerImg, (x, y))

#End_line/Asteroid Belt
rockImg = pygame.image.load('Game-Dev-1/images/stone.png')
rWidth = 24
rHeight = 24
beltY = playerY + 32
#..........................................................................
num_of_rocks = W//rWidth
remaining_space = W - (num_of_rocks*rWidth)
extra_space_per_stone = remaining_space//(num_of_rocks - 1) if num_of_rocks > 1 else 0

def draw_belt():
    for i in range(num_of_rocks):
        x_posi = i * (rWidth + extra_space_per_stone) 
        screen.blit(rockImg, (x_posi, beltY))


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
            
    draw_belt()        
    player(playerX, playerY)
    pygame.display.update()

# Quit the game: Outside the event loop
# If pygame.quit() is inside the loop, 
# it will execute as soon as the loop condition is met (when running = False). 
# However, at that point: The Pygame window will close immediately, preventing
# any remaining events or updates from completing cleanly. This can cause 
# unnecessary delays or issues when you're wrapping up the game.
pygame.quit()