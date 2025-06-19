import pygame
import math
import random
import sys

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paper Mario: Thousand-Year Door Engine")

# Colors
BACKGROUND = (100, 160, 255)
GROUND_COLOR = (136, 84, 50)
GREEN = (60, 160, 55)
RED = (222, 55, 55)
YELLOW = (255, 220, 70)
BLUE = (70, 150, 255)
BROWN = (139, 69, 19)
LIGHT_BROWN = (180, 140, 80)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
KOOPA_GREEN = (60, 150, 60)
KOOPA_SHELL = (130, 190, 70)
KOOPA_DARK = (40, 110, 40)
BANDANA_BLUE = (40, 110, 220)
PURPLE = (160, 80, 210)
ORANGE = (255, 145, 30)
PAPER_YELLOW = (250, 240, 180)
SHADOW = (0, 0, 0, 100)
MENU_BG = (80, 140, 220)
MENU_HIGHLIGHT = (120, 180, 255)

class VectorFont:
    @staticmethod
    def render_text(surface, text, x, y, size, color, outline_color=BLACK, outline=2):
        char_width = size * 0.6
        spacing = size * 0.1
        
        for i, char in enumerate(text):
            char_x = x + i * (char_width + spacing)
            VectorFont.draw_char(surface, char, char_x, y, size, color, outline_color, outline)
    
    @staticmethod
    def draw_char(surface, char, x, y, size, color, outline_color, outline):
        scale = size / 30
        
        # Character definitions
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
            return
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
        elif char == '.':
            points = [[(15, 25), (15, 25)]]
        elif char == ',':
            points = [[(15, 25), (10, 30)]]
        elif char == "'":
            points = [[(15, 0), (15, 10)]]
        elif char == '"':
            points = [
                [(10, 0), (10, 10)],
                [(20, 0), (20, 10)]
            ]
        elif char == '(':
            points = [[(20, 0), (10, 15), (20, 30)]]
        elif char == ')':
            points = [[(10, 0), (20, 15), (10, 30)]]
        elif char == '[':
            points = [
                [(20, 0), (10, 0)],
                [(10, 0), (10, 30)],
                [(10, 30), (20, 30)]
            ]
        elif char == ']':
            points = [
                [(10, 0), (20, 0)],
                [(20, 0), (20, 30)],
                [(20, 30), (10, 30)]
            ]
        elif char == '-':
            points = [[(5, 15), (25, 15)]]
        else:
            # Default to a box for unsupported characters
            points = [
                [(0, 0), (30, 0)],
                [(30, 0), (30, 30)],
                [(30, 30), (0, 30)],
                [(0, 30), (0, 0)]
            ]
        
        # Draw the character
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
        self.width = 40
        self.height = 50
        self.walking_speed = 4
        self.running_speed = 6
        self.speed = self.walking_speed
        self.jump_power = 14
        self.velocity_y = 0
        self.gravity = 0.7
        self.direction = 1  # 1 for right, -1 for left
        self.leg_offset = 0
        self.head_bob = 0
        self.bandana_offset = 0
        self.is_jumping = False
        self.is_grounded = False
        self.crouching = False
        self.running = False
        self.hit_points = 3
        self.invincible = 0
        self.closing_eyes = 0
        
    def update(self, platforms, ground_level):
        # Update animation parameters
        time = pygame.time.get_ticks() * 0.01
        self.leg_offset = math.sin(time) * 4
        self.head_bob = math.sin(time * 3) * 1
        self.bandana_offset = math.sin(time * 2.5) * 3
        
        # Apply gravity
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        
        # Apply invincibility timer
        if self.invincible > 0:
            self.invincible -= 1
        
        # Check eye blink
        if self.closing_eyes > 0:
            self.closing_eyes -= 1
        elif random.random() < 0.005:  # Random blink
            self.closing_eyes = 7
            
        # Update ground collision
        self.is_grounded = False
        if self.y >= ground_level - self.height:
            self.y = ground_level - self.height
            self.velocity_y = 0
            self.is_grounded = True
            self.is_jumping = False
            
        # Platform collisions
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
            return
            
        # Determine speed (walk or run)
        self.speed = self.running_speed if self.running else self.walking_speed
            
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
            
        # Platform collisions horizontally
        for platform in platforms:
            if (self.x + self.width > platform.x and 
                self.x < platform.x + platform.width and
                self.y + self.height > platform.y and
                self.y < platform.y + platform.height):
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
            self.height = 35
        else:
            self.height = 50
            
    def run(self, run):
        self.running = run
    
    def damage(self):
        if self.invincible == 0:
            self.hit_points -= 1
            self.invincible = 30
            
    def draw(self, surface):
        # Draw shadow
        pygame.draw.ellipse(surface, SHADOW, 
            (self.x - 10, self.y + self.height - 5, 40, 10))
        
        # Draw shell (with shell design)
        shell_rect = (self.x - 15, self.y - 25, self.width, 25)
        pygame.draw.ellipse(surface, KOOPA_SHELL, shell_rect)
        pygame.draw.ellipse(surface, BLACK, shell_rect, 2)
        
        # Shell pattern
        nubs = [
            (self.x, self.y - 10), 
            (self.x - 10, self.y - 5),
            (self.x + 10, self.y - 5),
            (self.x, self.y)
        ]
        for pos in nubs:
            pygame.draw.circle(surface, (150, 175, 60), pos, 4)
            pygame.draw.circle(surface, BLACK, pos, 4, 1)
        
        # Draw head
        head_y = self.y - 40 + self.head_bob
        head_x = self.x
        
        # Draw bandana (with flowing effect)
        bandana_points = [
            (head_x - 20, head_y - self.bandana_offset - 5),
            (head_x - 15, head_y - self.bandana_offset - 8),
            (head_x + 15, head_y - self.bandana_offset - 8),
            (head_x + 20, head_y - self.bandana_offset - 5)
        ]
        pygame.draw.polygon(surface, BANDANA_BLUE, bandana_points)
        pygame.draw.polygon(surface, BLACK, bandana_points, 2)
        
        # Bandana knot
        pygame.draw.circle(surface, (30, 80, 200), 
                          (head_x, head_y - self.bandana_offset - 8), 4)
        
        # Head shape
        head_rect = (head_x - 15, head_y, 30, 18)
        pygame.draw.ellipse(surface, KOOPA_GREEN, head_rect)
        pygame.draw.ellipse(surface, KOOPA_DARK, head_rect, 2)
        
        # Eyes
        eye_x = head_x - 5 if self.direction == -1 else head_x + 5
        eye_x += self.direction  # Slight offset
        
        eye_open = self.closing_eyes < 4
        eye_height = 10 if eye_open else 2
        pygame.draw.ellipse(surface, WHITE, 
                           (eye_x - 5, head_y + 5, 10, eye_height))
        if eye_open:
            pupil_size = 4 if self.invincible % 6 >= 3 else 5
            pygame.draw.circle(surface, BLACK, 
                              (eye_x, head_y + 8), pupil_size)
        
        # Mouth (changes expression when hurt)
        if self.invincible > 0 and self.invincible % 10 > 4:
            # Hurt expression
            pygame.draw.arc(surface, (120, 40, 40), 
                           (head_x - 12, head_y - 1, 24, 12), 
                           math.pi, 2 * math.pi, 2)
        else:
            # Normal expression
            pygame.draw.arc(surface, KOOPA_DARK, 
                           (head_x - 8, head_y + 5, 16, 10), 
                           0, math.pi, 2)
        
        # Legs with walking effect
        for i, side in enumerate([-1, 1]):
            leg_x = self.x + side * 7
            leg_y = self.y - 15 + self.leg_offset * (1 if i == 0 else -1)
            pygame.draw.ellipse(surface, KOOPA_DARK, 
                              (leg_x - 5, leg_y, 10, 12))
            
        # Draw hit points (as health meter)
        for i in range(3):
            fill = i < self.hit_points
            hp_color = GREEN if fill else RED
            # Draw heart using vectors
            hp_x = self.x + i * 15
            hp_y = self.y - 55
            
            # Heart shape (two circles + triangle)
            pygame.draw.circle(surface, RED if fill else (120, 120, 120), 
                              (hp_x - 3, hp_y - 2), 4)
            pygame.draw.circle(surface, RED if fill else (120, 120, 120), 
                              (hp_x + 3, hp_y - 2), 4)
            pygame.draw.polygon(surface, RED if fill else (120, 120, 120), [
                (hp_x - 5, hp_y - 1),
                (hp_x + 5, hp_y - 1),
                (hp_x, hp_y + 5)
            ])
            
            # Outline
            pygame.draw.line(surface, BLACK, (hp_x - 3, hp_y - 2), (hp_x - 5, hp_y - 1), 1)
            pygame.draw.line(surface, BLACK, (hp_x - 3, hp_y - 2), (hp_x, hp_y + 5), 1)
            pygame.draw.line(surface, BLACK, (hp_x + 3, hp_y - 2), (hp_x + 5, hp_y - 1), 1)
            pygame.draw.line(surface, BLACK, (hp_x + 3, hp_y - 2), (hp_x, hp_y + 5), 1)

class Goomba:
    def __init__(self, x, y, ground_level, walk_range=100):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 20
        self.speed = 1.5
        self.direction = -1
        self.walk_range = walk_range
        self.start_x = x
        self.ground_level = ground_level
        self.squish = 0
        self.animation_offset = 0
        self.crushed = False
        
    def update(self):
        self.animation_offset = math.sin(pygame.time.get_ticks() * 0.03) * 2
        
        if not self.crushed:
            # Walk back and forth
            self.x += self.speed * self.direction
            if abs(self.x - self.start_x) > self.walk_range:
                self.direction *= -1
                
            # Set position on ground
            self.y = self.ground_level - self.height
                
    def draw(self, surface, camera_offset):
        if self.crushed:
            # Draw squished Goomba
            pygame.draw.ellipse(surface, BROWN,
                               (self.x - camera_offset, self.y + 5, 
                                self.width, 8))
            pygame.draw.ellipse(surface, BLACK, 
                               (self.x - camera_offset, self.y + 5, 
                                self.width, 8), 1)
            return
        
        # Draw shadow
        pygame.draw.ellipse(surface, SHADOW, 
                          (self.x - 10 - camera_offset, self.y + self.height - 3, 
                           30, 8))
        
        # Draw body
        body_rect = (self.x - camera_offset, self.y + self.animation_offset, 
                    self.width, self.height - (self.squish * 10))
        pygame.draw.ellipse(surface, BROWN, body_rect)
        pygame.draw.ellipse(surface, BLACK, body_rect, 1)
        
        # Feet
        pygame.draw.ellipse(surface, BLACK, 
                          (self.x - camera_offset + 5, self.y + self.height - 5, 
                           6, 5))
        pygame.draw.ellipse(surface, BLACK, 
                          (self.x - camera_offset + 19, self.y + self.height - 5, 
                           6, 5))
        
        # Eyes
        eye_offset = 0
        eye_pos = [
            (self.x - camera_offset + 8 + eye_offset, self.y + 7),
            (self.x - camera_offset + 22 + eye_offset, self.y + 7)
        ]
        for pos in eye_pos:
            pygame.draw.circle(surface, WHITE, pos, 4)
            pygame.draw.circle(surface, BLACK, pos, 2)
            
        # Eyebrows (give expression)
        pygame.draw.line(surface, BLACK, 
                        (self.x - camera_offset + 6, self.y + 4),
                        (self.x - camera_offset + 10, self.y + 2), 2)
        pygame.draw.line(surface, BLACK, 
                        (self.x - camera_offset + 24, self.y + 4),
                        (self.x - camera_offset + 20, self.y + 2), 2)

class Platform:
    def __init__(self, x, y, width, height, color=LIGHT_BROWN, is_spike=False, is_cloud=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.is_spike = is_spike
        self.is_cloud = is_cloud
        
    def draw(self, surface, camera_offset):
        x_pos = self.x - camera_offset
        
        if self.is_cloud:
            # Draw fluffy cloud platform
            cloud_color = (250, 250, 250)
            
            base_rect = (x_pos, self.y, self.width, 15)
            pygame.draw.rect(surface, cloud_color, base_rect)
            pygame.draw.rect(surface, (200, 200, 200), base_rect, 2)
            
            # Cloud fluff textures
            fluffs = [
                (x_pos + 10, self.y - 8, 25, 18),
                (x_pos + 40, self.y - 5, 35, 22),
                (x_pos + 90, self.y - 6, 30, 20),
                (x_pos + 140, self.y - 8, 25, 18)
            ]
            for fluff in fluffs:
                pygame.draw.ellipse(surface, cloud_color, fluff)
                pygame.draw.ellipse(surface, (200, 200, 200), fluff, 1)
            return
        elif self.is_spike:
            # Draw spike platform
            pygame.draw.rect(surface, (140, 140, 140), 
                           (x_pos, self.y, self.width, self.height))
            pygame.draw.rect(surface, BLACK, 
                           (x_pos, self.y, self.width, self.height), 2)
            
            # Spikes
            for i in range(0, self.width, 15):
                spike_points = [
                    (x_pos + i, self.y + self.height),
                    (x_pos + i + 7, self.y + self.height - 12),
                    (x_pos + i + 14, self.y + self.height)
                ]
                pygame.draw.polygon(surface, (100, 100, 100), spike_points)
                pygame.draw.polygon(surface, BLACK, spike_points, 1)
            return
            
        # Regular brick platform
        pygame.draw.rect(surface, self.color, 
                        (x_pos, self.y, self.width, self.height))
        pygame.draw.rect(surface, (80, 45, 30), 
                        (x_pos, self.y, self.width, self.height), 2)
        
        # Brick patterns
        for i in range(0, self.width, 20):
            for j in range(0, self.height, 15):
                brick_x = x_pos + i
                brick_y = self.y + j
                pygame.draw.rect(surface, (self.color[0]-20, self.color[1]-20, self.color[2]-20),
                               (brick_x, brick_y, 18, 13))
                
        # Edge highlights
        pygame.draw.line(surface, (self.color[0]+20, self.color[1]+20, self.color[2]+20),
                        (x_pos + self.width - 1, self.y),
                        (x_pos + self.width - 1, self.y + self.height), 2)
        pygame.draw.line(surface, (self.color[0]+20, self.color[1]+20, self.color[2]+20),
                        (x_pos, self.y),
                        (x_pos + self.width, self.y), 2)

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.animation_offset = 0
        self.rotation = 0
        self.flash = 0
        
    def update(self):
        if self.collected:
            return
        self.animation_offset = math.sin(pygame.time.get_ticks() * 0.03) * 3
        self.rotation = (pygame.time.get_ticks() % 360) * 2
        self.flash = math.sin(pygame.time.get_ticks() * 0.1)
        
    def draw(self, surface, camera_offset):
        if self.collected:
            return
            
        coin_y = self.y + self.animation_offset
        coin_x = self.x - camera_offset
        coin_size = 15
        
        # Draw shiny base
        base_color = YELLOW
        pygame.draw.circle(surface, base_color, (coin_x, coin_y), coin_size)
        
        # Draw shine effect based on flash value
        if self.flash > 0.5:
            pygame.draw.ellipse(surface, (255, 255, 200),
                              (coin_x - coin_size*0.7, coin_y - coin_size*0.5, 
                               coin_size*1.4, coin_size*1.0))
        
        # Draw rotation effect
        pygame.draw.line(surface, ORANGE,
                       (coin_x - math.sin(math.radians(self.rotation)) * coin_size * 0.7,
                        coin_y - math.cos(math.radians(self.rotation)) * coin_size * 0.7),
                       (coin_x + math.sin(math.radians(self.rotation)) * coin_size * 0.7,
                        coin_y + math.cos(math.radians(self.rotation)) * coin_size * 0.7), 
                       3)
        
        # Draw outline
        pygame.draw.circle(surface, (200, 170, 0), (coin_x, coin_y), coin_size, 2)

class DialogBox:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.timer = 0
        self.typing_index = 0
        self.open = False
        
    def update(self):
        self.timer += 1
        if self.typing_index < len(self.text) and self.timer % 3 == 0:
            self.typing_index += 1
            
    def open_box(self):
        self.open = True
        self.timer = 0
        self.typing_index = 0
        
    def draw(self, surface):
        if not self.open:
            return
            
        # Draw main box with paper effect
        pygame.draw.rect(surface, PAPER_YELLOW, 
                       (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, BLACK, 
                       (self.x, self.y, self.width, self.height), 3)
        
        # Draw text
        displayed_text = self.text[:self.typing_index]
        VectorFont.render_text(surface, displayed_text, 
                            self.x + 20, self.y + 20, 
                            22, BLACK)
        
        # Draw arrow if text complete
        if self.typing_index == len(self.text) and self.timer % 20 < 10:
            arrow_y = self.y + self.height - 18
            pygame.draw.polygon(surface, BLACK, [
                (self.x + self.width - 25, arrow_y),
                (self.x + self.width - 15, arrow_y),
                (self.x + self.width - 20, arrow_y + 7)
            ])

def draw_background(surface, camera_offset):
    # Draw sky gradient
    for i in range(HEIGHT//2):
        color_val = 140 + int(i/(HEIGHT)*80)
        pygame.draw.line(surface, (color_val, color_val, 255), 
                       (0, i), (WIDTH, i))
    
    # Draw distant mountains
    mountain_color = (100, 120, 160)
    mountains = [
        (0, HEIGHT//2, WIDTH//4, HEIGHT//3, 30),
        (WIDTH//5, HEIGHT//2-20, WIDTH//4, HEIGHT//2.5, 50),
        (WIDTH//1.8, HEIGHT//2, WIDTH//4, HEIGHT//3, 60)
    ]
    
    for x, y, w, h, offset in mountains:
        adjusted_x = (x - camera_offset * 0.1) % (WIDTH + w) - w
        pygame.draw.polygon(surface, mountain_color, [
            (adjusted_x, y),
            (adjusted_x + w//2, y - h),
            (adjusted_x + w, y),
            (adjusted_x + w, HEIGHT),
            (adjusted_x, HEIGHT)
        ])
        # Mountain outline
        pygame.draw.line(surface, BLACK, (adjusted_x, y), (adjusted_x + w//2, y - h), 2)
        pygame.draw.line(surface, BLACK, (adjusted_x + w//2, y - h), (adjusted_x + w, y), 2)
        
    # Draw clouds
    cloud_offset = (camera_offset * 0.2) % WIDTH
    clouds = [
        (cloud_offset - 150, 50, 100, 40),
        (cloud_offset, 80, 120, 35),
        (cloud_offset + 200, 40, 90, 30)
    ]
    
    for x, y, w, h in clouds:
        pygame.draw.ellipse(surface, (250, 250, 255), (x, y, w, h))
        pygame.draw.ellipse(surface, (200, 200, 255), (x, y, w, h), 2)

def draw_ground(surface, ground_level, camera_offset):
    # Draw grass
    pygame.draw.rect(surface, GROUND_COLOR, 
                   (0 - camera_offset, ground_level, WIDTH*2, HEIGHT - ground_level))
    
    # Draw grass top
    pygame.draw.rect(surface, GREEN, 
                   (0 - camera_offset, ground_level, WIDTH*2, 12))
    
    # Draw grass tufts
    for i in range(0, WIDTH*2, 20):
        height = random.randint(0, 5)
        for j in range(4):
            line_x = i - camera_offset + j * 4
            pygame.draw.line(surface, GREEN, 
                           (line_x, ground_level),
                           (line_x, ground_level - height - j//2), 1)
    
    # Draw ground details
    for i in range(0, WIDTH*2, 15):
        x = i - camera_offset
        pygame.draw.line(surface, (100, 60, 40), 
                       (x, ground_level + 10), (x, ground_level + 40), 1)

def draw_ui(surface, coins, lives):
    # Draw score panel (curved)
    panel_y = 20
    pygame.draw.rect(surface, (70, 40, 30, 220), 
                   (WIDTH//2 - 100, panel_y, 200, 50), 
                   border_radius=15)
    pygame.draw.rect(surface, BLACK, 
                   (WIDTH//2 - 100, panel_y, 200, 50), 
                   3, border_radius=15)
    
    # Draw coin
    pygame.draw.circle(surface, YELLOW, (WIDTH//2 - 50, panel_y + 25), 15)
    pygame.draw.circle(surface, ORANGE, (WIDTH//2 - 50, panel_y + 25), 15, 2)
    
    # Draw star
    pygame.draw.circle(surface, (220, 220, 100), (WIDTH//2 + 50, panel_y + 25), 13)
    pygame.draw.circle(surface, (180, 180, 70), (WIDTH//2 + 50, panel_y + 25), 13, 2)
    
    # Draw coin and star counts
    VectorFont.render_text(surface, f"x{coins}", 
                        WIDTH//2 - 25, panel_y + 10, 
                        24, WHITE)
    
    VectorFont.render_text(surface, f"x{lives}", 
                        WIDTH//2 + 75, panel_y + 10, 
                        24, WHITE)
    
    # Draw title with outline
    VectorFont.render_text(surface, "KOOP THE KOOPA", 
                        WIDTH//2 - 90, HEIGHT - 40, 
                        26, YELLOW)
    
    # Draw instructions
    if pygame.time.get_ticks() < 10000:  # Show only in the beginning
        VectorFont.render_text(surface, "Hold SHIFT to run", 
                            WIDTH//2 - 80, HEIGHT - 90, 
                            18, WHITE)

def draw_main_menu(surface, selection):
    # Draw menu background
    surface.fill(MENU_BG)
    
    # Draw decorative paper texture
    for i in range(0, WIDTH, 40):
        for j in range(0, HEIGHT, 40):
            pygame.draw.rect(surface, (70, 130, 210), (i, j, 35, 35), 1)
    
    # Draw title banner
    pygame.draw.rect(surface, RED, (0, 50, WIDTH, 120))
    pygame.draw.rect(surface, (180, 40, 40), (0, 50, WIDTH, 120), 3)
    
    # Draw title with vector font
    VectorFont.render_text(surface, "PAPER MARIO", 
                        WIDTH//2 - 180, 70, 
                        60, YELLOW, BLACK, 4)
    
    VectorFont.render_text(surface, "KOOPA ENGINE 1.0", 
                        WIDTH//2 - 220, 130, 
                        48, WHITE, BLACK, 3)
    
    # Draw Koopa character
    koopa_x = WIDTH//2
    koopa_y = HEIGHT//2 + 40
    
    # Draw shell
    pygame.draw.ellipse(surface, KOOPA_SHELL, 
                      (koopa_x - 60, koopa_y - 40, 120, 60))
    pygame.draw.ellipse(surface, BLACK, 
                      (koopa_x - 60, koopa_y - 40, 120, 60), 3)
    
    # Draw head
    pygame.draw.ellipse(surface, KOOPA_GREEN, 
                      (koopa_x - 40, koopa_y - 70, 80, 40))
    pygame.draw.ellipse(surface, BLACK, 
                      (koopa_x - 40, koopa_y - 70, 80, 40), 2)
    
    # Draw eyes
    pygame.draw.circle(surface, WHITE, (koopa_x - 15, koopa_y - 55), 10)
    pygame.draw.circle(surface, WHITE, (koopa_x + 15, koopa_y - 55), 10)
    pygame.draw.circle(surface, BLACK, (koopa_x - 15, koopa_y - 55), 4)
    pygame.draw.circle(surface, BLACK, (koopa_x + 15, koopa_y - 55), 4)
    
    # Draw bandana
    bandana_points = [
        (koopa_x - 50, koopa_y - 70),
        (koopa_x - 30, koopa_y - 100),
        (koopa_x + 30, koopa_y - 100),
        (koopa_x + 50, koopa_y - 70)
    ]
    pygame.draw.polygon(surface, BANDANA_BLUE, bandana_points)
    pygame.draw.polygon(surface, BLACK, bandana_points, 2)
    
    # Draw menu options
    options = [
        "START GAME",
        "CONTROLS",
        "QUIT"
    ]
    
    for i, option in enumerate(options):
        y_pos = HEIGHT//2 + 120 + i * 50
        color = WHITE if i != selection else YELLOW
        
        # Draw selection highlight
        if i == selection:
            pygame.draw.rect(surface, MENU_HIGHLIGHT, 
                          (WIDTH//2 - 110, y_pos - 25, 220, 40), 
                          border_radius=10)
            pygame.draw.rect(surface, BLACK, 
                          (WIDTH//2 - 110, y_pos - 25, 220, 40), 
                          3, border_radius=10)
        
        # Draw option text
        VectorFont.render_text(surface, option, 
                            WIDTH//2 - 80, y_pos - 10, 
                            30, color)
    
    # Draw copyright
    VectorFont.render_text(surface, "© 2023 KOOPA STUDIOS", 
                        WIDTH//2 - 120, HEIGHT - 30, 
                        20, WHITE)

def draw_boot_screen(surface, progress):
    # Draw boot screen background
    surface.fill((30, 30, 60))
    
    # Draw loading bar frame
    bar_width = 400
    bar_height = 30
    bar_x = (WIDTH - bar_width) // 2
    bar_y = HEIGHT // 2 + 50
    
    pygame.draw.rect(surface, (60, 60, 100), 
                   (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(surface, BLACK, 
                   (bar_x, bar_y, bar_width, bar_height), 3)
    
    # Draw loading bar
    fill_width = int(bar_width * progress)
    pygame.draw.rect(surface, BLUE, 
                   (bar_x, bar_y, fill_width, bar_height))
    
    # Draw loading text
    VectorFont.render_text(surface, "LOADING KOOPA ENGINE...", 
                        WIDTH//2 - 180, HEIGHT//2 - 30, 
                        36, WHITE)
    
    # Draw progress percentage
    percent = int(progress * 100)
    VectorFont.render_text(surface, f"{percent}%", 
                        WIDTH//2 - 30, bar_y + bar_height + 20, 
                        24, WHITE)
    
    # Draw decorative elements
    for i in range(20):
        size = random.randint(5, 15)
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT//2 - 50)
        pygame.draw.circle(surface, (100, 100, 200), (x, y), size)
        pygame.draw.circle(surface, (70, 70, 180), (x, y), size, 1)

def create_stage():
    ground_level = HEIGHT - 60
    
    # Create platforms
    platforms = [
        Platform(300, ground_level - 120, 140, 20, (180, 160, 130), is_cloud=True),
        Platform(600, ground_level - 180, 110, 20, (150, 200, 150)),
        Platform(900, ground_level - 80, 120, 20, LIGHT_BROWN),
        Platform(1200, ground_level - 160, 70, 20, (200, 150, 100)),
        Platform(1500, ground_level - 220, 80, 20, LIGHT_BROWN),
        Platform(1800, ground_level - 140, 100, 20, (200, 150, 100)),
        
        # Spike platforms
        Platform(400, ground_level - 40, 80, 20, is_spike=True),
        Platform(1100, ground_level - 40, 80, 20, is_spike=True),
    ]
    
    # Create coins
    coins = [
        Coin(320, ground_level - 150),
        Coin(650, ground_level - 220),
        Coin(950, ground_level - 120),
        Coin(1230, ground_level - 190),
        Coin(1530, ground_level - 250),
        Coin(1840, ground_level - 170),
    ]
    
    # Create Goombas
    goombas = [
        Goomba(100, ground_level, ground_level),
        Goomba(800, ground_level, ground_level),
        Goomba(1400, ground_level, ground_level),
        Goomba(1900, ground_level, ground_level, 150)
    ]
    
    return platforms, coins, goombas, ground_level

def main():
    game_states = {
        "MENU": 0,
        "BOOT": 1,
        "GAMEPLAY": 2,
        "GAME_OVER": 3
    }
    game_state = game_states["MENU"]
    
    # Menu variables
    menu_selection = 0
    boot_progress = 0
    
    # Create game objects
    platforms, coins, goombas, ground_level = create_stage()
    koops = Koops(400, ground_level - 100)
    
    # Camera system - follows Koops horizontally
    camera_offset = 0
    
    # Dialog box
    dialog = DialogBox("JUMP ON ENEMIES TO DEFEAT THEM! WATCH OUT FOR SPIKES!", 
                      WIDTH//2 - 250, 100, 500, 80)
    
    # Game variables
    collected_coins = 0
    lives = 3
    clock = pygame.time.Clock()
    game_time = 0
    
    # Particles for effects
    particles = []
    
    # Main game loop
    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0
        game_time += delta_time * 1000
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if game_state == game_states["MENU"]:
                    if event.key == pygame.K_DOWN:
                        menu_selection = (menu_selection + 1) % 3
                    elif event.key == pygame.K_UP:
                        menu_selection = (menu_selection - 1) % 3
                    elif event.key == pygame.K_RETURN:
                        if menu_selection == 0:  # Start Game
                            game_state = game_states["BOOT"]
                            boot_progress = 0
                        elif menu_selection == 2:  # Quit
                            running = False
                
                elif game_state == game_states["GAMEPLAY"]:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                        koops.jump()
                    elif event.key == pygame.K_s:
                        koops.crouch(True)
                    elif event.key == pygame.K_LSHIFT:
                        koops.run(True)
                
                elif game_state == game_states["GAME_OVER"] and event.key == pygame.K_r:
                    # Reset game
                    platforms, coins, goombas, ground_level = create_stage()
                    koops = Koops(400, ground_level - 100)
                    collected_coins = 0
                    lives = 3
                    game_state = game_states["GAMEPLAY"]
            
            elif event.type == pygame.KEYUP and game_state == game_states["GAMEPLAY"]:
                if event.key == pygame.K_s:
                    koops.crouch(False)
                elif event.key == pygame.K_LSHIFT:
                    koops.run(False)
        
        # Draw based on game state
        if game_state == game_states["MENU"]:
            # Draw main menu
            draw_main_menu(screen, menu_selection)
        
        elif game_state == game_states["BOOT"]:
            # Update boot progress
            boot_progress += 0.02
            if boot_progress >= 1.0:
                game_state = game_states["GAMEPLAY"]
                dialog.open_box()
            
            # Draw boot screen
            draw_boot_screen(screen, boot_progress)
        
        elif game_state == game_states["GAMEPLAY"] or game_state == game_states["GAME_OVER"]:
            # Update camera
            target_offset = koops.x - WIDTH//2
            camera_offset = camera_offset * 0.9 + target_offset * 0.1
            
            # Draw background
            screen.fill(BACKGROUND)
            draw_background(screen, camera_offset)
            
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
            dialog.update()
            
            for coin in coins:
                coin.update()
                
                # Check coin collection
                if not coin.collected:
                    dist = math.sqrt((koops.x - coin.x)**2 + (koops.y - coin.y)**2)
                    if dist < 30:
                        coin.collected = True
                        collected_coins += 1
                        # Add coin particle effect
                        for _ in range(10):
                            particles.append([
                                coin.x, coin.y,
                                random.uniform(-2.5, 2.5), 
                                random.uniform(-3.5, -1.5),
                                30,  # max life
                                YELLOW
                            ])
            
            # Update and draw particles
            for p in particles[:]:
                p[0] += p[2]  # x + speed_x
                p[1] += p[3]  # y + speed_y
                p[3] += 0.15  # gravity
                p[4] -= 1  # lifetime decrease
                
                if p[4] <= 0:
                    particles.remove(p)
                else:
                    # Draw particle
                    pygame.draw.circle(screen, p[5], 
                                   (int(p[0] - camera_offset), int(p[1])), 
                                   max(1, int(p[4] / 10)))
            
            # Update Goombas
            for goomba in goombas:
                goomba.update()
                
                # Goomba collision
                if not goomba.crushed:
                    # Horizontal collision
                    if (koops.x + koops.width > goomba.x + 5 and 
                        koops.x < goomba.x + goomba.width - 5 and
                        koops.y + koops.height - 5 > goomba.y and
                        koops.y < goomba.y + goomba.height):
                        
                        if koops.y + koops.height < goomba.y + 10 and koops.velocity_y > 0:
                            # Jumped on enemy
                            goomba.crushed = True
                            koops.velocity_y = -koops.jump_power * 0.7
                            # Add particle effect
                            for _ in range(15):
                                particles.append([
                                    goomba.x, goomba.y,
                                    random.uniform(-2.5, 2.5), 
                                    random.uniform(-4, -2),
                                    20,  # max life
                                    BROWN
                                ])
                        elif koops.invincible == 0:
                            # Damaged by enemy
                            koops.damage()
            
            # Check spike collision
            for platform in platforms:
                if platform.is_spike:
                    if (koops.x + koops.width > platform.x and 
                        koops.x < platform.x + platform.width and
                        koops.y + koops.height > platform.y and
                        koops.y < platform.y + platform.height):
                        # Player hit a spike
                        koops.damage()
                        # Push player away
                        koops.velocity_y = -8
                        if koops.x < platform.x + platform.width//2:
                            koops.x = platform.x - koops.width - 5
                        else:
                            koops.x = platform.x + platform.width + 5
                        
                        # Add red damage particles
                        for _ in range(15):
                            particles.append([
                                koops.x + koops.width//2, 
                                koops.y + koops.height,
                                random.uniform(-3, 3), 
                                random.uniform(-5, -3),
                                25,  # max life
                                RED
                            ])
            
            # Draw ground
            draw_ground(screen, ground_level, camera_offset)
            
            # Draw platforms
            for platform in platforms:
                platform.draw(screen, camera_offset)
            
            # Draw coins
            for coin in coins:
                coin.draw(screen, camera_offset)
            
            # Draw Goombas
            for goomba in goombas:
                goomba.draw(screen, camera_offset)
            
            # Draw Koops
            koops.draw(screen)
            
            # Draw UI
            draw_ui(screen, collected_coins, lives)
            
            # Draw dialog box
            dialog.draw(screen)
            
            # Update lives based on hit points
            if koops.hit_points <= 0:
                lives -= 1
                koops.hit_points = 3
                koops.x = camera_offset + WIDTH//2
                koops.y = ground_level - 100
                koops.velocity_y = 0
            
            # Game over check
            if lives <= 0:
                game_state = game_states["GAME_OVER"]
                # Draw game over screen with parallax
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (0, 0))
                
                VectorFont.render_text(screen, "GAME OVER", 
                                    WIDTH//2 - 100, HEIGHT//2 - 50, 
                                    50, RED, WHITE, 5)
                VectorFont.render_text(screen, "PRESS R TO RESTART", 
                                    WIDTH//2 - 140, HEIGHT//2 + 30, 
                                    28, YELLOW)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
