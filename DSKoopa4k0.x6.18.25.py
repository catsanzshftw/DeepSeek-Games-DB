import pygame
import math
import random
import sys

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paper Mario TTY Engine")

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
PURPLE = (150, 70, 200)
ORANGE = (245, 150, 66)
PAPER_YELLOW = (250, 240, 180)

class VectorFont:
    @staticmethod
    def render_text(surface, text, x, y, size, color, outline_color=BLACK, outline=2):
        # Draw each character as vector shapes
        char_width = size * 0.6
        spacing = size * 0.1
        
        for i, char in enumerate(text):
            char_x = x + i * (char_width + spacing)
            VectorFont.draw_char(surface, char, char_x, y, size, color, outline_color, outline)
    
    @staticmethod
    def draw_char(surface, char, x, y, size, color, outline_color, outline):
        # Scale all points by size
        scale = size / 30
        
        # Character definitions - each character is defined by a list of lines
        if char == 'A':
            points = [
                [(0, 30), (15, 0)],
                [(15, 0), (30, 30)],
                [(5, 20), (25, 20)]
            ]
        elif char == 'B':
            points = [
                [(0, 0), (0, 30)],
                [(0, 0), (20, 0), (25, 5), (25, 10), (20, 15), (0, 15)],
                [(0, 15), (20, 15), (25, 20), (25, 25), (20, 30), (0, 30)]
            ]
        elif char == 'C':
            points = [
                [(25, 0), (5, 0), (0, 5), (0, 25), (5, 30), (25, 30)]
            ]
        elif char == 'D':
            points = [
                [(0, 0), (0, 30)],
                [(0, 0), (20, 0), (30, 10), (30, 20), (20, 30), (0, 30)]
            ]
        elif char == 'E':
            points = [
                [(0, 0), (0, 30)],
                [(0, 0), (25, 0)],
                [(0, 15), (20, 15)],
                [(0, 30), (25, 30)]
            ]
        elif char == 'F':
            points = [
                [(0, 0), (0, 30)],
                [(0, 0), (25, 0)],
                [(0, 15), (20, 15)]
            ]
        elif char == 'G':
            points = [
                [(25, 0), (5, 0), (0, 5), (0, 25), (5, 30), (25, 30), (30, 25)],
                [(30, 25), (20, 25), (20, 15)]
            ]
        elif char == 'H':
            points = [
                [(0, 0), (0, 30)],
                [(30, 0), (30, 30)],
                [(0, 15), (30, 15)]
            ]
        elif char == 'I':
            points = [
                [(0, 0), (30, 0)],
                [(15, 0), (15, 30)],
                [(0, 30), (30, 30)]
            ]
        elif char == 'J':
            points = [
                [(15, 0), (30, 0)],
                [(30, 0), (30, 20), (25, 30), (15, 30), (10, 25), (10, 20)]
            ]
        elif char == 'K':
            points = [
                [(0, 0), (0, 30)],
                [(0, 15), (30, 0)],
                [(0, 15), (30, 30)]
            ]
        elif char == 'L':
            points = [
                [(0, 0), (0, 30)],
                [(0, 30), (25, 30)]
            ]
        elif char == 'M':
            points = [
                [(0, 30), (0, 0), (15, 15), (30, 0), (30, 30)]
            ]
        elif char == 'N':
            points = [
                [(0, 30), (0, 0), (30, 30), (30, 0)]
            ]
        elif char == 'O':
            points = [
                [(0, 0), (0, 30), (30, 30), (30, 0), (0, 0)]
            ]
        elif char == 'P':
            points = [
                [(0, 0), (0, 30)],
                [(0, 0), (20, 0), (30, 10), (30, 15), (20, 30), (0, 30)]
            ]
        elif char == 'Q':
            points = [
                [(0, 0), (0, 30), (30, 30), (30, 0), (0, 0)],
                [(15, 15), (30, 30)]
            ]
        elif char == 'R':
            points = [
                [(0, 0), (0, 30)],
                [(0, 0), (20, 0), (30, 10), (30, 15), (20, 30), (0, 30)],
                [(15, 15), (30, 30)]
            ]
        elif char == 'S':
            points = [
                [(25, 0), (5, 0), (0, 5), (0, 15), (5, 15), (25, 15), (30, 20), (30, 25), (25, 30), (5, 30)]
            ]
        elif char == 'T':
            points = [
                [(0, 0), (30, 0)],
                [(15, 0), (15, 30)]
            ]
        elif char == 'U':
            points = [
                [(0, 0), (0, 25), (5, 30), (25, 30), (30, 25), (30, 0)]
            ]
        elif char == 'V':
            points = [
                [(0, 0), (15, 30), (30, 0)]
            ]
        elif char == 'W':
            points = [
                [(0, 0), (0, 30), (15, 15), (30, 30), (30, 0)]
            ]
        elif char == 'X':
            points = [
                [(0, 0), (30, 30)],
                [(30, 0), (0, 30)]
            ]
        elif char == 'Y':
            points = [
                [(0, 0), (15, 15), (30, 0)],
                [(15, 15), (15, 30)]
            ]
        elif char == 'Z':
            points = [
                [(0, 0), (30, 0)],
                [(30, 0), (0, 30)],
                [(0, 30), (30, 30)]
            ]
        elif char == ' ':
            return  # Skip space
        elif char == '!':
            points = [
                [(15, 0), (15, 20)],
                [(15, 25), (15, 30)]
            ]
        elif char == '?':
            points = [
                [(5, 0), (25, 0), (30, 5), (30, 15), (20, 25), (15, 25)],
                [(15, 30), (15, 30)]
            ]
        elif char == '/':
            points = [[(30, 0), (0, 30)]]
        elif char == ':':
            points = [
                [(15, 10), (15, 10)],
                [(15, 20), (15, 20)]
            ]
        else:
            return  # Skip unsupported characters
        
        # Draw the character with outline
        for line in points:
            scaled_line = []
            for point in line:
                scaled_point = (x + point[0] * scale, y + point[1] * scale)
                scaled_line.append(scaled_point)
            
            # Draw outline
            if len(scaled_line) > 1:
                pygame.draw.lines(surface, outline_color, False, scaled_line, outline + 2)
            
            # Draw main line
            pygame.draw.lines(surface, color, False, scaled_line, outline)

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
            coin_x = self.x
            
            # Create a surface for the coin to rotate
            coin_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(coin_surf, YELLOW, (10, 10), 10)
            pygame.draw.circle(coin_surf, (200, 170, 0), (10, 10), 10, 2)
            pygame.draw.circle(coin_surf, (180, 150, 0), (10, 10), 6)
            
            # Rotate the coin
            rotated_coin = pygame.transform.rotate(coin_surf, self.rotation)
            surface.blit(rotated_coin, (coin_x - rotated_coin.get_width()//2, 
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
    
    # Draw coin count with vector font
    VectorFont.render_text(surface, f"x{coins}", 45, 20, 24, WHITE)
    
    # Draw lives
    for i in range(lives):
        pygame.draw.circle(surface, RED, (WIDTH - 30 - i*20, 30), 8)
    
    # Draw title with vector font
    VectorFont.render_text(surface, "TTY ENGINE", WIDTH//2 - 100, 15, 24, YELLOW)
    
    # Draw instructions with vector font
    instructions = [
        "W/SPC - JUMP",
        "A - LEFT",
        "D - RIGHT",
        "S - CROUCH",
        "COLLECT COINS!",
        "AVOID SPIKES!"
    ]
    
    for i, inst in enumerate(instructions):
        VectorFont.render_text(surface, inst, WIDTH - 180, HEIGHT - 30 - i*20, 16, WHITE)

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

def draw_main_menu(surface):
    # Draw paper-like background
    surface.fill(PAPER_YELLOW)
    
    # Draw decorative elements
    for i in range(20):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(5, 20)
        pygame.draw.rect(surface, (240, 230, 180), (x, y, size, size))
        pygame.draw.rect(surface, BROWN, (x, y, size, size), 1)
    
    # Draw title with vector font
    VectorFont.render_text(surface, "PAPER MARIO", WIDTH//2 - 150, 80, 40, RED, BLACK, 3)
    VectorFont.render_text(surface, "TTY ENGINE", WIDTH//2 - 130, 140, 40, BLUE, BLACK, 3)
    
    # Draw Koops character
    pygame.draw.ellipse(surface, (160, 190, 70), (WIDTH//2 - 40, HEIGHT//2, 80, 60))
    pygame.draw.ellipse(surface, BLACK, (WIDTH//2 - 40, HEIGHT//2, 80, 60), 2)
    
    # Draw head
    head_x = WIDTH//2
    head_y = HEIGHT//2 - 20
    pygame.draw.ellipse(surface, KOOPA_GREEN, (head_x - 20, head_y, 40, 25))
    pygame.draw.ellipse(surface, BLACK, (head_x - 20, head_y, 40, 25), 2)
    
    # Draw eyes
    pygame.draw.circle(surface, WHITE, (head_x - 8, head_y + 10), 8)
    pygame.draw.circle(surface, BLACK, (head_x - 8, head_y + 10), 4)
    pygame.draw.circle(surface, WHITE, (head_x + 8, head_y + 10), 8)
    pygame.draw.circle(surface, BLACK, (head_x + 8, head_y + 10), 4)
    
    # Draw bandana
    bandana_points = [
        (head_x - 25, head_y - 5),
        (head_x - 15, head_y - 15),
        (head_x + 15, head_y - 15),
        (head_x + 25, head_y - 5)
    ]
    pygame.draw.polygon(surface, BANDANA_BLUE, bandana_points)
    pygame.draw.polygon(surface, BLACK, bandana_points, 2)
    
    # Draw menu options
    VectorFont.render_text(surface, "PRESS SPACE TO START", WIDTH//2 - 140, HEIGHT - 80, 24, BLACK)
    VectorFont.render_text(surface, "WASD TO MOVE", WIDTH//2 - 80, HEIGHT - 50, 20, BLACK)

def main():
    # Game states
    MENU = 0
    GAMEPLAY = 1
    GAME_OVER = 2
    
    game_state = MENU
    
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
                if game_state == MENU and event.key == pygame.K_SPACE:
                    game_state = GAMEPLAY
                elif game_state == GAMEPLAY:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                        koops.jump()
                    elif event.key == pygame.K_s:
                        koops.crouch(True)
                elif game_state == GAME_OVER and event.key == pygame.K_r:
                    # Reset game
                    platforms, coins, ground_level = create_tech_demo_stage()
                    koops = Koops(100, ground_level - 100)
                    collected_coins = 0
                    lives = 3
                    game_state = GAMEPLAY
            elif event.type == pygame.KEYUP and game_state == GAMEPLAY:
                if event.key == pygame.K_s:
                    koops.crouch(False)
        
        # Draw based on game state
        screen.fill(BACKGROUND)
        
        if game_state == MENU:
            draw_main_menu(screen)
        elif game_state == GAMEPLAY or game_state == GAME_OVER:
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
            draw_ui(screen, collected_coins, lives)
            
            # Draw paper effect
            if paper_alpha > 0:
                draw_paper_effect(screen, paper_alpha)
            
            # Game over check
            if lives <= 0:
                game_state = GAME_OVER
                VectorFont.render_text(screen, "GAME OVER", WIDTH//2 - 80, HEIGHT//2 - 30, 40, RED, BLACK, 3)
                VectorFont.render_text(screen, "PRESS R TO RESTART", WIDTH//2 - 120, HEIGHT//2 + 20, 24, BLACK)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
