import pygame
import sys
import random

# SMB3 GBA Palette
PALETTE = {
    'sky_blue': (135, 206, 235),
    'grass_green': (34, 139, 34),
    'path_brown': (139, 69, 19),
    'mountain_gray': (192, 192, 192),
    'mario_red': (205, 0, 0),
    'castle_gray': (112, 128, 144),
    'cloud_white': (245, 245, 220),
    'highlight_yellow': (255, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255)
}

# World 1 node positions (GBA layout)
WORLD_1_NODE_POSITIONS = [
    (100, 300),  # Start
    (250, 300),  # 1-1
    (400, 300),  # 1-2
    (550, 300),  # 1-3
    (700, 300),  # Castle
]

# Simplified level types based on SMB3
LEVEL_TYPES = {
    '1-1': {
        'theme': 'grassland',
        'length': 'short',
        'difficulty': 'easy',
        'features': ['basic_platforms', 'goombas', 'pipes']
    },
    '1-2': {
        'theme': 'underground',
        'length': 'medium',
        'difficulty': 'easy',
        'features': ['pipes', 'bricks', 'koopas']
    },
    '1-3': {
        'theme': 'sky',
        'length': 'long',
        'difficulty': 'medium',
        'features': ['clouds', 'platforms', 'piranha_plants']
    },
    'castle': {
        'theme': 'castle',
        'length': 'long',
        'difficulty': 'hard',
        'features': ['lava', 'fire_bars', 'bowser']
    }
}

class Node:
    def __init__(self, x, y, node_type, level_id):
        self.x = x
        self.y = y
        self.type = node_type  # 'start', 'level', 'castle'
        self.level_id = level_id
        self.rect = pygame.Rect(x, y, 30, 30)
        
    def draw(self, surface):
        if self.type == 'castle':
            color = PALETTE['castle_gray']
        else:
            color = PALETTE['grass_green']
        pygame.draw.rect(surface, color, self.rect)
        
        # Draw level ID if it's a level
        if self.type == 'level':
            font = pygame.font.Font(None, 20)
            text = font.render(self.level_id, True, PALETTE['white'])
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

class WorldMap:
    def __init__(self):
        self.nodes = [
            Node(100, 300, 'start', 'Start'),
            Node(250, 300, 'level', '1-1'),
            Node(400, 300, 'level', '1-2'),
            Node(550, 300, 'level', '1-3'),
            Node(700, 300, 'castle', 'Castle')
        ]
        self.paths = [(0, 1), (1, 2), (2, 3), (3, 4)]
        self.background = self.create_background()
        
    def create_background(self):
        surface = pygame.Surface((800, 600))
        surface.fill(PALETTE['sky_blue'])
        
        # Draw paths
        for start_idx, end_idx in self.paths:
            start = self.nodes[start_idx]
            end = self.nodes[end_idx]
            pygame.draw.line(surface, PALETTE['path_brown'],
                           (start.rect.centerx, start.rect.centery),
                           (end.rect.centerx, end.rect.centery), 5)
        
        # Draw nodes
        for node in self.nodes:
            node.draw(surface)
            
        return surface
    
    def get_node_at_pos(self, pos):
        for node in self.nodes:
            if node.rect.collidepoint(pos):
                return node
        return None

class Player:
    def __init__(self):
        self.size = 30
        self.reset_position()
        
    def reset_position(self):
        self.x = 100
        self.y = 300
        self.target_node = 0
        self.moving = False
        self.move_progress = 0.0
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self, world, keys):
        if not self.moving:
            direction = 0
            if keys[pygame.K_RIGHT] and self.target_node < len(world.nodes) - 1:
                direction = 1
            elif keys[pygame.K_LEFT] and self.target_node > 0:
                direction = -1
                
            if direction != 0:
                self.target_node += direction
                self.moving = True
                self.move_progress = 0.0

        if self.moving:
            start_node = world.nodes[self.target_node - (1 if self.move_progress < 0 else 0)]
            end_node = world.nodes[self.target_node]
            
            self.move_progress += 0.05
            if self.move_progress >= 1.0:
                self.move_progress = 1.0
                self.moving = False
                
            self.x = start_node.x + (end_node.x - start_node.x) * self.move_progress
            self.y = start_node.y + (end_node.y - start_node.y) * self.move_progress
            self.rect.x = self.x
            self.rect.y = self.y

    def draw(self, surface):
        pygame.draw.rect(surface, PALETTE['mario_red'], self.rect)
        # Draw Mario's hat
        hat_rect = pygame.Rect(self.rect.x + 5, self.rect.y - 10, 20, 5)
        pygame.draw.rect(surface, PALETTE['highlight_yellow'], hat_rect)

class LevelGenerator:
    @staticmethod
    def generate_level(level_id):
        """Generate a simplified level based on SMB3 level types"""
        level_data = LEVEL_TYPES.get(level_id, {
            'theme': 'grassland',
            'length': 'short',
            'difficulty': 'easy',
            'features': ['basic_platforms']
        })
        
        # Create a surface for the level
        level_surface = pygame.Surface((800, 600))
        
        # Set background based on theme
        if level_data['theme'] == 'grassland':
            level_surface.fill(PALETTE['sky_blue'])
            # Draw ground
            pygame.draw.rect(level_surface, PALETTE['grass_green'], (0, 500, 800, 100))
        elif level_data['theme'] == 'underground':
            level_surface.fill(PALETTE['black'])
            # Draw ceiling and floor
            pygame.draw.rect(level_surface, PALETTE['path_brown'], (0, 0, 800, 50))
            pygame.draw.rect(level_surface, PALETTE['path_brown'], (0, 550, 800, 50))
        elif level_data['theme'] == 'sky':
            level_surface.fill(PALETTE['sky_blue'])
            # Draw clouds
            for i in range(5):
                x = random.randint(50, 700)
                y = random.randint(100, 400)
                pygame.draw.ellipse(level_surface, PALETTE['cloud_white'], (x, y, 100, 50))
        elif level_data['theme'] == 'castle':
            level_surface.fill(PALETTE['castle_gray'])
            # Draw bricks
            for i in range(10):
                x = random.randint(50, 700)
                y = random.randint(100, 500)
                pygame.draw.rect(level_surface, PALETTE['mountain_gray'], (x, y, 40, 20))
        
        # Add level info text
        font = pygame.font.Font(None, 36)
        title = font.render(f"Level {level_id}", True, PALETTE['white'])
        theme = font.render(f"Theme: {level_data['theme']}", True, PALETTE['white'])
        features = font.render(f"Features: {', '.join(level_data['features'])}", True, PALETTE['white'])
        
        level_surface.blit(title, (50, 50))
        level_surface.blit(theme, (50, 100))
        level_surface.blit(features, (50, 150))
        
        # Add "Press ESC to return" text
        return_text = font.render("Press ESC to return to world map", True, PALETTE['white'])
        level_surface.blit(return_text, (50, 550))
        
        return level_surface

class GameState:
    WORLD_MAP = 0
    LEVEL = 1

def main():
    pygame.init()
    pygame.display.set_caption("Super Mario Bros 3 - World 1")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    world_map = WorldMap()
    player = Player()
    current_state = GameState.WORLD_MAP
    current_level = None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and current_state == GameState.LEVEL:
                    current_state = GameState.WORLD_MAP
                
                if event.key == pygame.K_SPACE and current_state == GameState.WORLD_MAP:
                    # Check if player is on a node
                    for node in world_map.nodes:
                        if player.rect.colliderect(node.rect):
                            if node.type == 'level' or node.type == 'castle':
                                current_level = LevelGenerator.generate_level(node.level_id)
                                current_state = GameState.LEVEL
                            break
        
        keys = pygame.key.get_pressed()
        
        if current_state == GameState.WORLD_MAP:
            player.update(world_map, keys)
            screen.blit(world_map.background, (0, 0))
            player.draw(screen)
            
            # Draw UI
            world_text = font.render("World 1", True, PALETTE['black'])
            help_text = font.render("Press SPACE to enter level", True, PALETTE['black'])
            screen.blit(world_text, (10, 10))
            screen.blit(help_text, (10, 50))
            
        elif current_state == GameState.LEVEL:
            screen.blit(current_level, (0, 0))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
