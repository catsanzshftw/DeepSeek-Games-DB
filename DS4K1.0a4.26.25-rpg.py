import pygame
import sys
import math

class DeltaruneEngine:
    def __init__(self):
        pygame.init()
        self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Deltarune Zero Engine")
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Game state
        self.current_chapter = 0
        self.in_overworld = True
        self.player_pos = [self.width//2, self.height//2]
        self.player_speed = 3
        self.player_color = (255, 255, 255)
        
        # World parameters
        self.overworld_entities = []
        self.chapter_entities = []
        self.dialog_active = False
        self.dialog_text = ""
        self.dialog_timer = 0
        
        # R1 Zero technique variables
        self.iteration_count = 0
        self.self_iterating = False
        self.ambient_pulse = 0
        
        # Initialize some test entities
        self._init_test_entities()
    
    def _init_test_entities(self):
        # Overworld entities (simple circles)
        self.overworld_entities = [
            {"pos": [100, 100], "radius": 20, "color": (200, 50, 50), "interact": "chapter0"},
            {"pos": [500, 300], "radius": 20, "color": (50, 200, 50), "interact": "secret"},
            {"pos": [300, 400], "radius": 20, "color": (50, 50, 200), "interact": "test"}
        ]
        
        # Chapter 0 entities
        self.chapter_entities = [
            {"pos": [200, 200], "radius": 30, "color": (150, 150, 255), "interact": "enemy1"},
            {"pos": [400, 250], "radius": 25, "color": (255, 150, 150), "interact": "enemy2"}
        ]
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if not self.dialog_active:
            # Movement
            if keys[pygame.K_LEFT]:
                self.player_pos[0] -= self.player_speed
            if keys[pygame.K_RIGHT]:
                self.player_pos[0] += self.player_speed
            if keys[pygame.K_UP]:
                self.player_pos[1] -= self.player_speed
            if keys[pygame.K_DOWN]:
                self.player_pos[1] += self.player_speed
            
            # Interaction
            if keys[pygame.K_z]:
                self.check_interactions()
        
        # Debug/iteration controls
        if keys[pygame.K_r]:
            self.self_iterating = not self.self_iterating
        if keys[pygame.K_0]:
            self.in_overworld = not self.in_overworld
    
    def check_interactions(self):
        entities = self.overworld_entities if self.in_overworld else self.chapter_entities
        
        for entity in entities:
            distance = math.sqrt((self.player_pos[0] - entity["pos"][0])**2 + 
                                (self.player_pos[1] - entity["pos"][1])**2)
            
            if distance < 30 + entity["radius"]:
                self.trigger_interaction(entity["interact"])
                break
    
    def trigger_interaction(self, interaction_type):
        self.dialog_active = True
        
        if interaction_type == "chapter0":
            self.dialog_text = "Enter Chapter 0? (Press Z to confirm)"
            self.pending_action = lambda: self.start_chapter(0)
        elif interaction_type.startswith("enemy"):
            self.dialog_text = f"Encountered {interaction_type}! (Press Z)"
        else:
            self.dialog_text = f"Interacted with {interaction_type} (Press Z)"
        
        self.dialog_timer = 120
    
    def start_chapter(self, chapter_num):
        self.current_chapter = chapter_num
        self.in_overworld = False
        self.player_pos = [self.width//2, self.height//2]
    
    def return_to_overworld(self):
        self.in_overworld = True
        self.player_pos = [self.width//2, self.height//2]
    
    def update(self):
        # Handle dialog timer
        if self.dialog_active:
            self.dialog_timer -= 1
            if self.dialog_timer <= 0:
                self.dialog_active = False
        
        # R1 Zero technique: self-iteration
        if self.self_iterating:
            self.iteration_count += 1
            self.ambient_pulse = (math.sin(self.iteration_count * 0.05) + 1) * 50
        
        # Keep player in bounds
        self.player_pos[0] = max(10, min(self.width - 10, self.player_pos[0]))
        self.player_pos[1] = max(10, min(self.height - 10, self.player_pos[1]))
    
    def render(self):
        # Clear screen with ambient pulse if iterating
        if self.self_iterating:
            bg_color = (10 + self.ambient_pulse, 10, 20 + self.ambient_pulse//2)
        else:
            bg_color = (10, 10, 20)
        
        self.screen.fill(bg_color)
        
        # Draw appropriate entities
        entities = self.overworld_entities if self.in_overworld else self.chapter_entities
        
        for entity in entities:
            pygame.draw.circle(self.screen, entity["color"], entity["pos"], entity["radius"])
        
        # Draw player (triangle representing direction)
        pygame.draw.polygon(self.screen, self.player_color, [
            (self.player_pos[0], self.player_pos[1] - 10),
            (self.player_pos[0] - 7, self.player_pos[1] + 7),
            (self.player_pos[0] + 7, self.player_pos[1] + 7)
        ])
        
        # Draw dialog if active
        if self.dialog_active:
            dialog_rect = pygame.Rect(50, self.height - 100, self.width - 100, 80)
            pygame.draw.rect(self.screen, (0, 0, 0), dialog_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), dialog_rect, 2)
            
            font = pygame.font.SysFont(None, 24)
            text = font.render(self.dialog_text, True, (255, 255, 255))
            self.screen.blit(text, (70, self.height - 80))
        
        # Draw debug info
        debug_text = f"FPS: {int(self.clock.get_fps())} | {'Overworld' if self.in_overworld else f'Chapter {self.current_chapter}'}"
        debug_text += f" | ITER: {self.iteration_count}" if self.self_iterating else ""
        font = pygame.font.SysFont(None, 20)
        text = font.render(debug_text, True, (200, 200, 200))
        self.screen.blit(text, (10, 10))
        
        pygame.display.flip()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z and self.dialog_active:
                        if hasattr(self, 'pending_action'):
                            self.pending_action()
                            del self.pending_action
                        self.dialog_active = False
                    elif event.key == pygame.K_ESCAPE and not self.in_overworld:
                        self.return_to_overworld()
            
            self.handle_input()
            self.update()
            self.render()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    engine = DeltaruneEngine()
    engine.run()
