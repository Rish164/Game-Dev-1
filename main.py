import pygame
import math
import random


#Distance formula
def distance(x1, x2, y1, y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

#Enemy Data
enemy_img = [
    pygame.image.load('enemy images/enemy.png'),
    pygame.image.load('enemy images/ghost.png'),
    pygame.image.load('enemy images/ghostx.png'),
    pygame.image.load('enemy images/ufo.png')
]

score = 0

pygame.init()
#......................................................................


#Screen
W = 800
H = 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space Invaders: The Game")
pygame.display.set_icon(pygame.image.load('images/gameicon.png'))
#........................................................................


#Player
playerImg = pygame.image.load('images/spaceship.png')
playerX = W/2 - 32
playerY = 4*H/5
p_vector = 1
#
def player(x, y):
    screen.blit(playerImg, (x, y))
#........................................................................


#End_line/Asteroid Belt
rockImg = pygame.image.load('images/stone.png')
rWidth, rHeight = 24, 24
beltY = 4*H/5 + 32
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
bulletImg = pygame.image.load('images/bullet.png')
b_speed = 3.5
b_x = -500
b_y = -500
state = "ready"
#
def fire(x, y):
    screen.blit(bulletImg, (x+16, y))
#........................................................................


#Enemy
class Enemy:
    def __init__(self, image, x, y, x_vector, y_vector):
        self.image = image
        self.x = x
        self.y = y
        self.x_vector = x_vector
        self.y_vector = y_vector
        self.crossed = False
    #
    def move(self):
        self.x += self.x_vector
        self.y += self.y_vector
        if self.x<=0 or self.x>=W-64:
            self.x_vector = -self.x_vector #Reversing Horizontal direction for boundaries
    #
        if self.y>=beltY and not self.crossed:
            global score
            score -= 1
            self.crossed = True
            print(score)
    #    
    def draw_enemy(self):
        screen.blit(self.image, (self.x, self.y))

enemies = []

def spawn_enemy():
    image = random.choice(enemy_img)
    x = random.choice([0, W-64])
    y = random.choice([-50, 50])
    x_vector = random.choice([-0.6, 0.6])
    y_vector = random.choice([0.1, 0.5])

    enemy = Enemy(image, x, y, x_vector, y_vector)
    enemies.append(enemy)
#
#Spawn Time
last_spawn_time = pygame.time.get_ticks()
spawn_interval = 650
#........................................................................


#collision/bullet/enemy
def isCollisionbullet():
    if distance(b_x, enemy.x, b_y, enemy.y) < 32:
        return True
    return False
#........................................................................


#collision/enemy/asteroidbelt
#within enemy.move()
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
    
    
    #Asteroid belt
    draw_belt() 
    #
    
    #....................................................................


    #Enemy Spawn and movement
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time >= spawn_interval:
        spawn_enemy()
        last_spawn_time = current_time
    #
    for enemy in enemies:
        enemy.move()
        enemy.draw_enemy()
    #....................................................................


    #Player Movement/boundaries   
    keys = pygame.key.get_pressed()
    playerX += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * p_vector
    playerY += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * p_vector
    #    
    #boundaries
    if playerX <= -24:
        playerX = -24
    elif playerX >= W - 40:
        playerX = W - 40
    #
    if playerY <= (2*H/3)-100:
        playerY = (2*H/3)-100
    elif playerY >= H - 64:
        playerY = H - 64
    #.....................................................................
    
    
    #bullet mechanics
    if b_y <= 0:  # Reset bullet when it goes off-screen
        state = "ready"
        b_y = -500
    if state == "fire":  # Fix: Use == instead of is (my comment)
        fire(b_x, b_y)
        b_y -= b_speed
    #Kill
    for enemy in enemies:
        if isCollisionbullet():
            state = "ready"
            b_y = playerY
            score += 1
            print(score)
            enemy.x = random.choice([0, W])
            enemy.y = random.choice([-50, 100])
    #.....................................................................


    #changes/updates/frames       
    player(playerX, playerY)
    pygame.display.update()

# Quit the game: Outside the event loop
# If pygame.quit() is inside the loop, 
# it will execute as soon as the loop condition is met (when running = False). 
# However, at that point: The Pygame window will close immediately, preventing
# any remaining events or updates from completing cleanly. This can cause 
# unnecessary delays or issues when you're wrapping up the game.
pygame.quit()