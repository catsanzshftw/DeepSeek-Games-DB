import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the window
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Breakout Game")

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Paddle and ball properties
paddle_width = 80
paddle_height = 10
paddle_x = width // 2 - paddle_width // 2
paddle_y = height - paddle_height * 3

ball_radius = 10
ball_x = width // 2
ball_y = height // 2
ball_speed_x = 5
ball_speed_y = 5

# Game objects (bricks)
brick_width = 75
brick_height = 20
brick_offset = 30
number_of_bricks = 5
bricks = []
for i in range(number_of_bricks):
    bricks.append(pygame.Rect(brick_offset + i * brick_width, brick_offset, brick_width, brick_height))

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Clear screen
    screen.fill(BLACK)

    # Draw bricks (for testing)
    for brick in bricks:
        pygame.draw.rect(screen, BLUE, brick)

    # Draw paddle
    pygame.draw.rect(screen, WHITE, pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height))

    # Draw ball
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)

    # Update game objects
    # Move paddle
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        paddle_x -= 5
    if key[pygame.K_RIGHT]:
        paddle_x += 5

    # Keep paddle within bounds
    paddle_x = max(0, min(paddle_x, width - paddle_width))

    # Move ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with walls
    if ball_x <= ball_radius or ball_x >= width - ball_radius:
        ball_speed_x *= -1
    if ball_y <= ball_radius or ball_y >= height - ball_radius:
        ball_speed_y *= -1

    # Ball collision with paddle
    if (ball_x > paddle_x and ball_x < paddle_x + paddle_width) and (ball_y > paddle_y - ball_radius):
        ball_speed_y *= -1

    # Check for brick collisions (for testing)
    for brick in bricks:
        if pygame.Rect.colliderect(brick, pygame.Rect(ball_x, ball_y, 2*ball_radius, 2*ball_radius)):
            bricks.remove(brick)

    # Update screen
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

    # Check for exit
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

pygame.quit()
