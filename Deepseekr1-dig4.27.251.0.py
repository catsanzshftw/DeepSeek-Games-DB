import pygame
import random
import array

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dig Dug Clone")
clock = pygame.time.Clock()

# Sound generation function
def generate_beep(frequency=440, duration=0.1, volume=0.5):
    sample_rate = 44100
    sample_length = int(sample_rate * duration)
    period = sample_rate // frequency
    samples = array.array('h')
    max_val = int(32767 * volume)
    
    for i in range(sample_length):
        value = max_val if (i % period) < (period // 2) else -max_val
        samples.append(value)
    
    return pygame.mixer.Sound(buffer=samples.tobytes())

# Create game sounds
dig_sound = generate_beep(880, 0.05)
death_sound = generate_beep(220, 0.5)
restart_sound = generate_beep(660, 0.1)

# Game constants
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 30  # Reduced FPS to 30

# Colors
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Game state
class GameState:
    def __init__(self):
        self.grid = []
        self.player_pos = [0, 0]
        self.enemies = []
        self.dig_particles = []
        self.score = 0
        self.game_over = False
        self.player_move_cooldown = 0  # Player movement cooldown
        self.enemy_move_cooldown = 0   # Enemy movement cooldown
        self.init_game()
        
    def init_game(self):
        self.grid = [[1 if random.random() < 0.9 else 0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.player_pos = [GRID_WIDTH//2, GRID_HEIGHT//2]
        self.grid[self.player_pos[1]][self.player_pos[0]] = 0
        self.dig_particles = []
        self.score = 0
        self.game_over = False
        self.player_move_cooldown = 0
        self.enemy_move_cooldown = 0
        
        # Generate enemies in valid positions
        self.enemies = []
        while len(self.enemies) < 3:
            x = random.randint(0, GRID_WIDTH-1)
            y = random.randint(0, GRID_HEIGHT-1)
            if self.grid[y][x] == 0 and (x, y) != tuple(self.player_pos):
                self.enemies.append([x, y])

def move_towards(target, current, grid, enemies):
    tx, ty = target
    cx, cy = current
    dx, dy = 0, 0
    
    # Calculate preferred direction
    if abs(tx - cx) > abs(ty - cy):
        dx = 1 if tx > cx else -1
    else:
        dy = 1 if ty > cy else -1
    
    # Try primary direction
    new_x = cx + dx
    new_y = cy + dy
    if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
        if grid[new_y][new_x] == 0 and not any(e == [new_x, new_y] for e in enemies):
            return [new_x, new_y]
    
    # Try secondary directions
    directions = []
    if dx != 0:
        directions = [(0, 1), (0, -1), (-dx, 0)]
    else:
        directions = [(1, 0), (-1, 0), (0, -dy)]
    
    for d in directions:
        new_x = cx + d[0]
        new_y = cy + d[1]
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            if grid[new_y][new_x] == 0 and not any(e == [new_x, new_y] for e in enemies):
                return [new_x, new_y]
    
    # Fallback to current position if no moves
    return current

# Initialize game state
state = GameState()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and state.game_over:
            if event.key == pygame.K_r:
                restart_sound.play()
                state.init_game()

    # Game logic
    if not state.game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        move_vec = (0, 0)
        if keys[pygame.K_LEFT]: move_vec = (-1, 0)
        elif keys[pygame.K_RIGHT]: move_vec = (1, 0)
        elif keys[pygame.K_UP]: move_vec = (0, -1)
        elif keys[pygame.K_DOWN]: move_vec = (0, 1)
        
        if move_vec != (0, 0) and state.player_move_cooldown <= 0:
            new_x = state.player_pos[0] + move_vec[0]
            new_y = state.player_pos[1] + move_vec[1]
            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                if state.grid[new_y][new_x] == 1:
                    state.grid[new_y][new_x] = 0
                    state.dig_particles.append([
                        new_x * CELL_SIZE + CELL_SIZE//2,
                        new_y * CELL_SIZE + CELL_SIZE//2,
                        random.randint(5, 10)
                    ])
                    dig_sound.play()
                    state.score += 10
                state.player_pos = [new_x, new_y]
                # Set cooldown after moving
                state.player_move_cooldown = 10  # Adjust this value to change player speed
        
        # Update cooldowns
        if state.player_move_cooldown > 0:
            state.player_move_cooldown -= 1
        
        # Update particles
        state.dig_particles = [[x, y, s-0.2] for x, y, s in state.dig_particles if s > 0.2]
        
        # Enemy movement
        if state.enemy_move_cooldown <= 0:
            for i, enemy in enumerate(state.enemies):
                new_pos = move_towards(state.player_pos, enemy, state.grid, state.enemies)
                state.enemies[i] = new_pos
                
                # Collision check
                if abs(enemy[0] - state.player_pos[0]) < 1 and abs(enemy[1] - state.player_pos[1]) < 1:
                    death_sound.play()
                    state.game_over = True
            # Set enemy cooldown after movement
            state.enemy_move_cooldown = 15  # Adjust this value to change enemy speed
        else:
            state.enemy_move_cooldown -= 1

    # Rendering (unchanged)
    screen.fill(BLACK)
    
    # Draw grid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if state.grid[y][x]:
                pygame.draw.rect(screen, BROWN, 
                               (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
    
    # Draw particles
    for x, y, s in state.dig_particles:
        pygame.draw.circle(screen, BROWN, (x, y), int(s))
    
    # Draw player
    pygame.draw.circle(screen, ORANGE,
                      (state.player_pos[0]*CELL_SIZE + CELL_SIZE//2,
                       state.player_pos[1]*CELL_SIZE + CELL_SIZE//2),
                      CELL_SIZE//2 - 2)
    
    # Draw enemies
    for x, y in state.enemies:
        pygame.draw.circle(screen, RED,
                          (x*CELL_SIZE + CELL_SIZE//2,
                           y*CELL_SIZE + CELL_SIZE//2),
                          CELL_SIZE//2 - 2)
    
    # Draw UI
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {state.score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    if state.game_over:
        font = pygame.font.Font(None, 72)
        go_text = font.render("Game Over!", True, RED)
        screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT//2 - 40))
        restart_text = font.render("Press R to restart", True, WHITE)
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
