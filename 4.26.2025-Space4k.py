import pygame
import sys
from pygame.math import Vector2

class Player:
    def __init__(self):
        self.pos = Vector2(300, 350)
        self.size = Vector2(40, 20)
        self.speed = 5
        self.color = (0, 255, 0)
        self.bullets = []
        self.fire_cooldown = 0

    def move(self, direction):
        self.pos.x += direction * self.speed
        self.pos.x = max(20, min(580, self.pos.x))

    def shoot(self):
        if self.fire_cooldown <= 0:
            self.bullets.append(Bullet(self.pos + Vector2(15, -10)))
            self.fire_cooldown = 30

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
        self.player = Player()
        self.enemies = []
        self.score = 0
        
        # Create enemy grid
        for y in range(5):
            for x in range(10):
                self.enemies.append(Enemy(Vector2(100 + x * 40, 50 + y * 30)))

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
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
                
        # Update enemies
        move_down = False
        for enemy in self.enemies:
            enemy.pos.x += enemy.speed * enemy.direction
            if enemy.pos.x > 570 or enemy.pos.x < 30:
                move_down = True
                
        if move_down:
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
                    self.player.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break

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
        
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
