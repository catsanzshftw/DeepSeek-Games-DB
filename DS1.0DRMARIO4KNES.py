import pygame
import random
import sys

# Constants
GRID_SIZE = 30
GRID_COLS = 8
GRID_ROWS = 16
FPS = 60
COLORS = {
    'RED': (255, 0, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'GRAY': (128, 128, 128)
}

class Virus:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.active = True

    def draw(self, surface):
        if self.active:
            pygame.draw.circle(surface, self.color, 
                (self.x * GRID_SIZE + GRID_SIZE//2, self.y * GRID_SIZE + GRID_SIZE//2),
                GRID_SIZE//2 - 2)

class Capsule:
    ROTATIONS = {
        'horizontal': [(1, 0), (-1, 0)],
        'vertical': [(0, 1), (0, -1)],
        'diag_up': [(-1, 1), (1, -1)],
        'diag_down': [(1, 1), (-1, -1)]
    }

    def __init__(self, colors, start_pos):
        self.colors = colors
        self.pos = list(start_pos)
        self.rotation = 'horizontal'
        self.last_move = pygame.time.get_ticks()

    def draw(self, surface):
        base_x = self.pos[0] * GRID_SIZE
        base_y = self.pos[1] * GRID_SIZE
        offsets = self.ROTATIONS[self.rotation]
        
        # Draw first half
        pygame.draw.rect(surface, self.colors[0],
            (base_x, base_y, GRID_SIZE-2, GRID_SIZE-2))
        
        # Draw second half
        dx, dy = offsets[0]
        pygame.draw.rect(surface, self.colors[1],
            ((self.pos[0] + dx) * GRID_SIZE, 
             (self.pos[1] + dy) * GRID_SIZE, 
             GRID_SIZE-2, GRID_SIZE-2))

    def rotate(self, grid):
        original_rotation = self.rotation
        rotations = list(self.ROTATIONS.keys())
        new_index = (rotations.index(self.rotation) + 1) % len(rotations)
        self.rotation = rotations[new_index]
        
        if not self._valid_position(grid):
            self.rotation = original_rotation

    def _valid_position(self, grid):
        offsets = self.ROTATIONS[self.rotation]
        for dx, dy in offsets:
            x = self.pos[0] + dx
            y = self.pos[1] + dy
            if not (0 <= x < GRID_COLS and 0 <= y < GRID_ROWS):
                return False
            if grid[y][x] is not None:
                return False
        return True

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.grid = [[None for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.viruses = []
        self.score = 0
        self.level = 1
        self.init_level()
        self.current_capsule = None
        self.next_capsule = None
        self.game_over = False
        self.spawn_new_capsule()

    def init_level(self):
        virus_count = min(4 * self.level, GRID_COLS * GRID_ROWS // 4)
        colors = [COLORS['RED'], COLORS['BLUE'], COLORS['YELLOW']]
        
        for _ in range(virus_count):
            while True:
                x = random.randint(0, GRID_COLS-1)
                y = random.randint(GRID_ROWS//2, GRID_ROWS-1)
                color = random.choice(colors)
                if self.grid[y][x] is None:
                    self.viruses.append(Virus(x, y, color))
                    self.grid[y][x] = color
                    break
    def spawn_new_capsule(self):
        colors = [random.choice([COLORS['RED'], COLORS['BLUE'], COLORS['YELLOW']]),
                 random.choice([COLORS['RED'], COLORS['BLUE'], COLORS['YELLOW']])]
        
        if self.next_capsule:
            self.current_capsule = self.next_capsule
            self.current_capsule.pos = [GRID_COLS//2 - 1, 0]
        else:
            self.current_capsule = Capsule(colors, (GRID_COLS//2 - 1, 0))
        
        self.next_capsule = Capsule(
            [random.choice([COLORS['RED'], COLORS['BLUE'], COLORS['YELLOW']),
             random.choice([COLORS['RED'], COLORS['BLUE'], COLORS['YELLOW']])],
            (GRID_COLS//2 - 1, 0))
        
        if not self.valid_capsule_position():
            self.game_over = True

    def valid_capsule_position(self):
        return self.current_capsule._valid_position(self.grid)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        
        if now - self.current_capsule.last_move > 100:
            if keys[pygame.K_LEFT]:
                self.move_capsule(-1, 0)
            if keys[pygame.K_RIGHT]:
                self.move_capsule(1, 0)
            if keys[pygame.K_DOWN]:
                self.move_capsule(0, 1)
            self.current_capsule.last_move = now
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.current_capsule.rotate(self.grid)
                if event.key == pygame.K_SPACE:
                    self.hard_drop()

    def move_capsule(self, dx, dy):
        self.current_capsule.pos[0] += dx
        self.current_capsule.pos[1] += dy
        
        if not self.current_capsule._valid_position(self.grid):
            self.current_capsule.pos[0] -= dx
            self.current_capsule.pos[1] -= dy
            return False
        return True

    def hard_drop(self):
        while self.move_capsule(0, 1):
            pass
        self.lock_capsule()

    def lock_capsule(self):
        offsets = Capsule.ROTATIONS[self.current_capsule.rotation]
        color1, color2 = self.current_capsule.colors
        
        # Place capsule parts in grid
        x, y = self.current_capsule.pos
        self.grid[y][x] = color1
        for dx, dy in offsets:
            self.grid[y + dy][x + dx] = color2
        
        self.check_matches()
        self.spawn_new_capsule()

    def check_matches(self):
        visited = set()
        to_remove = set()

        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                if (x, y) not in visited and self.grid[y][x] is not None:
                    color = self.grid[y][x]
                    group = self.flood_fill(x, y, color)
                    if len(group) >= 4:
                        to_remove.update(group)
                    visited.update(group)

        # Remove matched pieces and viruses
        for x, y in to_remove:
            self.grid[y][x] = None
            self.viruses = [v for v in self.viruses if not (v.x == x and v.y == y)]
            self.score += 100

        # Drop pieces after removal
        self.apply_gravity()

    def flood_fill(self, x, y, color):
        stack = [(x, y)]
        visited = set()
        
        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS:
                    if self.grid[ny][nx] == color and (nx, ny) not in visited:
                        stack.append((nx, ny))
        return visited

    def apply_gravity(self):
        for x in range(GRID_COLS):
            column = [self.grid[y][x] for y in range(GRID_ROWS)]
            new_column = [cell for cell in column if cell is not None]
            new_column += [None] * (GRID_ROWS - len(new_column))
            for y in range(GRID_ROWS):
                self.grid[y][x] = new_column[y]

    def draw_grid(self):
        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, self.grid[y][x],
                                   (x * GRID_SIZE + 200, y * GRID_SIZE,
                                    GRID_SIZE-2, GRID_SIZE-2))
                else:
                    pygame.draw.rect(self.screen, COLORS['GRAY'],
                                   (x * GRID_SIZE + 200, y * GRID_SIZE,
                                    GRID_SIZE-2, GRID_SIZE-2), 1)

        for virus in self.viruses:
            virus.draw(self.screen)

    def draw_ui(self):
        # Score and Level
        score_text = self.font.render(f"Score: {self.score}", True, COLORS['WHITE'])
        level_text = self.font.render(f"Level: {self.level}", True, COLORS['WHITE'])
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(level_text, (20, 60))

        # Next capsule preview
        next_text = self.font.render("Next:", True, COLORS['WHITE'])
        self.screen.blit(next_text, (600, 20))
        if self.next_capsule:
            temp_pos = [3, 2]
            self.next_capsule.pos = temp_pos
            self.next_capsule.draw(self.screen)

        # Game over screen
        if self.game_over:
            overlay = pygame.Surface((800, 600))
            overlay.set_alpha(128)
            overlay.fill(COLORS['BLACK'])
            self.screen.blit(overlay, (0, 0))
            
            go_text = self.font.render("Game Over!", True, COLORS['RED'])
            restart_text = self.font.render("Press R to restart", True, COLORS['WHITE'])
            self.screen.blit(go_text, (400 - go_text.get_width()//2, 250))
            self.screen.blit(restart_text, (400 - restart_text.get_width()//2, 300))

    def run(self):
        while True:
            self.screen.fill(COLORS['BLACK'])
            self.handle_input()
            
            if not self.game_over:
                self.current_capsule.draw(self.screen)
                self.draw_grid()
                self.draw_ui()
                
                # Automatic falling
                if pygame.time.get_ticks() - self.current_capsule.last_move > 1000:
                    if not self.move_capsule(0, 1):
                        self.lock_capsule()
                    self.current_capsule.last_move = pygame.time.get_ticks()
                
                # Check level completion
                if not self.viruses:
                    self.level += 1
                    self.init_level()
            else:
                self.draw_ui()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.__init__()
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = GameEngine()
    game.run()
