import pygame
import random
import sys
import math
import numpy
from pygame.locals import *

# Constants
GRID_SIZE = 16
GRID_COLS = 8
GRID_ROWS = 16
FPS = 60
COLORS = {
    'RED': (228, 0, 0),
    'BLUE': (0, 84, 228),
    'YELLOW': (248, 252, 0),
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'GRAY': (96, 96, 96)
}

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.move_sound = self.generate_beep(440, 50)
        self.rotate_sound = self.generate_beep(660, 50)
        self.drop_sound = self.generate_beep(880, 50)
        self.clear_sound = self.generate_beep(220, 200)
        self.game_over_sound = self.generate_beep(110, 500)
        
        # Background music (simple loop)
        self.bg_music = self.generate_music()
        self.bg_channel = pygame.mixer.Channel(0)
        self.bg_channel.play(self.bg_music, loops=-1)

    def generate_beep(self, frequency, duration, volume=0.1):
        sample_rate = 44100
        n_samples = int(sample_rate * duration / 1000.0)
        buf = numpy.zeros((n_samples, 2), dtype=numpy.int16)
        for s in range(n_samples):
            t = float(s) / sample_rate
            buf[s][0] = int(32767.0 * volume * math.sin(2 * math.pi * frequency * t))
            buf[s][1] = int(32767.0 * volume * math.sin(2 * math.pi * frequency * t))
        return pygame.sndarray.make_sound(buf)

    def generate_music(self):
        melody = [
            (330, 200), (392, 200), (440, 200), (523, 400),
            (440, 200), (523, 200), (587, 400), (523, 400)
        ]
        samples = []
        for note in melody * 2:  # Repeat melody twice
            freq, duration = note
            n_samples = int(44100 * duration / 1000.0)
            for s in range(n_samples):
                t = float(s) / 44100
                sample = int(32767.0 * 0.1 * math.sin(2 * math.pi * freq * t))
                samples.append((sample, sample))
        return pygame.sndarray.make_sound(numpy.array(samples, dtype=numpy.int16))

    def play_move(self):
        pygame.mixer.find_channel(True).play(self.move_sound)

    def play_rotate(self):
        pygame.mixer.find_channel(True).play(self.rotate_sound)

    def play_drop(self):
        pygame.mixer.find_channel(True).play(self.drop_sound)

    def play_clear(self):
        pygame.mixer.find_channel(True).play(self.clear_sound)

    def play_game_over(self):
        self.bg_channel.stop()
        pygame.mixer.find_channel(True).play(self.game_over_sound)

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
    ROTATIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Right, Down, Left, Up

    def __init__(self, colors, start_pos):
        self.colors = colors
        self.pos = list(start_pos)
        self.rotation = 0
        self.last_move = pygame.time.get_ticks()

    def draw(self, surface):
        # Primary block
        x0 = self.pos[0] * GRID_SIZE
        y0 = self.pos[1] * GRID_SIZE
        pygame.draw.rect(surface, self.colors[0], (x0 + 1, y0 + 1, GRID_SIZE - 2, GRID_SIZE - 2))
        # Secondary block
        dx, dy = self.ROTATIONS[self.rotation]
        x1 = (self.pos[0] + dx) * GRID_SIZE
        y1 = (self.pos[1] + dy) * GRID_SIZE
        pygame.draw.rect(surface, self.colors[1], (x1 + 1, y1 + 1, GRID_SIZE - 2, GRID_SIZE - 2))

    def rotate(self, grid):
        original_rotation = self.rotation
        self.rotation = (self.rotation + 1) % 4
        if not self._valid_position(grid):
            self.rotation = original_rotation

    def _valid_position(self, grid):
        x0, y0 = self.pos
        if not (0 <= x0 < GRID_COLS and 0 <= y0 < GRID_ROWS) or grid[y0][x0] is not None:
            return False
        dx, dy = self.ROTATIONS[self.rotation]
        x1, y1 = x0 + dx, y0 + dy
        if not (0 <= x1 < GRID_COLS and 0 <= y1 < GRID_ROWS) or grid[y1][x1] is not None:
            return False
        return True

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((256, 240))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 16)
        self.grid = [[None for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.viruses = []
        self.score = 0
        self.level = 1
        self.sound_manager = SoundManager()
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
                if self.grid[y][x] is None:
                    virus = Virus(x, y, random.choice(colors))
                    self.viruses.append(virus)
                    self.grid[y][x] = virus.color
                    break

    def spawn_new_capsule(self):
        colors = [random.choice(list(COLORS.values())[:3]), random.choice(list(COLORS.values())[:3])]
        start_pos = (GRID_COLS//2 - 1, 0)
        if self.next_capsule:
            self.current_capsule = self.next_capsule
            self.current_capsule.pos = list(start_pos)
            self.current_capsule.rotation = 0
        else:
            self.current_capsule = Capsule(colors, start_pos)
        self.next_capsule = Capsule(
            [random.choice(list(COLORS.values())[:3]), random.choice(list(COLORS.values())[:3])],
            start_pos
        )
        if not self.current_capsule._valid_position(self.grid):
            self.game_over = True
            self.sound_manager.play_game_over()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        move_interval = 100

        if keys[pygame.K_LEFT] and now - self.current_capsule.last_move > move_interval:
            if self.move_capsule(-1, 0):
                self.sound_manager.play_move()
            self.current_capsule.last_move = now
        if keys[pygame.K_RIGHT] and now - self.current_capsule.last_move > move_interval:
            if self.move_capsule(1, 0):
                self.sound_manager.play_move()
            self.current_capsule.last_move = now
        if keys[pygame.K_DOWN] and now - self.current_capsule.last_move > move_interval:
            if self.move_capsule(0, 1):
                self.sound_manager.play_move()
            self.current_capsule.last_move = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.current_capsule.rotate(self.grid)
                    self.sound_manager.play_rotate()
                if event.key == pygame.K_SPACE:
                    self.hard_drop()
                if event.key == pygame.K_r and self.game_over:
                    self.__init__()

    def move_capsule(self, dx, dy):
        self.current_capsule.pos[0] += dx
        self.current_capsule.pos[1] += dy
        if not self.current_capsule._valid_position(self.grid):
            self.current_capsule.pos[0] -= dx
            self.current_capsule.pos[1] -= dy
            return False
        return True

    def hard_drop(self):
        self.sound_manager.play_drop()
        while self.move_capsule(0, 1):
            pass
        self.lock_capsule()

    def lock_capsule(self):
        x, y = self.current_capsule.pos
        dx, dy = Capsule.ROTATIONS[self.current_capsule.rotation]
        self.grid[y][x] = self.current_capsule.colors[0]
        self.grid[y + dy][x + dx] = self.current_capsule.colors[1]
        self.check_matches()
        self.spawn_new_capsule()

    def check_matches(self):
        visited = set()
        to_remove = set()
        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                if (x, y) in visited or self.grid[y][x] is None:
                    continue
                group = self.flood_fill(x, y, self.grid[y][x])
                if len(group) >= 4:
                    to_remove.update(group)
                visited.update(group)
        # Remove matched pieces
        if to_remove:
            self.sound_manager.play_clear()
            for x, y in to_remove:
                self.grid[y][x] = None
                self.viruses = [v for v in self.viruses if not (v.x == x and v.y == y)]
                self.score += 100
            self.apply_gravity()
            if not self.viruses:
                self.level += 1
                self.init_level()

    def flood_fill(self, x, y, color):
        stack = [(x, y)]
        visited = set()
        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS and self.grid[ny][nx] == color:
                    stack.append((nx, ny))
        return visited

    def apply_gravity(self):
        for x in range(GRID_COLS):
            col = []
            for y in range(GRID_ROWS):
                if self.grid[y][x] is not None:
                    col.append(self.grid[y][x])
            col += [None] * (GRID_ROWS - len(col))
            for y in range(GRID_ROWS):
                self.grid[y][x] = col[y]

    def draw_grid(self):
        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                rect = (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE-2, GRID_SIZE-2)
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, self.grid[y][x], rect)
                else:
                    pygame.draw.rect(self.screen, COLORS['GRAY'], rect, 1)
        for virus in self.viruses:
            virus.draw(self.screen)

    def draw_ui(self):
        # Score and Level
        score_text = self.font.render(f"SCORE: {self.score}", True, COLORS['WHITE'])
        level_text = self.font.render(f"LEVEL: {self.level}", True, COLORS['WHITE'])
        self.screen.blit(score_text, (140, 20))
        self.screen.blit(level_text, (140, 40))

        # Next capsule preview
        next_text = self.font.render("NEXT", True, COLORS['WHITE'])
        self.screen.blit(next_text, (140, 80))
        if self.next_capsule:
            preview_x, preview_y = 140, 100
            primary_rect = (preview_x + 1, preview_y + 1, GRID_SIZE-2, GRID_SIZE-2)
            secondary_rect = (preview_x + GRID_SIZE + 1, preview_y + 1, GRID_SIZE-2, GRID_SIZE-2)
            pygame.draw.rect(self.screen, self.next_capsule.colors[0], primary_rect)
            pygame.draw.rect(self.screen, self.next_capsule.colors[1], secondary_rect)

        # Game Over
        if self.game_over:
            go_text = self.font.render("GAME OVER", True, COLORS['RED'])
            restart_text = self.font.render("PRESS R", True, COLORS['WHITE'])
            self.screen.blit(go_text, (80, 100))
            self.screen.blit(restart_text, (88, 120))

    def run(self):
        while True:
            self.screen.fill(COLORS['BLACK'])
            self.handle_input()
            if not self.game_over:
                self.draw_grid()
                self.current_capsule.draw(self.screen)
                # Auto-fall
                fall_speed = max(50, 1000 - (self.level - 1) * 100)
                if pygame.time.get_ticks() - self.current_capsule.last_move > fall_speed:
                    if not self.move_capsule(0, 1):
                        self.lock_capsule()
                    self.current_capsule.last_move = pygame.time.get_ticks()
                self.draw_ui()
            else:
                self.draw_ui()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = GameEngine()
    game.run()
