import asyncio
import pygame
import random
from pygame import Vector2

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRAVITY = 1500
JUMP_FORCE = -650
PLAYER_SPEED = 300
WORLD_COLORS = [
    (135, 206, 235),  # World 1: Sky Blue
    (100, 149, 237),  # World 2: Cornflower Blue
    (233, 150, 122),  # World 3: Dark Salmon
    (152, 251, 152),  # World 4: Pale Green
    (221, 160, 221)   # World 5: Plum
]
PLATFORM_COLORS = [
    (139, 69, 19),    # World 1
    (70, 130, 180),   # World 2
    (210, 180, 140),  # World 3
    (107, 142, 35),   # World 4
    (139, 0, 139)     # World 5
]

class GameState:
    RUNNING, PAUSED, GAME_OVER = range(3)

class PlayerState:
    SMALL, BIG, FIRE = range(3)

class Entity:
    def __init__(self, pos, size):
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.size = Vector2(size)
        self.color = (255, 0, 0)
        self.on_ground = False

    def get_rect(self):
        return pygame.Rect(self.pos, self.size)

class Player(Entity):
    def __init__(self, pos):
        super().__init__(pos, (32, 32))
        self.state = PlayerState.SMALL
        self.invincible = False
        self.can_shoot = False
        self.lives = 3
        self.score = 0
        self.coins = 0

    def jump(self):
        if self.on_ground:
            self.vel.y = JUMP_FORCE
            self.on_ground = False

    def update(self, dt, platforms, enemies):
        self.pos.x += self.vel.x * dt
        self.vel.y += GRAVITY * dt
        self.pos.y += self.vel.y * dt
        self.on_ground = False
        self.resolve_collisions(platforms, enemies)

    def resolve_collisions(self, platforms, enemies):
        player_rect = self.get_rect()
        for plat in platforms:
            if player_rect.colliderect(plat.get_rect()):
                if self.vel.y > 0:
                    self.pos.y = plat.pos.y - self.size.y
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.pos.y = plat.pos.y + plat.size.y
                    self.vel.y = 0
        for enemy in enemies:
            if player_rect.colliderect(enemy.get_rect()):
                if self.vel.y > 0:
                    enemy.stomp()
                    self.vel.y = JUMP_FORCE * 0.8
                else:
                    self.take_damage()

    def take_damage(self):
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            pygame.time.set_timer(pygame.USEREVENT, 2000)

class Block(Entity):
    def __init__(self, pos, content=None, world_num=0):
        super().__init__(pos, (32, 32))
        self.content = content
        self.bumped = False
        self.set_color(world_num)

    def set_color(self, world_num):
        if self.content:
            self.color = (139, 69, 19)
        else:
            self.color = PLATFORM_COLORS[world_num]

    def bump(self):
        if not self.bumped and self.content:
            self.bumped = True
            return self.content
        return None

class Goomba(Entity):
    def __init__(self, pos):
        super().__init__(pos, (32, 24))
        self.color = (165, 42, 42)
        self.direction = 1
        self.speed = 100

    def update(self, dt, platforms):
        self.pos.x += self.direction * self.speed * dt
        front_pos = self.pos.x + (self.size.x * self.direction)
        if not any(p.get_rect().collidepoint(front_pos, self.pos.y + 1) for p in platforms):
            self.direction *= -1
        self.vel.y += GRAVITY * dt
        self.pos.y += self.vel.y * dt
        for plat in platforms:
            if self.get_rect().colliderect(plat.get_rect()):
                if self.vel.y > 0:
                    self.pos.y = plat.pos.y - self.size.y
                    self.vel.y = 0

    def stomp(self):
        pass

class Flagpole(Entity):
    def __init__(self, pos):
        super().__init__(pos, (16, 256))
        self.color = (255, 255, 0)

class Level:
    def __init__(self, platform_data, enemy_data, start_pos, end_pos):
        self.platform_data = platform_data
        self.enemy_data = enemy_data
        self.start_pos = start_pos
        self.end_pos = end_pos

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = GameState.RUNNING
        self.worlds = self.create_worlds()
        self.current_world = 0
        self.current_level = 0
        self.player = Player((0, 0))
        self.load_current_level()

    def create_worlds(self):
        worlds = []
        for w in range(5):
            levels = []
            for l in range(4):
                platform_data = []
                enemy_data = []
                # Base platform
                for i in range(25):
                    platform_data.append((i*32, SCREEN_HEIGHT-32, None))
                # Variable platforms
                for _ in range(l+1):
                    x = random.randint(200, 600)
                    y = SCREEN_HEIGHT - 200 - (l*100)
                    platform_data.append((x, y, None))
                # Enemies
                for _ in range(l):
                    x = random.randint(300, 700)
                    enemy_data.append((x, SCREEN_HEIGHT-64-24, 'goomba'))
                # Level setup
                levels.append(Level(
                    platform_data,
                    enemy_data,
                    (100, SCREEN_HEIGHT-64),
                    (25*32-100, SCREEN_HEIGHT-64)
                ))
            worlds.append(levels)
        return worlds

    def load_current_level(self):
        level_data = self.worlds[self.current_world][self.current_level]
        self.platforms = [Block(Vector2(x, y), content, self.current_world) 
                         for x, y, content in level_data.platform_data]
        self.enemies = [Goomba(Vector2(x, y)) for x, y, _ in level_data.enemy_data]
        self.flagpole = Flagpole(Vector2(level_data.end_pos))
        self.player.pos = Vector2(level_data.start_pos)
        self.player.vel = Vector2(0, 0)
        self.camera_x = 0

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        self.player.vel.x = 0
        if keys[pygame.K_LEFT]:
            self.player.vel.x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.player.vel.x = PLAYER_SPEED
        if keys[pygame.K_SPACE]:
            self.player.jump()

    def update(self, dt):
        if self.state != GameState.RUNNING:
            return
        self.player.update(dt, self.platforms, self.enemies)
        for enemy in self.enemies:
            enemy.update(dt, self.platforms)
        if self.player.get_rect().colliderect(self.flagpole.get_rect()):
            self.level_complete()
        if self.player.pos.y > SCREEN_HEIGHT:
            self.handle_fall()
        self.camera_x = max(0, self.player.pos.x - SCREEN_WIDTH//2)

    def level_complete(self):
        self.current_level += 1
        if self.current_level >= 4:
            self.current_world += 1
            self.current_level = 0
            if self.current_world >= 5:
                self.state = GameState.GAME_OVER
                return
        self.load_current_level()

    def handle_fall(self):
        self.player.lives -= 1
        if self.player.lives <= 0:
            self.state = GameState.GAME_OVER
        else:
            self.load_current_level()

    def draw(self):
        self.screen.fill(WORLD_COLORS[self.current_world])
        for plat in self.platforms:
            rect = plat.get_rect().move(-self.camera_x, 0)
            pygame.draw.rect(self.screen, plat.color, rect)
        for enemy in self.enemies:
            rect = enemy.get_rect().move(-self.camera_x, 0)
            pygame.draw.ellipse(self.screen, enemy.color, rect)
        pygame.draw.rect(self.screen, self.flagpole.color, 
                        self.flagpole.get_rect().move(-self.camera_x, 0))
        player_rect = self.player.get_rect().move(-self.camera_x, 0)
        pygame.draw.rect(self.screen, self.player.color, player_rect)
        self.draw_hud()
        if self.state == GameState.GAME_OVER:
            self.draw_game_over()
        pygame.display.flip()

    def draw_hud(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"World {self.current_world+1}-{self.current_level+1} Lives: {self.player.lives}", 
                          True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def draw_game_over(self):
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER" if self.current_world < 5 else "YOU WIN!", 
                          True, (255, 0, 0))
        self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 
                               SCREEN_HEIGHT//2 - text.get_height()//2))

    async def run(self):
        while True:
            dt = self.clock.tick(60)/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            self.handle_input(dt)
            self.update(dt)
            self.draw()
            await asyncio.sleep(0)

if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())
