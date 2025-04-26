import pygame
import sys
import math
from pygame.math import Vector2
import numpy as np

class AudioEngine:
    def __init__(self):
        self.sample_rate = 44100
        pygame.mixer.init(frequency=self.sample_rate, channels=2)
        self.channels = [pygame.mixer.Channel(i) for i in range(4)]
        
    def _generate_wave(self, wave_type, freq, duration=0.1, volume=0.2):
        sample_count = int(self.sample_rate * duration)
        t = np.linspace(0, duration, sample_count, False)
        
        if wave_type == 'square':
            wave = np.where(np.sin(2 * np.pi * freq * t) > 0, 1, -1)
        elif wave_type == 'saw':
            wave = 2 * (t * freq % 1) - 1
        else:  # sine
            wave = np.sin(2 * np.pi * freq * t)
            
        wave = (wave * 32767 * volume).astype(np.int16)
        # Convert to stereo (2 channels)
        stereo_wave = np.column_stack((wave, wave))
        return pygame.sndarray.make_sound(stereo_wave)

    def play_shoot(self):
        sound = self._generate_wave('square', 880, 0.1, 0.3)
        self.channels[0].play(sound)

    def play_explosion(self):
        sound = self._generate_wave('saw', 220, 0.3, 0.4)
        self.channels[1].play(sound)

    def play_move(self, speed_factor):
        freq = 80 + speed_factor * 40
        sound = self._generate_wave('sine', freq, 0.05, 0.2)
        self.channels[2].play(sound)

class Player:
    def __init__(self, audio):
        self.audio = audio
        self.pos = Vector2(300, 350)
        self.size = Vector2(40, 20)
        self.speed = 5
        self.color = (0, 255, 0)
        self.bullets = []
        self.fire_cooldown = 0
        self.last_move_time = 0

    def move(self, direction):
        self.pos.x += direction * self.speed
        self.pos.x = max(20, min(580, self.pos.x))
        
        # Throttle movement sounds
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > 100:
            self.audio.play_move(abs(direction))
            self.last_move_time = current_time

    def shoot(self):
        if self.fire_cooldown <= 0:
            self.bullets.append(Bullet(self.pos + Vector2(15, -10)))
            self.fire_cooldown = 30
            self.audio.play_shoot()
            return True
        return False

class Bullet:
    def __init__(self, pos):
        self.pos = Vector2(pos)
        self.size = Vector2(10, 20)
        self.speed = 7
        self.color = (255, 255, 0)

    def update(self):
        self.pos.y -= self.speed

class Enemy:
    def __init__(self, pos):
        self.pos = Vector2(pos)
        self.size = Vector2(30, 20)
        self.color = (255, 0, 0)
        self.direction = 1
        self.speed = 1

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 400))
        self.clock = pygame.time.Clock()
        self.audio = AudioEngine()
        self.player = Player(self.audio)
        self.enemies = []
        self.score = 0
        self.game_over = False
        self.init_enemies()

    def init_enemies(self):
        for y in range(5):
            for x in range(10):
                self.enemies.append(Enemy(Vector2(100 + x * 40, 50 + y * 30)))

    def run(self):
        while True:
            self.handle_input()
            if not self.game_over:
                self.update()
            self.draw()
            self.clock.tick(60)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and self.game_over:
                if event.key == pygame.K_r:
                    self.__init__()  # Reset game
                
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move(-1)
            if keys[pygame.K_RIGHT]:
                self.player.move(1)
            if keys[pygame.K_SPACE]:
                self.player.shoot()

    def update(self):
        # Update bullets
        self.player.fire_cooldown -= 1
        for bullet in self.player.bullets[:]:
            bullet.update()
            if bullet.pos.y < -20:
                self.player.bullets.remove(bullet)
                
        # Enemy movement logic
        move_down = False
        for enemy in self.enemies:
            enemy.pos.x += enemy.speed * enemy.direction
            if enemy.pos.x > 570 or enemy.pos.x < 30:
                move_down = True
            # Game over if enemies reach bottom
            if enemy.pos.y > 340:
                self.game_over = True
                
        if move_down:
            speed_factor = self.enemies[0].speed if self.enemies else 1
            self.audio.play_move(speed_factor)
            for enemy in self.enemies:
                enemy.direction *= -1
                enemy.pos.y += 20
                enemy.speed *= 1.05

        # Collision detection
        for bullet in self.player.bullets[:]:
            bullet_rect = pygame.Rect(bullet.pos, bullet.size)
            for enemy in self.enemies[:]:
                enemy_rect = pygame.Rect(enemy.pos, enemy.size)
                if bullet_rect.colliderect(enemy_rect):
                    self.audio.play_explosion()
                    self.player.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break

        # Win condition
        if not self.enemies:
            self.init_enemies()

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        # Draw player
        pygame.draw.rect(self.screen, self.player.color, 
                        (self.player.pos.x - 20, self.player.pos.y,
                         self.player.size.x, self.player.size.y))
        
        # Draw bullets
        for bullet in self.player.bullets:
            pygame.draw.rect(self.screen, bullet.color,
                            (bullet.pos.x, bullet.pos.y,
                             bullet.size.x, bullet.size.y))
        
        # Draw enemies
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, enemy.color,
                            (enemy.pos.x - 15, enemy.pos.y,
                             enemy.size.x, enemy.size.y))
        
        # Draw score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        
        if self.game_over:
            font = pygame.font.Font(None, 72)
            text = font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(text, (150, 150))
            font = pygame.font.Font(None, 36)
            text = font.render("Press R to restart", True, (255, 255, 255))
            self.screen.blit(text, (200, 230))
        
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
