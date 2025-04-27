import pygame
import random

# Constants (FIX 1: Add missing constants)
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
FPS = 30
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

class Pill:
    def __init__(self, color1, color2):  # FIX 2: Add position initialization
        self.color1 = color1
        self.color2 = color2
        self.x = GRID_WIDTH // 2 - 1
        self.y = 0
        self.orientation = "horizontal"
        
    def draw(self, screen):  # FIX 3: Add proper drawing logic
        x_pos = self.x * GRID_SIZE
        y_pos = self.y * GRID_SIZE
        if self.orientation == "horizontal":
            pygame.draw.rect(screen, self.color1, (x_pos, y_pos, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.color2, (x_pos + GRID_SIZE, y_pos, GRID_SIZE, GRID_SIZE))
        else:
            pygame.draw.rect(screen, self.color1, (x_pos, y_pos, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.color2, (x_pos, y_pos + GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def move_left(self, grid):  # FIX 4: Add boundary checks
        if self.x > 0:
            if self.orientation == "horizontal" and self.x > 0:
                if grid[self.y][self.x-1] is None:
                    self.x -= 1
            elif self.orientation == "vertical" and self.x > 0:
                if grid[self.y][self.x-1] is None and grid[self.y+1][self.x-1] is None:
                    self.x -= 1

    def move_right(self, grid):  # FIX 5: Add boundary checks
        max_x = GRID_WIDTH - (2 if self.orientation == "horizontal" else 1)
        if self.x < max_x:
            if self.orientation == "horizontal" and self.x < GRID_WIDTH-2:
                if grid[self.y][self.x+2] is None:
                    self.x += 1
            elif self.orientation == "vertical" and self.x < GRID_WIDTH-1:
                if grid[self.y][self.x+1] is None and grid[self.y+1][self.x+1] is None:
                    self.x += 1

    def rotate(self, grid):  # FIX 6: Add rotation validation
        new_orientation = "vertical" if self.orientation == "horizontal" else "horizontal"
        if self._validate_rotation(new_orientation, grid):
            self.orientation = new_orientation

    def _validate_rotation(self, new_orientation, grid):  # FIX 7: Add rotation collision check
        if new_orientation == "vertical":
            if self.y >= GRID_HEIGHT-2 or grid[self.y+1][self.x] is not None:
                return False
        else:
            if self.x >= GRID_WIDTH-1 or grid[self.y][self.x+1] is not None:
                return False
        return True

    def fall(self, grid):  # FIX 8: Add proper fall validation
        if self._can_fall(grid):
            self.y += 1
            return True
        return False

    def _can_fall(self, grid):  # FIX 9: Comprehensive fall check
        if self.orientation == "horizontal":
            if self.y >= GRID_HEIGHT-1:
                return False
            return grid[self.y+1][self.x] is None and grid[self.y+1][self.x+1] is None
        else:
            if self.y >= GRID_HEIGHT-2:
                return False
            return grid[self.y+2][self.x] is None

    def place_in_grid(self, grid):  # FIX 10: Add bounds checking
        if self.orientation == "horizontal":
            if self.x+1 < GRID_WIDTH and self.y < GRID_HEIGHT:
                grid[self.y][self.x] = self.color1
                grid[self.y][self.x+1] = self.color2
        else:
            if self.y+1 < GRID_HEIGHT:
                grid[self.y][self.x] = self.color1
                grid[self.y+1][self.x] = self.color2

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GRID_WIDTH*GRID_SIZE, GRID_HEIGHT*GRID_SIZE))
        self.clock = pygame.time.Clock()
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]  # FIX 11: Initialize grid properly
        self.new_pill()
        
    def new_pill(self):  # FIX 12: Add spawn validation
        self.pill = Pill(random.choice([RED, BLUE, YELLOW]), random.choice([RED, BLUE, YELLOW]))
        # Check game over condition
        if not self._validate_position():
            print("Game Over!")
            pygame.quit()
            exit()

    def _validate_position(self):  # FIX 13: Spawn position validation
        if self.pill.orientation == "horizontal":
            return self.grid[0][GRID_WIDTH//2-1] is None and self.grid[0][GRID_WIDTH//2] is None
        else:
            return self.grid[0][GRID_WIDTH//2-1] is None and self.grid[1][GRID_WIDTH//2-1] is None

    def draw_grid(self):  # FIX 14: Fix grid drawing coordinates
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] is not None:
                    pygame.draw.rect(self.screen, self.grid[y][x], 
                                   (x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1))
                else:
                    pygame.draw.rect(self.screen, GRAY, 
                                   (x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1), 1)

    def check_collision(self):  # FIX 15: Proper collision detection
        if not self.pill.fall(self.grid):
            self.pill.place_in_grid(self.grid)
            self._clear_lines()  # FIX 16: Add line clearing
            self.new_pill()

    def _clear_lines(self):  # FIX 17: Line clearing logic
        full_lines = []
        for y in range(GRID_HEIGHT):
            if all(cell is not None for cell in self.grid[y]):
                full_lines.append(y)
        
        for y in full_lines:
            del self.grid[y]
            self.grid.insert(0, [None for _ in range(GRID_WIDTH)])

    def main_loop(self):
        fall_time = 0
        fall_speed = 1000  # ms
        running = True
        
        while running:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.pill.move_left(self.grid)
                    elif event.key == pygame.K_RIGHT:
                        self.pill.move_right(self.grid)
                    elif event.key == pygame.K_UP:
                        self.pill.rotate(self.grid)
                    elif event.key == pygame.K_DOWN:
                        while self.pill.fall(self.grid):  # FIX 18: Proper hard drop
                            pass
            
            # Automatic falling
            if current_time - fall_time > fall_speed:
                self.check_collision()
                fall_time = current_time
            
            self.screen.fill(BLACK)
            self.draw_grid()
            self.pill.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.main_loop()
