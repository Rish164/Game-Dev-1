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
#........................................................................


#Player
playerImg = pygame.image.load('Game-Dev-1/images/spaceship.png')
playerX = W/2 - 32
playerY = 4*H/5
p_vector = 0.8
#
def player(x, y):
    screen.blit(playerImg, (x, y))
#........................................................................


#End_line/Asteroid Belt
rockImg = pygame.image.load('Game-Dev-1/images/stone.png')
rWidth, rHeight = 24, 24
beltY = playerY + 32
#
num_of_rocks = W//rWidth
remaining_space = W - (num_of_rocks*rWidth)
extra_space_per_stone = remaining_space//(num_of_rocks - 1) if num_of_rocks > 1 else 0
#
def draw_belt():
    for i in range(num_of_rocks):
        x_posi = i * (rWidth + extra_space_per_stone) 
        screen.blit(rockImg, (x_posi, beltY))
#........................................................................


#Bullet
bulletImg = pygame.image.load('Game-Dev-1/images/bullet.png')
b_speed = 3
b_x = 0
b_y = playerY
state = "ready"
#
def fire(x, y):
    screen.blit(bulletImg, (x+16, y))
#........................................................................


#Now we will start the Event/Game loop
running = True
#Main/GameLoop / for continuous updation of events like movement collision etc.
while running:

    screen.fill((0, 0, 0))
    #.....................................................................


    #Eventloop / for specific event that happen once a frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            #sys.exit(): Removing this now, because this instantly kills the program
            #and we want to close the window first and then kill the program
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and state == "ready":
                state = "fire"
                b_x = playerX
                b_y = playerY       
    #....................................................................


    #Player Movement   
    keys = pygame.key.get_pressed()
    playerX += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * p_vector
    playerY += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * p_vector
    #    
    #player boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= W - 64:
        playerX = W - 64
    #
    if playerY <= (2*H/3)-100:
        playerY = (2*H/3)-100
    elif playerY >= H - 64:
        playerY = H - 64
    #.....................................................................


    #bullet mechanics
    if b_y <= 0:  # Reset bullet when it goes off-screen
        state = "ready"
        b_y = playerY
    if state == "fire":  # Fix: Use == instead of is (my comment)
        fire(b_x, b_y)
        b_y -= b_speed
    #.....................................................................


    #changes/updates/frames
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