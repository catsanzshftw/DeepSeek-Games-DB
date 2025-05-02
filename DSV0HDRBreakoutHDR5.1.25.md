import pygame
import random

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
Colors = [RED, GREEN, BLUE, (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Set up the game window dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Breakout Game")

# Set up the clock for a decent frame rate
clock = pygame.time.Clock()

# Paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        
    def move_left(self, pixels):
        self.rect.x -= pixels
        if self.rect.x < 0:
            self.rect.x = 0
    
    def move_right(self, pixels):
        self.rect.x += pixels
        if self.rect.x > width - self.rect.width:
            self.rect.x = width - self.rect.width

# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.velocity = [random.choice([-5, 5]), -5]
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        
    def bounce(self):
        self.velocity[0] = self.velocity[0]
        self.velocity[1] = -self.velocity[1]

# Brick class
class Brick(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        
# Initializing sprites
paddle = Paddle(WHITE, 100, 10)
paddle.rect.x = 350
paddle.rect.y = 560

ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(paddle)
all_sprites_list.add(ball)

all_bricks = pygame.sprite.Group()
for i in range(7):
    for j in range(5):
        brick = Brick(random.choice(Colors), 80, 30)

        brick.rect.x = 60 + i * 100
        brick.rect.y = 60 + j * 60
        all_sprites_list.add(brick)
        all_bricks.add(brick)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move_left(5)
    if keys[pygame.K_RIGHT]:
        paddle.move_right(5)
    
    # Game logic
    all_sprites_list.update()
    
    # Check ball collision with walls
    if ball.rect.x >= 790:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y > 590:
        ball.font = pygame.font.Font(None, 74)
        text = ball.font.render("GAME OVER", True, WHITE)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False
    if ball.rect.y < 40:
        ball.velocity[1] = -ball.velocity[1]
    
    # Check ball collision with paddle
    if pygame.sprite.collide_mask(ball, paddle):
        ball.rect.x += ball.velocity[0]
        ball.rect.y -= ball.velocity[1]
        ball.bounce()
    
    # Check ball collision with bricks
    brick_collision_list = pygame.sprite.spritecollide(ball, all_bricks, False)
    for brick in brick_collision_list:
        ball.bounce()
        all_bricks.remove(brick)
        all_sprites_list.remove(brick)
    
    # Drawing everything on the screen
    screen.fill(BLACK)
    all_sprites_list.draw(screen)
    
    # Update the display
    pygame.display.flip()
    
    # Limit the frame rate to 60 FPS
    clock.tick(60)

pygame.quit()
