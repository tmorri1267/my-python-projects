import pygame
import sys
import random

pygame.init()

# Screen Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enemy Crush")
clock = pygame.time.Clock()

# Frame Rate Controller
FPS = 60

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
CHARCOAL = (54, 54, 54)
BLUE = (50, 150, 255)
LIGHT_BLUE = (135, 206, 235)  
RED = (255, 0, 0)
LIGHT_RED = (255, 204, 203)
GREEN = (0, 128, 0)
LIGHT_GREEN = (144, 238, 144)

# Fonts
TITLE_FONT = pygame.font.SysFont("ptmono", 64, bold=True)
BUTTON_FONT = pygame.font.SysFont("ptmono", 32)
TEXT_FONT = pygame.font.SysFont("ptmono", 20)
SCORE_FONT = pygame.font.SysFont("ptmono", 26)

# --- THE BUTTON CLASS ---
class Button:
    def __init__(self, text, x, y, width, height, base_color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color

        # Render the text surface once
        self.text_surf = BUTTON_FONT.render(text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        # Draw the button body
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=8)

        # Draw the button text
        screen.blit(self.text_surf, self.text_rect)

    def check_hover(self, mouse_pos):
        # Change color is mouse hovers over button
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.base_color

    def is_clicked(self, click_pos):
        # Check if the button is hovered and clicked
        return self.rect.collidepoint(click_pos)

# --- THE TIMER CLASS ---
class Timer:
    def __init__(self, x, y, text, color, seconds):
        self.seconds = seconds
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont("ptmono", 50)
        self.rect = pygame.Rect(x, y, 60, 60)

    def start(self):
        self.is_running = True
        self.start_ticks = pygame.time.get_ticks() // 1000

    def get_remaining_time(self):
        # If the timer isn't running, do not count down; otherwise, do the countdown.
        if self.is_running == False:
            return self.seconds
        else:
            current_time = pygame.time.get_ticks() // 1000
            elapsed_time = current_time - self.start_ticks
            remaining_time = max(0, self.seconds - elapsed_time)
            return remaining_time

    def is_expired(self):
        return self.get_remaining_time() <= 0

    def draw(self, screen):
        seconds = self.get_remaining_time()
        text_surf = self.font.render(f"{self.text}: {seconds}", True, self.color)

        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

# --- THE PLAYER CLASS ---
class Player:
    def __init__(self, name, x, y, color):
        self.name = name # Player name
        self.color = color # Player color
        self.rect = pygame.Rect(x, y, 50, 50) # Player shape
        self.speed = 5

    def move(self):
        # Checks for any key being pressed on the keybaord
        keys = pygame.key.get_pressed()

        # Input handling (movement)
        # If the player presses the "<-" or "a" key, move them to the left with correspondence to speed
        # This logic applies to all other inputs relating to movement.
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # Boundary clamping logic
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

    def draw(self, screen_surface):
        # Draws the plaer on the screen
        pygame.draw.rect(screen_surface, self.color, self.rect)

# --- THE ENEMY CLASS ---
class Enemy:
    def __init__(self, name, x, y):
        self.name = name
        self.color = RED
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed_x = random.choice([-5, -3, 3, 5])
        self.speed_y = random.choice([-5, -3, 3, 5])
        self.hp = 5

        self.is_respawning = False
        self.respawn_time = 0
        self.delay_duration = 1500 # (in milliseconds)


    def update_ai(self):
        if self.is_respawning:
            current_time = pygame.time.get_ticks()
            if current_time - self.respawn_time >= self.delay_duration:
                self.respawn()
            return # Skips position updates while waiting to spawn
    
        # Enemies will always be moving to the speed in the __init__() function
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Right wall
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.speed_x = self.speed_x * -1
            self.speed_y = random.choice([-5, -3, 3, 5]) # Picks a random vertical speed when colliding into the wall

        # Left wall
        if self.rect.left <= 0:
            self.rect.left = 0
            self.speed_x = self.speed_x * -1
            self.speed_y = random.choice([-5, -3, 3, 5]) # Picks a random vertical speed when colliding into the wall

        # Top wall
        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y = self.speed_y * -1
            self.speed_x = random.choice([-5, -3, 3, 5]) # Picks a random horizontal speed when colliding into the wall

        # Bottom wall
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y = self.speed_y * -1
            self.speed_x = random.choice([-5, -3, 3, 5]) # Picks a random horizontal speed when colliding into the wall

    def start_respawn_timer(self):
        self.is_respawning = True
        self.respawn_time = pygame.time.get_ticks() # Saves current timestamp
        self.hp = 0
    
    def respawn(self):
        # Relocate safely inside screen margins
        self.rect.x = random.randint(50, SCREEN_WIDTH - 50)
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.hp = 5
        self.is_respawning = False

        # Assign fresh velocity vector on respawn
        self.speed_x = random.choice([-5, -4, -3, 3, 4, 5])
        self.speed_y = random.choice([-5, -4, -3, 3, 4, 5])

    def draw(self, screen_surface):
        # Don't draw the enemy while waiting to respawn
        if not self.is_respawning:
            top_point = (self.rect.x + (self.rect.width // 2), self.rect.y)
            bottom_left = (self.rect.x, self.rect.bottom)
            bottom_right = (self.rect.right, self.rect.bottom)
            pygame.draw.polygon(screen_surface, self.color, [top_point, bottom_left, bottom_right])


# Instantiate global game objects
# Center buttons horizontally by subtracting half of the button width from SCREEN_WIDTH / 2
play_button = Button(
    "Play",
    SCREEN_WIDTH // 2 - 100,
    300,
    200,
    60,
    GREEN,
    LIGHT_GREEN,
)

play_again_button = Button(
    "Play Again",
    255,
    300,
    300,
    60,
    GREEN,
    LIGHT_GREEN,
)


quit_button = Button(
    "Quit",
    SCREEN_WIDTH // 2 - 100,
    400,
    200,
    60,
    RED,
    LIGHT_RED,
)

score = 0
player = Player("Player", 400, 400, (50, 150, 255))
enemy1 = Enemy("Enemy 1", random.randint(100, 300), 150)
enemy2 = Enemy("Enemy 2", random.randint(100, 300), 150)
enemy3 = Enemy("Enemy 3", random.randint(100, 300), 150)
timer1 = Timer(355, 275, "Starting in", WHITE, 5)
timer2 = Timer(355, 25, "Time left", WHITE, 60)

# Game State Variable
# States: "INTRO", "COUNTDOWN", "PLAYING", "END", "GAME OVER"
game_state = "INTRO"

# ~~~ MENU SCREEN FUNCTION ~~~
def handle_menu_screen(mouse_pos, events_list):
    global running, game_state

    # Event handling
    for event in events_list:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.is_clicked(event.pos):
                game_state = "COUNTDOWN"
                timer1.start()
            elif quit_button.is_clicked(event.pos):
                running = False


        # Fill intro background
        screen.fill(BLACK)

        # Draw Title text
        title_surf = TITLE_FONT.render("Enemy Crush!", True, BLUE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surf, title_rect)

        # Draw subtitle text
        text_surf = TEXT_FONT.render("Defeat as much enemies as you can in a minute!", True, LIGHT_BLUE)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, 225))
        screen.blit(text_surf, text_rect)

        text_surf = TEXT_FONT.render("Game Version: 1.0", True, LIGHT_GREEN)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, 550))
        screen.blit(text_surf, text_rect)

        # Update button layouts
        play_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)

        # Draws the buttons on the screen
        play_button.draw(screen)
        quit_button.draw(screen)

# ~~~ COUNTDOWN SCREEN FUNCTION ~~~ 
def handle_countdown_screen():
    global game_state, score
    score = 0

    screen.fill(BLACK)
    timer1.draw(screen)

    if timer1.is_expired():
        game_state = "PLAYING"
        timer2.start()

# ~~~ GAMEPLAY SCREEN FUNCTION ~~~
def handle_gameplay_screen(events_list):
    global game_state, running, score


    # Process actions like clicking close buttons inside playing frames
    for event in events_list:
        if event.type == pygame.QUIT:
            running = False
            
    player.move()
    enemy1.update_ai()
    enemy2.update_ai()
    enemy3.update_ai()

    # Collision system interaction checker
    if not enemy1.is_respawning and player.rect.colliderect(enemy1.rect):
        score += 1
        enemy1.start_respawn_timer()

    # If enemy hp is less than or equal to zero, respawn an enemy on the screen in a random place
    if enemy1.hp <= 0 and not enemy1.is_respawning:
        score += 1
        enemy1.start_respawn_timer()
    
    if enemy1.rect.colliderect(player.rect):
        enemy1.hp -= 5

    if not enemy2.is_respawning and player.rect.colliderect(enemy2.rect):
        score += 1
        enemy2.start_respawn_timer()

    # If enemy hp is less than or equal to zero, respawn an enemy on the screen in a random place.
    if enemy2.hp <= 0 and not enemy2.is_respawning:

        enemy2.start_respawn_timer()
    
    if enemy2.rect.colliderect(player.rect):
        enemy2.hp -= 5

    if not enemy3.is_respawning and player.rect.colliderect(enemy3.rect):
        score += 1
        enemy3.start_respawn_timer()

    
    # If enemy hp is less than or equal to zero, respawn an enemy on the screen in a random place.
    if enemy3.hp <= 0 and not enemy3.is_respawning:
        score += 1
        enemy3.start_respawn_timer()
    
    if enemy3.rect.colliderect(player.rect):
        enemy3.hp -= 5


    # Render frame updates cleanly
    screen.fill((30, 30, 30))
    timer2.draw(screen)
    player.draw(screen)
    enemy1.draw(screen)
    enemy2.draw(screen)
    enemy3.draw(screen)

    # Draw subtitle text
    text_surf = TEXT_FONT.render("Use the WASD keys or the arrow keys to move around!", True, GREEN)
    text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, 500))
    screen.blit(text_surf, text_rect)
    score_surf = SCORE_FONT.render(f"Score: {score}", True, BLUE)
    screen.blit(score_surf, (330, 100))


    if timer2.is_expired():
        game_state = "END"

# ~~~ END SCREEN FUNCTION ~~~
def handle_end_screen(mouse_pos, events_list):
    global game_state, running, score

    # Event handling
    for event in events_list:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_again_button.is_clicked(event.pos):
                game_state = "COUNTDOWN"
                timer1.start()
            elif quit_button.is_clicked(event.pos):
                running = False


        # Fill background
        screen.fill(CHARCOAL)

        # Draw Title text
        title_surf = TITLE_FONT.render(f"You scored {score}!", True, BLUE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surf, title_rect)

        # Draw subtitle text
        text_surf = TEXT_FONT.render("Would you like to play again or quit?", True, WHITE)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, 230))
        screen.blit(text_surf, text_rect)

        # Update button layouts
        play_again_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)

        # Draws the buttons on the screen
        play_again_button.draw(screen)
        quit_button.draw(screen)



# Main game loop
running = True
while running:
    # Safely pull event cues exactly once per full framework loop execution
    current_events = pygame.event.get()
    for event in current_events:
        if event.type == pygame.QUIT:
            running = False


    mouse_pos = pygame.mouse.get_pos()

    if game_state == "INTRO":
        handle_menu_screen(mouse_pos, current_events)
        pygame.display.set_caption("Enemy Crush")
    elif game_state == "COUNTDOWN":
        handle_countdown_screen()
        pygame.display.set_caption("Enemy Crush - Countdown")
    elif game_state == "PLAYING":
        handle_gameplay_screen(current_events)
        pygame.display.set_caption("Enemy Crush - Playing")
    elif game_state == "END":
        handle_end_screen(mouse_pos, current_events)
        pygame.display.set_caption("Enemy Crush - Results")

    pygame.display.flip() # Updates display
    clock.tick(60) # Caps game at 60 fps

pygame.quit()
sys.exit()
