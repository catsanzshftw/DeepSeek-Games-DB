import pygame
import sys

# SMB3 GBA Palette
PALETTE = {
    'sky_blue': (135, 206, 235),
    'grass_green': (34, 139, 34),
    'path_brown': (139, 69, 19),
    'mountain_gray': (192, 192, 192),
    'mario_red': (205, 0, 0),
    'castle_gray': (112, 128, 144),
    'cloud_white': (245, 245, 220),
    'highlight_yellow': (255, 255, 0)
}

# World 1 node positions (GBA layout)
WORLD_1_NODES = [
    (100, 300),  # Start
    (250, 300),  # 1-1
    (400, 300),  # 1-2
    (550, 300),  # 1-3
    (700, 300),  # Castle
]

class Node:
    def __init__(self, x, y, node_type):
        self.x = x
        self.y = y
        self.type = node_type  # 'start', 'level', 'castle'

class World:
    def __init__(self):
        self.nodes = [
            Node(100, 300, 'start'),
            Node(250, 300, 'level'),
            Node(400, 300, 'level'),
            Node(550, 300, 'level'),
            Node(700, 300, 'castle')
        ]
        self.paths = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4)
        ]
        
        # Pre-render background surface
        self.background = pygame.Surface((800, 600))
        self.background.fill(PALETTE['sky_blue'])
        
        # Draw paths
        for connection in self.paths:
            start = self.nodes[connection[0]]
            end = self.nodes[connection[1]]
            pygame.draw.line(self.background, PALETTE['path_brown'],
                            (start.x + 15, start.y + 15),
                            (end.x + 15, end.y + 15), 5)
            
        # Draw nodes
        for node in self.nodes:
            color = PALETTE['grass_green']
            if node.type == 'castle':
                color = PALETTE['castle_gray']
            pygame.draw.rect(self.background, color,
                            (node.x, node.y, 30, 30))

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

    def update(self, world, keys):
        if not self.moving:
            direction = 0
            if keys[pygame.K_RIGHT] and self.target_node < len(world.nodes)-1:
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

    def draw(self, screen):
        pygame.draw.rect(screen, PALETTE['mario_red'], 
                        (self.x, self.y, self.size, self.size))
        pygame.draw.rect(screen, PALETTE['highlight_yellow'], 
                        (self.x + 5, self.y - 10, 20, 5))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    world = World()
    player = Player()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.update(world, keys)
        
        # Optimized drawing
        screen.blit(world.background, (0, 0))
        player.draw(screen)
        
        # Draw UI
        world_text = font.render("World 1", True, (0,0,0))
        screen.blit(world_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
