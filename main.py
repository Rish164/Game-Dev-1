import pygame
import math
import random

# Distance formula
def distance(x1, x2, y1, y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

# Enemy Data
enemy_img = [
    pygame.image.load('enemy images/enemy.png'),
    pygame.image.load('enemy images/ghost.png'),
    pygame.image.load('enemy images/ghostx.png'),
    pygame.image.load('enemy images/ufo.png')
]

score = 0

#Sonic Variables
sonic_ammo = 1
MAX_SONIC_AMMO = 5
KILL_REQUIREMENT = 15
kill_count = 0

#Activation Variables for Sonic Boom
sonic_boom_active = False
sonic_boom_start_time = 0
SONIC_BOOM_COOLDOWN = 30000 #30 seconds in milliseconds

sonic_boom_radius = 0 #initialize radius of the ring
SONIC_BOOM_EXPANSION_SPEED = 1 #Pixels per frame

pygame.init()
# ......................................................................

# Score display()
pygame.font.init()
font = pygame.font.Font(None, 32)

def draw_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))  # position: top-left
# .......................................................................

# Screen
W = 800
H = 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space Invaders: The Game")
pygame.display.set_icon(pygame.image.load('images/gameicon.png'))
# ........................................................................

# Player
playerImg = pygame.image.load('images/spaceship.png')
playerX = W/2 - 32
playerY = 4*H/5
normal_speed = 1
reduced_speed = 0.5  # Slower speed when firing
p_vector = normal_speed

def player(x, y):
    screen.blit(playerImg, (x, y))
# ........................................................................

#Health_Bar
health = 100
HEALTH_DECREASE_CROSS = 5
#..............................................................................

# End_line/Asteroid Belt
rockImg = pygame.image.load('images/stone.png')
rWidth, rHeight = 24, 24
beltY = 4*H/5 + 32

num_of_rocks = W//rWidth
remaining_space = W - (num_of_rocks*rWidth)
extra_space_per_stone = remaining_space//(num_of_rocks - 1) if num_of_rocks > 1 else 0

def draw_belt():
    for i in range(num_of_rocks):
        x_posi = i * (rWidth + extra_space_per_stone)
        screen.blit(rockImg, (x_posi, beltY))
# ........................................................................

# Bullet
bulletImg = pygame.image.load('images/bullet.png')
b_speed = 3.5
b_x = -500
b_y = -500
state = "ready"

def fire(x, y):
    screen.blit(bulletImg, (x+16, y))
# ........................................................................

# Enemy
class Enemy:
    def __init__(self, image, x, y, x_vector, y_vector):
        self.image = image
        self.x = x
        self.y = y
        self.x_vector = x_vector
        self.y_vector = y_vector
        self.crossed = False
    
    def move(self):
        self.x += self.x_vector
        self.y += self.y_vector
        
        if self.x <= 0 or self.x >= W-64:
            self.x_vector = -self.x_vector  # Reversing Horizontal direction for boundaries
    
        if self.y >= beltY and not self.crossed:
            global score, health
            score -= 1
            health -= HEALTH_DECREASE_CROSS #Reduce health when enemy crosses
            if health < 0:
                health = 0
            self.crossed = True
            # print(score)
    
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
# Spawn Time
last_spawn_time = pygame.time.get_ticks()
spawn_interval = 1000
# ........................................................................

# collision/bullet/enemy
def isCollisionbullet(enemy):
    return state == "fire" and distance(b_x, enemy.x, b_y, enemy.y) < 32

# collision/player/enemy
def isCollisionplayer(enemy):
    return distance(playerX, enemy.x, playerY, enemy.y) < 32
# ........................................................................

#Health_Bar_Display
def draw_health():
    health_bar_x = W-110
    health_bar_y = 25
    bar_width = 100
    bar_height = 15

    #Draw bar background
    pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, bar_width, bar_height))

    #Draw health fill bar
    fill_width = (health / 100) * bar_width
    pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, fill_width, bar_height))

    #Display health percentage
    health_text = font.render(f"{health}%", True, (255, 255, 255))
    screen.blit(health_text, (health_bar_x - 70, health_bar_y - 5))
#.........................................................................

#Sonic_Ammo funcs
def draw_sonic_ammo():
    text_x = 10
    text_y = 50  # Adjusted to leave space below the score
    ammo_x = text_x + 150  # Position bars after text
    ammo_y = text_y   # Align bars properly with text
    bar_width = 10
    bar_height = 25
    spacing = 5

    # Draw the text label
    text = font.render("Sonic Ammo:", True, (255, 255, 255))
    screen.blit(text, (text_x, text_y))

    # Draw the ammo bars in front of the text
    for i in range(sonic_ammo):
        pygame.draw.rect(screen, (255, 255, 255), (ammo_x + i * (bar_width + spacing), ammo_y, bar_width, bar_height))

# Now we will start the Event/Game loop
running = True
space_held = False  # New flag to track spacebar holding
while running:

    screen.fill((0, 0, 0))
    # .....................................................................

    # Event loop / for specific event that happen once a frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_held = True  # Set flag when spacebar is pressed
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                current_time = pygame.time.get_ticks()
                if sonic_ammo > 0 and not sonic_boom_active and current_time - sonic_boom_start_time >= SONIC_BOOM_COOLDOWN:
                    sonic_ammo -= 1  # Consume 1 Sonic Ammo
                    sonic_boom_active = True  # Activate Sonic Boom
                    sonic_boom_start_time = current_time  # Store activation time
                    sonic_boom_radius = 0  # Reset ring size when activated

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_held = False  # Reset flag when spacebar is released
    # ....................................................................
    
    # Adjust player speed based on firing state
    p_vector = reduced_speed if space_held else normal_speed
    
    # Asteroid belt
    draw_belt()
    #
    
    # ....................................................................

    # Enemy Spawn and movement
    current_time = pygame.time.get_ticks()
    if not sonic_boom_active and    current_time - last_spawn_time >= spawn_interval:
        spawn_enemy()
        last_spawn_time = current_time
    #
    for enemy in enemies:
        enemy.move()
        enemy.draw_enemy()
        if isCollisionplayer(enemy):
            health -= 10
            if health < 0:
                health = 0
            enemies.remove(enemy)
    # ....................................................................

    #Health restrictions
    if health > 100:
        health = 100

    # Player Movement/boundaries   
    if not sonic_boom_active or sonic_boom_radius >= H:
        keys = pygame.key.get_pressed()
        playerX += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * p_vector
        playerY += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * p_vector
    else:
        space_held = False #Prevent firing during Sonic Boom
        state = "ready" #Reset bullet state during Sonic Boom
    
    #
    # boundaries
    if playerX <= -24:
        playerX = -24
    elif playerX >= W - 40:
        playerX = W - 40
    #
    if playerY <= (2*H/3)-100:
        playerY = (2*H/3)-100
    elif playerY >= H - 64:
        playerY = H - 64
    # .....................................................................
    
    # bullet mechanics
    if b_y <= 0:
        state = "ready"
        b_y = -500
    if not sonic_boom_active: #Prevent firing during Sonic_Boom    
        if space_held and state == "ready":
            state = "fire"
            b_x = playerX
            b_y = playerY
        if state == "fire":
            fire(b_x, b_y)
            b_y -= b_speed
    else:
        state = "ready" #Ensure no bullets are active
        b_y = -500

    # Kill
    for enemy in enemies:
        if isCollisionbullet(enemy):
            state = "ready"
            b_y = -500
            score += 1
            health += 2
            
            kill_count += 1 #increment kill counter

            #Check if Sonic Ammo should be increased
            if kill_count >= KILL_REQUIREMENT:
                kill_count -= KILL_REQUIREMENT  # Reset counter by decrementing 15 kills for one bar
                if sonic_ammo < MAX_SONIC_AMMO:
                    sonic_ammo += 1  # Add 1 Sonic Ammo

            enemy.x = random.choice([0, W])
            enemy.y = random.choice([-50, 100])
    # .....................................................................

    # changes/updates/frames       
    player(playerX, playerY)

    draw_score()
    draw_health()
    draw_sonic_ammo()

    if sonic_boom_active:
        sonic_boom_radius += SONIC_BOOM_EXPANSION_SPEED  # Increase the ring size
        pygame.draw.circle(screen, (255, 255, 255), (int(playerX + 32), int(playerY + 32)), sonic_boom_radius, 5)

        #Check if enemies are inside the sonic boom radius
        for enemy in enemies[:]: #Iterating over a copy of the list
            if distance(enemy.x, playerX, enemy.y, playerY) <= sonic_boom_radius:
                score += 1 #Increase score for each enemy 
                health += 2 #Increase HP for each enemy killed
                enemies.remove(enemy) #Remove enemy

    # Stop Sonic Boom when it fully expands
    if sonic_boom_radius >= H:
        sonic_boom_active = False



    pygame.display.update()

pygame.quit()
