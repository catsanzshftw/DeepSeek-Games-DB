import numpy
import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Define color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
COLORS = [RED, GREEN, BLUE, (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Game window dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Boy Breakout")

# Clock for framerate
clock = pygame.time.Clock()

# Simple sound synthesizer variables
SAMPLE_RATE = 44100
sound_buffer = None
sound_channel = None
last_note_time = 0


def generate_square_wave(frequency, duration):
    """Generate a square wave sound at the given frequency for duration seconds."""
    global SAMPLE_RATE
    
    n_samples = int(SAMPLE_RATE * duration)
    buf = numpy.zeros((n_samples, 2), dtype=numpy.int16)
    
    samples_per_cycle = SAMPLE_RATE / frequency
    amp = 16384 * 0.5  # Adjust volume
    
    for s in range(n_samples):
        phase = s / samples_per_cycle
        # Simple square wave (value alternates between +amp and -amp)
        value = amp if (phase % 1) < 0.5 else -amp
        buf[s][0] = int(value)
        buf[s][1] = int(value)
    
    return buf


def play_note(frequency, duration=0.1):
    """Play a note with the given frequency for the duration."""
    global sound_channel, sound_buffer, last_note_time
    
    # To prevent too many sounds playing at once which can distort
    current_time = time.time()
    if current_time - last_note_time < 0.03:
        return
    last_note_time = current_time
    
    # Generate the sound buffer
    sound_buffer = pygame.sndarray.make_sound(generate_square_wave(frequency, duration))
    
    # Play the sound
    if sound_channel:
        # If a channel is playing currently, stop it (max 1 sound at a time for simplicity)
        sound_channel.stop()
    
    sound_channel = sound_buffer.play()


class Paddle(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, WHITE, [0, 0, width, height])
        self.rect = self.image.get_rect()
        
    def move_left(self, pixels):
        self.rect.x -= pixels
        if self.rect.x < 0:
            self.rect.x = 0
    
    def move_right(self, pixels):
        self.rect.x += pixels
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width


class Ball(pygame.sprite.Sprite):
    def __init__(self, diameter):
        super().__init__()
        self.image = pygame.Surface([diameter, diameter]) 
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, WHITE, [0, 0, diameter, diameter])
        self.rect = self.image.get_rect()
        self.velocity = [random.choice([-5, 4]), -4]
        self.diameter = diameter
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        
        # Bounce off top and sides   
        if self.rect.x <= 0 or self.rect.x >= WIDTH - self.diameter:
            self.velocity[0] = -self.velocity[0]
            play_note(440, 0.05)  # Wall hit sound
            
        if self.rect.y <= 0:
            self.velocity[1] = -self.velocity[1]
            play_note(440, 0.05)  # Wall hit sound
            
    def bounce(self):
        self.velocity[1] = -self.velocity[1]
        play_note(880, 0.1)  # Paddle hit sound


class Brick(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.color = color


def main():
    global sound_channel
    
    # Initialize sound system
    try:
        import numpy
        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2)
        sound_channel = pygame.mixer.Channel(0)
    except ImportError:
        print("Warning: numpy not found. Sound will be disabled.")
        sound_enabled = False
    else:
        sound_enabled = True
    
    # Create game objects
    paddle = Paddle(100, 10)
    paddle.rect.x = 350
    paddle.rect.y = 560
    
    ball = Ball(10)
    ball.rect.x = 345
    ball.rect.y = 300
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle)
    all_sprites.add(ball)
    
    bricks = pygame.sprite.Group()
    for row in range(5):
        for col in range(7):
            brick = Brick(random.choice(COLORS), 80, 30)
            brick.rect.x = 60 + col * 100
            brick.rect.y = 60 + row * 60
            bricks.add(brick)
            all_sprites.add(brick)
    
    # Game variables
    score = 0
    lives = 3
    font = pygame.font.Font(None, 36)
    game_over = False
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    # Reset game
                    main()
                    return
        
        if not game_over:
            # Move paddle
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move_left(5)
            if keys[pygame.K_RIGHT]:
                paddle.move_right(5)
            
            # Update ball
            ball.update()
            
            # Check for ball-paddle collision
            if pygame.sprite.collide_rect(ball, paddle):
                ball.bounce()
            
            # Check for ball-brick collisions
            brick_hit = pygame.sprite.spritecollide(ball, bricks, True)
            if brick_hit:
                ball.bounce()
                score += 10
                if sound_enabled:
                    play_note(660, 0.1)  # Brick hit sound
            
            # Check for game over
            if ball.rect.y >= HEIGHT:
                lives -= 1
                if lives <= 0:
                    game_over = True
                    if sound_enabled:
                        play_note(220, 0.3)  # Game over sound
                else:
                    ball.rect.x = 345
                    ball.rect.y = 300
                    ball.velocity = [random.choice([-5, 4]), -4]
                    if sound_enabled:
                        play_note(330, 0.1)  # Life lost sound
            
            # Check for level completion
            if len(bricks) == 0:
                game_over = True
                if sound_enabled:
                    play_note(880, 0.5)  # Level complete sound
        
        # Drawing
        screen.fill(BLACK)
        all_sprites.draw(screen)
        
        # Display score and lives
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 120, 10))
        
        if game_over:
            if len(bricks) == 0:
                message = "Level Complete! Press SPACE to play again"
            else:
                message = "Game Over! Press SPACE to play again"
            game_over_text = font.render(message, True, WHITE)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()
