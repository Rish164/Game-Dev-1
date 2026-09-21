# 🚀 Space Invaders

A Python-based **Space Invaders-style arcade game** built using **Pygame**.

The project was developed to explore the fundamentals of game development in Python, including real-time event handling, player movement, projectile mechanics, enemy spawning, collision detection, scoring, and game-loop architecture.

---

## 🎮 Game Overview

**Space Invaders** is a 2D arcade shooter where the player controls a spaceship and attempts to destroy incoming enemies before they cross the asteroid belt.

Enemies continuously spawn from the sides of the screen and move toward the player's area. The player can move around the lower portion of the screen and fire projectiles to destroy enemies.

The game currently features multiple enemy types, dynamic enemy spawning, projectile collision detection, boundary restrictions, and a score system.

---

## ✨ Features

* 🚀 Player-controlled spaceship
* 👾 Multiple enemy types
* 🔫 Projectile-based shooting
* 💥 Bullet–enemy collision detection
* 🏆 Real-time score tracking
* 🌌 Continuous enemy spawning
* ↔️ Horizontal enemy movement with boundary reversal
* ⬇️ Enemy vertical movement
* 🪨 Asteroid belt / danger boundary
* 📉 Score penalty when enemies cross the belt
* 🖥️ Real-time Pygame game loop
* 🎨 Custom game sprites and icon
* 🎲 Randomized enemy type, spawn position, and movement

---

## 🕹️ Controls

| Key                | Action     |
| ------------------ | ---------- |
| `←`                | Move left  |
| `→`                | Move right |
| `↑`                | Move up    |
| `↓`                | Move down  |
| `SPACE`            | Fire       |
| `X / Close Window` | Exit game  |

---

## 🧠 Game Mechanics

### Player Movement

The spaceship can be controlled using the arrow keys.

Movement is updated every frame using Pygame's keyboard state:

```python
keys = pygame.key.get_pressed()

playerX += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * p_vector
playerY += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * p_vector
```

The player's position is restricted using screen boundaries so the spaceship cannot move indefinitely outside the playable area.

---

### 🔫 Shooting System

The game uses a projectile state system:

```text
READY → FIRE → READY
```

When the player presses `SPACE`, a bullet is created at the spaceship's position.

The projectile continuously moves upward until it either:

1. Hits an enemy, or
2. Leaves the screen.

Once either event occurs, the bullet is reset and becomes available for firing again.

---

### 👾 Enemy System

Enemies are implemented using an `Enemy` class.

Each enemy stores:

* Sprite/image
* X position
* Y position
* Horizontal velocity
* Vertical velocity
* Whether it has crossed the asteroid belt

Example:

```python
class Enemy:
    def __init__(self, image, x, y, x_vector, y_vector):
        self.image = image
        self.x = x
        self.y = y
        self.x_vector = x_vector
        self.y_vector = y_vector
        self.crossed = False
```

This allows every enemy to maintain its own movement state.

---

### 🎲 Random Enemy Spawning

Enemy characteristics are randomized when an enemy is spawned.

The game randomly selects:

* Enemy type
* Starting side
* Starting vertical position
* Horizontal direction
* Vertical speed

This prevents every enemy from following exactly the same trajectory.

---

### 💥 Collision Detection

The project uses a distance-based collision calculation.

```python
def distance(x1, x2, y1, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)
```

A collision is detected when the distance between the bullet and enemy falls below a predefined threshold.

```python
if state == "fire" and distance(b_x, enemy.x, b_y, enemy.y) < 32:
    return True
```

When a collision occurs:

* The bullet is reset
* The player's score increases
* The enemy is repositioned

---

### 🪨 Asteroid Belt

An asteroid belt is positioned above the player's lower movement area.

If an enemy reaches the belt, the player's score is reduced.

```python
if self.y >= beltY and not self.crossed:
    score -= 1
    self.crossed = True
```

The `crossed` flag ensures that the same enemy does not repeatedly decrease the score every frame after crossing the belt.

---

## 📊 Scoring

The scoring system currently works as follows:

| Event                       | Score |
| --------------------------- | ----: |
| Destroy an enemy            |  `+1` |
| Enemy crosses asteroid belt |  `-1` |

The score is displayed in the top-left corner of the screen.

---

## 🏗️ Project Structure

```text
Space-Invaders/
│
├── images/
│   ├── spaceship.png
│   ├── bullet.png
│   ├── stone.png
│   └── gameicon.png
│
├── enemy images/
│   ├── enemy.png
│   ├── ghost.png
│   ├── ghostx.png
│   └── ufo.png
│
├── main.py
│
└── README.md
```

> Replace `main.py` with the actual filename if your Python file has a different name.

---

## 🛠️ Tech Stack

| Technology | Purpose                                 |
| ---------- | --------------------------------------- |
| **Python** | Core programming language               |
| **Pygame** | Game engine / graphics / input handling |
| **Math**   | Distance-based collision calculations   |
| **Random** | Randomized enemy generation             |

---

## ⚙️ Insta
