import pygame
import math
import random
import sys

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paper Koopa Engine")

# Colors
BACKGROUND = (41, 129, 194)
GROUND_COLOR = (120, 78, 58)
GREEN = (65, 152, 57)
RED = (217, 65, 65)
YELLOW = (245, 203, 66)
BLUE = (66, 135, 245)
BROWN = (139, 69, 19)
LIGHT_BROWN = (160, 120, 80)
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
KOOPA_GREEN = (85, 180, 70)
KOOPA_SHELL = (180, 210, 80)
KOOPA_DARK = (60, 130, 50)

class Koopa:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 60
        self.speed = 2
        self.direction = 1  # 1 for right, -1 for left
        self.animation_offset = 0
        self.walking = True
        self.flip_timer = 0
        
    def update(self):
        # Animate walking motion
        self.animation_offset = math.sin(pygame.time.get_ticks() * 0.01) * 3
        
        # Move Koopa
        if self.walking:
            self.x += self.speed * self.direction
            
            # Turn around at edges
            if self.x < 50 or self.x > WIDTH - 100:
                self.direction *= -1
                self.flip_timer = 30
                self.walking = False
        else:
            self.flip_timer -= 1
            if self.flip_timer <= 0:
                self.walking = True
    
    def draw(self, surface):
        # Draw Koopa body
        body_height = 40
        
        # Draw shell
        pygame.draw.ellipse(surface, KOOPA_SHELL, (self.x - 25, self.y - body_height, self.width, body_height))
        pygame.draw.ellipse(surface, BLACK, (self.x - 25, self.y - body_height, self.width, body_height), 2)
        
        # Draw shell pattern
        for i in range(3):
            pygame.draw.ellipse(surface, (140, 170, 60), 
                                (self.x - 15 + i*15, self.y - body_height + 10, 10, 20))
        
        # Draw head
        head_x = self.x
        head_y = self.y - body_height - 5 + self.animation_offset
        
        if self.direction == -1:  # Facing left
            pygame.draw.ellipse(surface, KOOPA_GREEN, (head_x - 15, head_y, 30, 20))
            pygame.draw.ellipse(surface, BLACK, (head_x - 15, head_y, 30, 20), 2)
            
            # Draw eyes
            pygame.draw.circle(surface, WHITE, (head_x - 8, head_y + 8), 6)
            pygame.draw.circle(surface, BLACK, (head_x - 8, head_y + 8), 3)
        else:  # Facing right
            pygame.draw.ellipse(surface, KOOPA_GREEN, (head_x - 15, head_y, 30, 20))
            pygame.draw.ellipse(surface, BLACK, (head_x - 15, head_y, 30, 20), 2)
            
            # Draw eyes
            pygame.draw.circle(surface, WHITE, (head_x + 8, head_y + 8), 6)
            pygame.draw.circle(surface, BLACK, (head_x + 8, head_y + 8), 3)
        
        # Draw feet
        foot_y = self.y
        for i in range(2):
            offset = math.sin(pygame.time.get_ticks() * 0.01 + i) * 3
            pygame.draw.ellipse(surface, KOOPA_DARK, (self.x - 20 + i*25, foot_y + offset, 10, 8))

class Cloud:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = random.randint(30, 60)
        
    def update(self):
        self.x += self.speed
        if self.x > WIDTH + 100:
            self.x = -100
            self.y = random.randint(20, 150)
            self.size = random.randint(30, 60)
            
    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (self.x, self.y), self.size)
        pygame.draw.circle(surface, WHITE, (self.x - self.size//2, self.y), self.size - 10)
        pygame.draw.circle(surface, WHITE, (self.x + self.size//2, self.y), self.size - 10)
        pygame.draw.circle(surface, WHITE, (self.x, self.y - self.size//3), self.size - 15)

class QuestionBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 35
        self.hit = False
        self.bounce_offset = 0
        self.bounce_direction = 1
        self.coin_timer = 0
        
    def update(self):
        # Bounce animation
        if self.hit:
            self.bounce_offset += 0.5 * self.bounce_direction
            if self.bounce_offset > 5:
                self.bounce_direction = -1
            if self.bounce_offset < 0:
                self.bounce_direction = 1
                self.bounce_offset = 0
                
            self.coin_timer += 1
            if self.coin_timer > 60:
                self.hit = False
                self.coin_timer = 0
        
    def draw(self, surface):
        # Draw block
        block_y = self.y - self.bounce_offset
        pygame.draw.rect(surface, YELLOW, (self.x, block_y, self.size, self.size))
        pygame.draw.rect(surface, BLACK, (self.x, block_y, self.size, self.size), 2)
        
        # Draw question mark
        font = pygame.font.SysFont(None, 30)
        text = font.render("?", True, BLACK)
        surface.blit(text, (self.x + self.size//2 - text.get_width()//2, 
                           block_y + self.size//2 - text.get_height()//2))
        
        # Draw coin when hit
        if self.hit and self.coin_timer < 30:
            coin_y = block_y - 30 - self.coin_timer
            pygame.draw.circle(surface, YELLOW, (self.x + self.size//2, coin_y), 10)
            pygame.draw.circle(surface, (200, 170, 0), (self.x + self.size//2, coin_y), 10, 2)
            pygame.draw.circle(surface, (180, 150, 0), (self.x + self.size//2, coin_y), 6)

class Platform:
    def __init__(self, x, y, width, height, color=LIGHT_BROWN):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, BROWN, (self.x, self.y, self.width, self.height), 2)
        
        # Draw platform details
        for i in range(0, self.width, 10):
            pygame.draw.line(surface, BROWN, (self.x + i, self.y), (self.x + i, self.y + self.height), 1)

def draw_ground(surface):
    pygame.draw.rect(surface, GROUND_COLOR, (0, HEIGHT - 50, WIDTH, 50))
    
    # Draw grass on top
    pygame.draw.rect(surface, GREEN, (0, HEIGHT - 50, WIDTH, 10))
    
    # Draw ground details
    for i in range(0, WIDTH, 15):
        pygame.draw.line(surface, (100, 60, 40), (i, HEIGHT - 50), (i, HEIGHT), 1)

def draw_ui(surface, coins):
    # Draw score panel
    pygame.draw.rect(surface, (200, 50, 50, 180), (10, 10, 150, 40), border_radius=10)
    pygame.draw.rect(surface, BLACK, (10, 10, 150, 40), 2, border_radius=10)
    
    # Draw coin
    pygame.draw.circle(surface, YELLOW, (30, 30), 12)
    pygame.draw.circle(surface, (180, 150, 0), (30, 30), 12, 2)
    
    # Draw coin count
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"x {coins}", True, WHITE)
    surface.blit(text, (45, 20))
    
    # Draw title
    title_font = pygame.font.SysFont(None, 40, bold=True)
    title = title_font.render("PAPER KOOPA", True, YELLOW)
    surface.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    # Draw instructions
    inst_font = pygame.font.SysFont(None, 22)
    inst = inst_font.render("Press SPACE to hit blocks", True, WHITE)
    surface.blit(inst, (WIDTH//2 - inst.get_width()//2, HEIGHT - 30))

# Create game objects
koopa = Koopa(WIDTH//2, HEIGHT - 70)
clouds = [Cloud(random.randint(0, WIDTH), random.randint(20, 150), random.uniform(0.1, 0.3)) for _ in range(4)]
blocks = [
    QuestionBlock(150, HEIGHT - 150),
    QuestionBlock(250, HEIGHT - 200),
    QuestionBlock(400, HEIGHT - 150)
]
platforms = [
    Platform(100, HEIGHT - 150, 100, 20),
    Platform(250, HEIGHT - 200, 80, 20),
    Platform(380, HEIGHT - 150, 120, 20)
]

# Game variables
coins = 0
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Check if player hit any blocks
                mouse_pos = pygame.mouse.get_pos()
                for block in blocks:
                    if not block.hit and block.x <= mouse_pos[0] <= block.x + block.size and \
                       block.y <= mouse_pos[1] <= block.y + block.size:
                        block.hit = True
                        coins += 1
    
    # Update game objects
    koopa.update()
    for cloud in clouds:
        cloud.update()
    for block in blocks:
        block.update()
    
    # Draw everything
    screen.fill(BACKGROUND)
    
    # Draw clouds
    for cloud in clouds:
        cloud.draw(screen)
    
    # Draw ground
    draw_ground(screen)
    
    # Draw platforms
    for platform in platforms:
        platform.draw(screen)
    
    # Draw blocks
    for block in blocks:
        block.draw(screen)
    
    # Draw Koopa
    koopa.draw(screen)
    
    # Draw UI
    draw_ui(screen, coins)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
