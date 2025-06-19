import pygame
import math
import random
import sys

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paper Koops Engine - Tech Demo")

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
BANDANA_BLUE = (70, 130, 230)
LIGHT_YELLOW = (255, 255, 200)
PURPLE = (150, 70, 200)
ORANGE = (245, 150, 66)

# Fonts
title_font = pygame.font.SysFont("Arial", 36, bold=True)
menu_font = pygame.font.SysFont("Arial", 28)
ui_font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)

class Koops:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 35
        self.height = 45
        self.speed = 4
        self.jump_power = 12
        self.velocity_y = 0
        self.gravity = 0.6
        self.direction = 1  # 1 for right, -1 for left
        self.animation_offset = 0
        self.bandana_flap = 0
        self.is_jumping = False
        self.is_grounded = False
        self.crouching = False
        self.hit_points = 3
        
    def update(self, platforms, ground_level):
        # Animate walking motion
        self.animation_offset = math.sin(pygame.time.get_ticks() * 0.01) * 3
        self.bandana_flap = math.sin(pygame.time.get_ticks() * 0.02) * 2
        
        # Apply gravity
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        
        # Check ground collision
        self.is_grounded = False
        if self.y >= ground_level - self.height:
            self.y = ground_level - self.height
            self.velocity_y = 0
            self.is_grounded = True
            self.is_jumping = False
            
        # Check platform collisions
        for platform in platforms:
            if (self.x + self.width > platform.x and 
                self.x < platform.x + platform.width and
                self.y + self.height > platform.y and
                self.y + self.height < platform.y + 20 and
                self.velocity_y > 0):
                self.y = platform.y - self.height
                self.velocity_y = 0
                self.is_grounded = True
                self.is_jumping = False
    
    def move(self, dx, platforms, ground_level):
        if self.crouching:
            return  # Can't move while crouching
            
        # Move horizontally
        self.x += dx * self.speed
        
        # Prevent going off screen left
        if self.x < 0:
            self.x = 0
            
        # Prevent going off screen right
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
            
        # Update direction
        if dx > 0:
            self.direction = 1
        elif dx < 0:
            self.direction = -1
            
        # Check platform collisions horizontally
        for platform in platforms:
            if (self.x + self.width > platform.x and 
                self.x < platform.x + platform.width and
                self.y + self.height > platform.y and
                self.y < platform.y + platform.height):
                # Push player back
                if dx > 0:  # Moving right
                    self.x = platform.x - self.width
                elif dx < 0:  # Moving left
                    self.x = platform.x + platform.width
    
    def jump(self):
        if self.is_grounded and not self.is_jumping:
            self.velocity_y = -self.jump_power
            self.is_jumping = True
            self.is_grounded = False
            
    def crouch(self, crouch):
        self.crouching = crouch
        if crouch:
            self.height = 30
        else:
            self.height = 45
    
    def draw(self, surface):
        # Draw Koops body
        body_height = 30
        
        # Draw shell (darker green for Koops)
        pygame.draw.ellipse(surface, (160, 190, 70), (self.x - 15, self.y - body_height + 10, self.width, body_height))
        pygame.draw.ellipse(surface, BLACK, (self.x - 15, self.y - body_height + 10, self.width, body_height), 2)
        
        # Draw shell pattern
        for i in range(3):
            pygame.draw.ellipse(surface, (140, 170, 60), 
                                (self.x - 5 + i*10, self.y - body_height + 20, 7, 15))
        
        # Draw head
        head_x = self.x
        head_y = self.y - body_height - 5 + self.animation_offset
        
        # Draw bandana
        bandana_points = [
            (head_x - 15, head_y - 5),
            (head_x - 10, head_y - 8 - self.bandana_flap),
            (head_x + 10, head_y - 8 - self.bandana_flap),
            (head_x + 15, head_y - 5)
        ]
        pygame.draw.polygon(surface, BANDANA_BLUE, bandana_points)
        pygame.draw.polygon(surface, BLACK, bandana_points, 2)
        
        # Draw head
        pygame.draw.ellipse(surface, KOOPA_GREEN, (head_x - 12, head_y, 24, 16))
        pygame.draw.ellipse(surface, BLACK, (head_x - 12, head_y, 24, 16), 2)
        
        # Draw eyes based on direction
        if self.direction == -1:  # Facing left
            pygame.draw.circle(surface, WHITE, (head_x - 6, head_y + 6), 5)
            pygame.draw.circle(surface, BLACK, (head_x - 6, head_y + 6), 2)
        else:  # Facing right
            pygame.draw.circle(surface, WHITE, (head_x + 6, head_y + 6), 5)
            pygame.draw.circle(surface, BLACK, (head_x + 6, head_y + 6), 2)
        
        # Draw feet
        foot_y = self.y
        for i in range(2):
            offset = math.sin(pygame.time.get_ticks() * 0.01 + i) * 3
            pygame.draw.ellipse(surface, KOOPA_DARK, (self.x - 15 + i*20, foot_y + offset, 8, 6))
            
        # Draw crouching effect
        if self.crouching:
            pygame.draw.rect(surface, (0, 0, 0, 100), (self.x - 20, self.y - 5, self.width + 10, 5))
            
        # Draw hit points
        for i in range(self.hit_points):
            pygame.draw.circle(surface, RED, (self.x + i*10, self.y - 40), 4)

class Platform:
    def __init__(self, x, y, width, height, color=LIGHT_BROWN, is_spike=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.is_spike = is_spike
        
    def draw(self, surface):
        if self.is_spike:
            # Draw spike platform
            pygame.draw.rect(surface, (100, 100, 100), (self.x, self.y, self.width, self.height))
            pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 2)
            
            # Draw spikes
            for i in range(0, self.width, 15):
                spike_points = [
                    (self.x + i, self.y),
                    (self.x + i + 7, self.y - 10),
                    (self.x + i + 14, self.y)
                ]
                pygame.draw.polygon(surface, (80, 80, 80), spike_points)
                pygame.draw.polygon(surface, BLACK, spike_points, 1)
        else:
            # Draw normal platform
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(surface, BROWN, (self.x, self.y, self.width, self.height), 2)
            
            # Draw platform details
            for i in range(0, self.width, 10):
                pygame.draw.line(surface, BROWN, (self.x + i, self.y), (self.x + i, self.y + self.height), 1)

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.animation_offset = 0
        self.rotation = 0
        
    def update(self):
        self.animation_offset = math.sin(pygame.time.get_ticks() * 0.03) * 3
        self.rotation = pygame.time.get_ticks() % 360
        
    def draw(self, surface):
        if not self.collected:
            # Draw coin with rotation effect
            coin_y = self.y + self.animation_offset
            
            # Create a surface for the coin to rotate
            coin_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(coin_surf, YELLOW, (10, 10), 10)
            pygame.draw.circle(coin_surf, (200, 170, 0), (10, 10), 10, 2)
            pygame.draw.circle(coin_surf, (180, 150, 0), (10, 10), 6)
            
            # Rotate the coin
            rotated_coin = pygame.transform.rotate(coin_surf, self.rotation)
            surface.blit(rotated_coin, (self.x - rotated_coin.get_width()//2, 
                                        coin_y - rotated_coin.get_height()//2))

def draw_ground(surface, ground_level):
    pygame.draw.rect(surface, GROUND_COLOR, (0, ground_level, WIDTH, HEIGHT - ground_level))
    
    # Draw grass on top
    pygame.draw.rect(surface, GREEN, (0, ground_level, WIDTH, 10))
    
    # Draw ground details
    for i in range(0, WIDTH, 15):
        pygame.draw.line(surface, (100, 60, 40), (i, ground_level), (i, HEIGHT), 1)

def draw_ui(surface, coins, lives):
    # Draw score panel
    pygame.draw.rect(surface, (200, 50, 50, 180), (10, 10, 150, 40), border_radius=10)
    pygame.draw.rect(surface, BLACK, (10, 10, 150, 40), 2, border_radius=10)
    
    # Draw coin
    pygame.draw.circle(surface, YELLOW, (30, 30), 12)
    pygame.draw.circle(surface, (200, 170, 0), (30, 30), 12, 2)
    
    # Draw coin count
    text = ui_font.render(f"x {coins}", True, WHITE)
    surface.blit(text, (45, 20))
    
    # Draw lives
    for i in range(lives):
        pygame.draw.circle(surface, RED, (WIDTH - 30 - i*20, 30), 8)
    
    # Draw title
    title = small_font.render("TECH DEMO - WASD CONTROLS", True, YELLOW)
    surface.blit(title, (WIDTH//2 - title.get_width()//2, 15))
    
    # Draw instructions
    instructions = [
        "W / SPACE - Jump",
        "A - Move Left",
        "D - Move Right",
        "S - Crouch",
        "Collect coins!",
        "Avoid spikes!"
    ]
    
    for i, inst in enumerate(instructions):
        text = small_font.render(inst, True, WHITE)
        surface.blit(text, (WIDTH - text.get_width() - 10, HEIGHT - 30 - i*20))

def create_tech_demo_stage():
    ground_level = HEIGHT - 50
    
    # Create platforms
    platforms = [
        Platform(100, ground_level - 100, 100, 20, LIGHT_BROWN),
        Platform(250, ground_level - 150, 80, 20, (200, 150, 100)),
        Platform(380, ground_level - 100, 120, 20, LIGHT_BROWN),
        Platform(150, ground_level - 200, 70, 20, (150, 200, 150)),
        Platform(50, ground_level - 250, 80, 20, LIGHT_BROWN),
        Platform(400, ground_level - 250, 100, 20, (200, 150, 100)),
        # Spike platforms
        Platform(200, ground_level - 50, 80, 20, is_spike=True),
        Platform(450, ground_level - 50, 80, 20, is_spike=True),
    ]
    
    # Create coins
    coins = [
        Coin(130, ground_level - 120),
        Coin(280, ground_level - 170),
        Coin(440, ground_level - 120),
        Coin(180, ground_level - 220),
        Coin(90, ground_level - 270),
        Coin(450, ground_level - 270),
    ]
    
    return platforms, coins, ground_level

def draw_paper_effect(surface, alpha):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (255, 255, 255, alpha), (0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(overlay, BLACK, (0, 0, WIDTH, HEIGHT), 3)
    
    # Draw paper texture
    for i in range(0, WIDTH, 20):
        pygame.draw.line(overlay, (0, 0, 0, 30), (i, 0), (i, HEIGHT), 1)
    for i in range(0, HEIGHT, 20):
        pygame.draw.line(overlay, (0, 0, 0, 30), (0, i), (WIDTH, i), 1)
    
    surface.blit(overlay, (0, 0))

def main():
    # Create game objects
    platforms, coins, ground_level = create_tech_demo_stage()
    koops = Koops(100, ground_level - 100)
    
    # Game variables
    collected_coins = 0
    lives = 3
    clock = pygame.time.Clock()
    
    # Paper effect variables
    paper_alpha = 0
    paper_effect_timer = 0
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    koops.jump()
                elif event.key == pygame.K_s:
                    koops.crouch(True)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    koops.crouch(False)
        
        # Get pressed keys for continuous movement
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_d]:
            dx = 1
        
        # Move Koops
        koops.move(dx, platforms, ground_level)
        
        # Update game objects
        koops.update(platforms, ground_level)
        for coin in coins:
            coin.update()
            
            # Check coin collection
            if not coin.collected:
                dist = math.sqrt((koops.x - coin.x)**2 + (koops.y - coin.y)**2)
                if dist < 30:
                    coin.collected = True
                    collected_coins += 1
        
        # Check spike collision
        for platform in platforms:
            if platform.is_spike:
                if (koops.x + koops.width > platform.x and 
                    koops.x < platform.x + platform.width and
                    koops.y + koops.height > platform.y and
                    koops.y < platform.y + platform.height):
                    # Player hit a spike
                    koops.hit_points -= 1
                    if koops.hit_points <= 0:
                        lives -= 1
                        koops.hit_points = 3
                        koops.x = 100
                        koops.y = ground_level - 100
                        paper_effect_timer = 30
                    
                    # Push player up
                    koops.y = platform.y - koops.height - 10
                    koops.velocity_y = -8
        
        # Paper effect animation
        if paper_effect_timer > 0:
            paper_effect_timer -= 1
            paper_alpha = min(150, paper_alpha + 10)
        else:
            paper_alpha = max(0, paper_alpha - 5)
        
        # Draw everything
        screen.fill(BACKGROUND)
        
        # Draw ground
        draw_ground(screen, ground_level)
        
        # Draw platforms
        for platform in platforms:
            platform.draw(screen)
        
        # Draw coins
        for coin in coins:
            coin.draw(screen)
        
        # Draw Koops
        koops.draw(screen)
        
        # Draw UI
        draw_ui(screen,R collected_coins, lives)
        
        # Draw paper effect
        if paper_alpha > 0:
            draw_paper_effect(screen, paper_alpha)
        
        # Game over check
        if lives <= 0:
            game_over_text = title_font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2))
            restart_text = ui_font.render("Press R to restart", True, WHITE)
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
            
            if keys[pygame.K_r]:
                # Reset game
                platforms, coins, ground_level = create_tech_demo_stage()
                koops = Koops(100, ground_level - 100)
                collected_coins = 0
                lives = 3
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
