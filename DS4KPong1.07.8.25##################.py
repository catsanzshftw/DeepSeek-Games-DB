import pygame
import sys
import math
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
PADDLE_SPEED = 7
AI_REACTION_SPEED = 0.5  # Lower means faster reaction
FPS = 60

# Colors - Neon/Synthwave palette
BLACK = (0, 0, 0)
PINK = (255, 16, 240)
BLUE = (16, 42, 255)
GREEN = (57, 255, 20)
YELLOW = (255, 236, 39)
PURPLE = (180, 16, 255)
NEON_COLORS = [PINK, BLUE, GREEN, YELLOW, PURPLE]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Pong")
clock = pygame.time.Clock()

# Initialize mixer for sound
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Sound synthesis functions
def generate_beep(frequency, duration, volume=0.5):
    """Generate a beep sound with given frequency and duration"""
    sample_rate = 44100
    samples = int(sample_rate * duration)
    
    # Create a sine wave
    buffer = bytearray()
    for i in range(samples):
        value = int(127 + 127 * volume * math.sin(2 * math.pi * frequency * i / sample_rate))
        buffer.append(value)
        buffer.append(value)  # For stereo (same value to both channels)
    
    return pygame.mixer.Sound(buffer=bytes(buffer))

def play_hit_sound():
    """Play a sound when the ball hits a paddle"""
    sound = generate_beep(660, 0.1, 0.4)
    sound.play()

def play_score_sound():
    """Play a sound when a point is scored"""
    sound = generate_beep(440, 0.3, 0.5)
    sound.play()

def play_wall_sound():
    """Play a sound when the ball hits a wall"""
    sound = generate_beep(330, 0.15, 0.3)
    sound.play()

# Ball class
class Ball:
    def __init__(self):
        self.reset()
        
    def move(self):
        self.x += self.dx
        self.y += self.dy
        
        # Bounce off top and bottom
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.dy = -self.dy
            play_wall_sound()
            
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        # Add a glow effect
        glow_surface = pygame.Surface((self.radius*4, self.radius*4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*self.color, 100), (self.radius*2, self.radius*2), self.radius*2)
        surface.blit(glow_surface, (self.x - self.radius*2, self.y - self.radius*2))
        
    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = BALL_RADIUS
        self.dx = random.choice([-1, 1]) * 5
        self.dy = random.choice([-1, 1]) * 5
        self.color = random.choice(NEON_COLORS)

# Paddle class
class Paddle:
    def __init__(self, x, y, is_ai=False):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED
        self.color = random.choice(NEON_COLORS)
        self.is_ai = is_ai
        self.ai_thinking = False
        
    def move(self, ball=None):
        if self.is_ai and ball is not None:
            # AI will move this paddle with reaction delay
            if random.random() > AI_REACTION_SPEED:
                # Move toward the ball's y position
                if self.y + self.height/2 < ball.y:
                    self.y += self.speed
                elif self.y + self.height/2 > ball.y:
                    self.y -= self.speed
        else:
            # Player controlled with arrow keys
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.y > 0:
                self.y -= self.speed
            if keys[pygame.K_DOWN] and self.y < HEIGHT - self.height:
                self.y += self.speed
        
        # Ensure paddle stays on screen
        self.y = max(0, min(self.y, HEIGHT - self.height))
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        # Add glow effect
        glow_surface = pygame.Surface((self.width+10, self.height+10), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (*self.color, 50), (5, 5, self.width, self.height))
        surface.blit(glow_surface, (self.x-5, self.y-5))

# Game initialization
player_paddle = Paddle(20, HEIGHT//2 - PADDLE_HEIGHT//2)
ai_paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, is_ai=True)
ball = Ball()
player_score = 0
ai_score = 0
font = pygame.font.Font(None, 74)

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Move game objects
    ball.move()
    player_paddle.move()
    ai_paddle.move(ball)
    
    # Ball collisions with paddles
    if ball.dx < 0:  # Moving left
        if (ball.x - ball.radius <= player_paddle.x + player_paddle.width and
            ball.y >= player_paddle.y and ball.y <= player_paddle.y + player_paddle.height):
            ball.dx = abs(ball.dx) * 1.05  # Speed up slightly
            ball.dy = random.uniform(-5, 5)
            play_hit_sound()
            ball.color = player_paddle.color
            
    else:  # Moving right
        if (ball.x + ball.radius >= ai_paddle.x and
            ball.y >= ai_paddle.y and ball.y <= ai_paddle.y + ai_paddle.height):
            ball.dx = -abs(ball.dx) * 1.05  # Speed up slightly
            ball.dy = random.uniform(-5, 5)
            play_hit_sound()
            ball.color = ai_paddle.color
    
    # Scoring
    if ball.x < 0:
        ai_score += 1
        play_score_sound()
        ball.reset()
    elif ball.x > WIDTH:
        player_score += 1
        play_score_sound()
        ball.reset()
    
    # Drawing
    screen.fill(BLACK)
    
    # Draw center line (dashed)
    for y in range(0, HEIGHT, 20):
        pygame.draw.rect(screen, PURPLE, (WIDTH//2 - 2, y, 4, 10))
    
    # Draw game objects
    ball.draw(screen)
    player_paddle.draw(screen)
    ai_paddle.draw(screen)
    
    # Draw scores
    player_text = font.render(str(player_score), True, GREEN)
    ai_text = font.render(str(ai_score), True, BLUE)
    screen.blit(player_text, (WIDTH//4, 20))
    screen.blit(ai_text, (3*WIDTH//4, 20))
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)
