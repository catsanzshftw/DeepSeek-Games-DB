import pygame
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Set up window size and title
window = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Pong Game")

# Game constants
width = 600
height = 400
paddle_size = 100
ball_speed = 5
paddle_speed = 5

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

class Ball:
    def __init__(self):
        self.x = width/2 - 14
        self.y = height/2 - 14
        self.speed_x = ball_speed
        self.speed_y = ball_speed
        self.size = 30

    def update(self, paddle_left, paddle_right):
        # Ball movement
        self.x += self.speed_x
        self.y += self.speed_y

        # Collision with paddles
        if (self.x + self.size > paddle_right.x and 
            self.y > paddle_right.y and 
            self.y < paddle_right.y + paddle_size):
            self.speed_x = -self.speed_x
            
        if (self.x - self.size < paddle_left.x + paddle_size and 
            self.y > paddle_left.y and 
            self.y < paddle_left.y + paddle_size):
            self.speed_x = -self.speed_x

        # Collision with top and bottom
        if self.y + self.size > height:
            self.speed_y = -self.speed_y
        elif self.y - self.size < 0:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        pygame.draw.circle(screen, white, (int(self.x), int(self.y)), self.size)

class Paddle:
    def __init__(self, is_left=True):
        if is_left:
            self.x = 0
        else:
            self.x = width - paddle_size
        self.y = height/2 - paddle_size/2
        self.speed = paddle_speed

    def update(self, keys, is_left=True):
        if is_left:
            if keys[pygame.K_w]:
                self.y -= self.speed
            elif keys[pygame.K_s]:
                self.y += self.speed
        else:
            if keys[pygame.K_UP]:
                self.y -= self.speed
            elif keys[pygame.K_DOWN]:
                self.y += self.speed

        # Keep paddle within screen bounds
        if self.y < 0:
            self.y = 0
        elif self.y > height - paddle_size:
            self.y = height - paddle_size

    def draw(self, screen):
        pygame.draw.rect(screen, white, (self.x, self.y, paddle_size, paddle_size))

# Game loop
running = True
ball = Ball()
paddle_left = Paddle(is_left=True)
paddle_right = Paddle(is_left=False)

while running:
    # Handle user input
    keys = pygame.key.get_pressed()
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game objects
    ball.update(paddle_left, paddle_right)
    paddle_left.update(keys, is_left=True)
    paddle_right.update(keys, is_left=False)

    # Draw everything
    window.fill(black)
    ball.draw(window)
    paddle_left.draw(window)
    paddle_right.draw(window)

    # Check if ball goes past paddles
    if ball.x > width:
        print("Game Over! Right player lost.")
        running = False
    elif ball.x < 0:
        print("Game Over! Left player lost.")
        running = False

    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
