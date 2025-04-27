# snake_test.py
# Meow! A simple Snake game using Pygame with NES-like speed! Nyaa~

import pygame
import random
import sys
import numpy as np

# --- Constants ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SNAKE_BLOCK_SIZE = 20
FPS = 60  # Keep rendering at 60 FPS
MOVES_PER_SECOND = 8  # NES-like movement speed (adjust between 6-10 for authentic feel)

# --- Initialization ---
pygame.init()
pygame.mixer.init()

def make_beep(frequency=880, duration_ms=80, volume=0.5):
    """Generate a beep sound (sine wave)"""
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, n_samples, False)
    wave = np.sin(2 * np.pi * frequency * t)
    audio = (wave * 32767 * volume).astype(np.int16)
    stereo_audio = np.column_stack((audio, audio))
    sound = pygame.sndarray.make_sound(stereo_audio)
    return sound

beep_sound = make_beep()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game! (NES Speed)")
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("comicsansms", 35)
score_font = pygame.font.SysFont("comicsansms", 25)

# --- Helper Functions ---
def draw_snake(snake_block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block_size, snake_block_size])

def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3 + y_displace])

def show_score(score):
    value = score_font.render("Score: " + str(score), True, BLUE)
    screen.blit(value, [10, 10])

# --- Game Loop ---
def game_loop():
    game_over = False
    game_close = False
    
    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2
    x1_change = 0
    y1_change = 0
    
    snake_list = []
    length_of_snake = 1
    
    foodx = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
    foody = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
    
    # Timing variables for NES-like movement
    move_delay = 1000 / MOVES_PER_SECOND  # milliseconds between moves
    last_move_time = pygame.time.get_ticks()
    
    while not game_over:
        
        while game_close:
            screen.fill(BLACK)
            message("Game Over! Press Q-Quit or C-Play Again", RED)
            show_score(length_of_snake - 1)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
        
        current_time = pygame.time.get_ticks()
        
        # Handle input every frame for responsiveness
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_BLOCK_SIZE
                    x1_change = 0
        
        # Only move the snake at the NES-like interval
        if current_time - last_move_time >= move_delay:
            last_move_time = current_time
            
            # Update snake position
            x1 += x1_change
            y1 += y1_change
            
            # Boundary check
            if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
                game_close = True
                beep_sound.play()
            
            # Snake body updates
            snake_head = [x1, y1]
            snake_list.append(snake_head)
            
            if len(snake_list) > length_of_snake:
                del snake_list[0]
            
            # Self-collision check
            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True
                    beep_sound.play()
            
            # Food collision
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, SCREEN_WIDTH - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
                foody = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_BLOCK_SIZE) / SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
                length_of_snake += 1
                beep_sound.play()
        
        # Always render at 60 FPS for smooth display
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, [foodx, foody, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])
        draw_snake(SNAKE_BLOCK_SIZE, snake_list)
        show_score(length_of_snake - 1)
        pygame.display.update()
        
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
