import tkinter as tk
import pygame
import random
import array
import math  # Moved to top for clarity

# Game Constants
WIDTH, HEIGHT = 600, 400
BALL_SIZE = 15
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
BALL_SPEED = 5
PADDLE_SPEED_AI = 4
WIN_SCORE = 5

# Colors
BLACK = "#000000"
WHITE = "#FFFFFF"

# Sound Constants
SAMPLE_RATE = 44100
SOUND_ENABLED = True  # Always enable sound attempts

class PongGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pong - Beep Boop Edition")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initialize pygame mixer
        self.init_sounds()
        
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BLACK)
        self.canvas.pack(padx=10, pady=10)
        
        # Game Objects
        self.ball = self.canvas.create_oval(
            (WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2),
            (WIDTH//2 + BALL_SIZE//2, HEIGHT//2 + BALL_SIZE//2),
            fill=WHITE
        )
        self.player_paddle = self.canvas.create_rectangle(
            (50, HEIGHT//2 - PADDLE_HEIGHT//2),
            (50 + PADDLE_WIDTH, HEIGHT//2 + PADDLE_HEIGHT//2),
            fill=WHITE
        )
        self.opponent_paddle = self.canvas.create_rectangle(
            (WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2),
            (WIDTH - 50, HEIGHT//2 + PADDLE_HEIGHT//2),
            fill=WHITE
        )
        self.center_line = self.canvas.create_line(WIDTH//2, 0, WIDTH//2, HEIGHT, fill=WHITE, dash=(10, 10))
        
        # Game Variables
        self.ball_vel_x = BALL_SPEED * random.choice((1, -1))
        self.ball_vel_y = BALL_SPEED * random.choice((1, -1))
        self.player_score = self.opponent_score = 0
        
        # Bind mouse movement
        self.root.bind("<Motion>", self.mouse_move)
        self.root.bind("<Key>", self.key_press)
        
        self.game_over = False
        self.setup_game()

    def init_sounds(self):
        try:
            # Initialize mixer with proper settings
            pygame.mixer.init(frequency=SAMPLE_RATE, channels=1)
            self.beep = self.generate_tone(880)  # Higher pitch for beeps
            self.boop = self.generate_tone(440)  # Lower pitch for boops
        except pygame.error as e:
            print(f"Sound initialization failed: {e}. Running in silent mode.")
            SOUND_ENABLED = False

    def generate_tone(self, frequency):
        duration = 200  # milliseconds
        num_samples = int(SAMPLE_RATE * duration / 1000)
        buf = array.array('h', [0] * num_samples)
        for i in range(num_samples):
            # Generate sine wave instead of square wave for better sound
            sample = int(32767 * 0.5 * 
                         (1 + math.sin(2 * math.pi * frequency * i / SAMPLE_RATE)))
            buf[i] = sample
        return pygame.mixer.Sound(buffer=buf)

    def play_sound(self, sound):
        try:
            if pygame.mixer.get_init():
                sound.play()
        except:
            pass

    def setup_game(self):
        self.game_over = False
        self.player_score = self.opponent_score = 0
        self.reset_ball()
        self.update_scores()
        self.canvas.delete("game_over")  # Clear any existing game over text

    def mouse_move(self, event):
        if self.game_over:
            return
        paddle_y = event.y - PADDLE_HEIGHT//2
        paddle_y = max(0, min(paddle_y, HEIGHT - PADDLE_HEIGHT))
        self.canvas.coords(self.player_paddle, 50, paddle_y, 50 + PADDLE_WIDTH, paddle_y + PADDLE_HEIGHT)

    def key_press(self, event):
        if self.game_over:
            if event.keysym.lower() == 'y':  # Accept both upper and lower case
                self.setup_game()
            elif event.keysym.lower() == 'n':
                self.root.destroy()
        elif event.keysym == 'Escape':
            self.root.destroy()

    def reset_ball(self):
        self.canvas.coords(self.ball, 
                          WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2,
                          WIDTH//2 + BALL_SIZE//2, HEIGHT//2 + BALL_SIZE//2)
        self.ball_vel_x = BALL_SPEED * random.choice((1, -1))
        self.ball_vel_y = BALL_SPEED * random.choice((1, -1))

    def update_scores(self):
        self.canvas.delete("score")
        self.canvas.create_text(150, 50, text=str(self.player_score), fill=WHITE, font=("Arial", 36), tags="score")
        self.canvas.create_text(450, 50, text=str(self.opponent_score), fill=WHITE, font=("Arial", 36), tags="score")

    def draw_game_over(self):
        self.canvas.delete("game_over")
        winner = "YOU WIN!" if self.player_score >= WIN_SCORE else "AI WINS!"
        # Draw game over text on top layer
        self.canvas.create_text(WIDTH//2, HEIGHT//2, text=winner, fill=WHITE, font=("Arial", 36), tags="game_over")
        self.canvas.create_text(WIDTH//2, HEIGHT//2 + 40, text="Play again? (Y/N)", fill=WHITE, font=("Arial", 20), tags="game_over")
        # Bring game over text to front
        self.canvas.tag_raise("game_over")

    def update_ai(self):
        if self.game_over:
            return
            
        ball_y = self.canvas.coords(self.ball)[1]
        paddle_y = self.canvas.coords(self.opponent_paddle)[1]
        target_y = ball_y + random.randint(-10, 10)  # Add some randomness
        
        if paddle_y > target_y:
            self.canvas.move(self.opponent_paddle, 0, -PADDLE_SPEED_AI)
        elif paddle_y < target_y:
            self.canvas.move(self.opponent_paddle, 0, PADDLE_SPEED_AI)

    def update_ball(self):
        if self.game_over:
            return
            
        self.canvas.move(self.ball, self.ball_vel_x, self.ball_vel_y)
        
        # Wall collision
        ball_coords = self.canvas.coords(self.ball)
        if ball_coords[1] <= 0 or ball_coords[3] >= HEIGHT:
            self.ball_vel_y = -self.ball_vel_y
            self.play_sound(self.boop)
        
        # Paddle collision
        if self.ball_vel_x < 0:
            paddle_coords = self.canvas.coords(self.player_paddle)
            if (ball_coords[0] <= paddle_coords[2] and
                ball_coords[1] <= paddle_coords[3] and
                ball_coords[3] >= paddle_coords[1]):
                self.ball_vel_x = -self.ball_vel_x
                self.play_sound(self.beep)
        else:
            paddle_coords = self.canvas.coords(self.opponent_paddle)
            if (ball_coords[2] >= paddle_coords[0] and
                ball_coords[1] <= paddle_coords[3] and
                ball_coords[3] >= paddle_coords[1]):
                self.ball_vel_x = -self.ball_vel_x
                self.play_sound(self.boop)

    def check_score(self):
        if self.game_over:
            return
            
        ball_coords = self.canvas.coords(self.ball)
        if ball_coords[0] <= 0:
            self.opponent_score += 1
            self.play_sound(self.boop)
            self.reset_ball()
        elif ball_coords[2] >= WIDTH:
            self.player_score += 1
            self.play_sound(self.beep)
            self.reset_ball()

        if self.player_score >= WIN_SCORE or self.opponent_score >= WIN_SCORE:
            self.game_over = True
            self.draw_game_over()
        else:
            # Only update scores if game is still active
            self.update_scores()

    def game_loop(self):
        if not self.game_over:
            self.update_ai()
            self.update_ball()
            self.check_score()
        self.root.after(16, self.game_loop)

    def on_closing(self):
        if pygame.mixer.get_init():
            pygame.mixer.quit()
        self.root.destroy()

# Start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = PongGame(root)
    game.game_loop()
    root.mainloop()
