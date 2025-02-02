import pygame
import math
import random

def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

pygame.init()
#......................................................................

#Screen
W = 800
H = 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space Invaders: The Game")
pygame.display.set_icon(pygame.image.load('Game-Dev-1/images/gameicon.png'))
#......................................................................

#Player
playerImg = pygame.image.load('Game-Dev-1/images/spaceship.png')
playerX = W/2 - 32
playerY = 4*H/5
pX_change = 0
pY_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))
#......................................................................

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
#...........................................................................

#Enemy
class Enemy:
    def __init__(self, image, x, y, eX_change, eY_change):
        self.image = image
        self.x = x
        self.y = y
        self.eX_change = eX_change
        self.eY_change = eY_change

    def move(self):
        self.x += self.eX_change
        self.y += self.eY_change

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

enemy_images = [
    pygame.image.load('Game-Dev-1/enemy images/enemy.png'),
    pygame.image.load('Game-Dev-1/enemy images/ghost.png'),
    pygame.image.load('Game-Dev-1/enemy images/ghostx.png'),
    pygame.image.load('Game-Dev-1/enemy images/ufo.png'),
]

enemies = []

def spawn_enemy():
    img = random.choice(enemy_images)

    x = random.randint(0, W)
    y = random.randint(-50, 100)

    eX_change = random.choice([-0.2, 0.2])
    eY_change = random.choice([0.1, 0.2])

    enemy = Enemy(img, x, y, eX_change, eY_change)
    enemies.append(enemy)

#Timer for spawning enemies
spawn_timer = 0
spawn_interval = 1500
#..........................................................................


#Score
score = 0


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
            
        #Player Movement.................................................    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pX_change = -0.5
        elif keys[pygame.K_RIGHT]:
            pX_change = 0.5
        elif keys[pygame.K_UP]:
            pY_change = -0.5
        elif keys[pygame.K_DOWN]:
            pY_change = 0.5
        else:
            pX_change = 0
            pY_change = 0
        #..................................................................    

    #player boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= W - 64:
        playerX = W - 64

    if playerY <= (2*H/3)-100:
        playerY = (2*H/3)-100
    elif playerY >= H - 64:
        playerY = H - 64
    #.....................................................................

    #changes/updates/frames
    draw_belt()

    #Enemy Spawning with Timer
    if pygame.time.get_ticks() - spawn_timer > spawn_interval:
        spawn_enemy()
        spawn_timer = pygame.time.get_ticks()
    
    for enemy in enemies:
        enemy.move()
        enemy.draw()
    #Boundary for enemies
    for enemy in enemies:
        if enemy.x <= 0:
            enemy.eX_change = random.choice([0.5, 1.0])
        elif enemy.x >= W - 64:
            enemy.eX_change = random.choice([-0.5, -1.0])

    playerX += pX_change
    playerY += pY_change
    player(playerX, playerY)

    pygame.display.update()

# Quit the game: Outside the event loop
# If pygame.quit() is inside the loop, 
# it will execute as soon as the loop condition is met (when running = False). 
# However, at that point: The Pygame window will close immediately, preventing
# any remaining events or updates from completing cleanly. This can cause 
# unnecessary delays or issues when you're wrapping up the game.
pygame.quit()