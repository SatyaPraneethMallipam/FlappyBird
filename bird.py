import pygame
import random

pygame.init()

# Game settings
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
BACKGROUND_COLOR = (0, 0, 0)
PIPE_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)

# Load bird image
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (50, 50))  # Resize the image

# Bird settings
bird_x = 50
bird_y = HEIGHT // 2
bird_speed = 0
bird_flap_strength = -10

# Gravity
gravity = 0.5

# Obstacles
obstacles = []

class Obstacle:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
        self.passed = False

    def move(self):
        self.x -= bird_speed

    def draw(self):
        pygame.draw.rect(win, PIPE_COLOR, (self.x, 0, 50, self.height))
        pygame.draw.rect(win, PIPE_COLOR, (self.x, self.height + 150, 50, HEIGHT))

def draw_bird(x, y):
    win.blit(bird_img, (x, y))

def draw_background():
    win.fill(BACKGROUND_COLOR)

def draw_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, TEXT_COLOR)
    win.blit(text, (10, 10))

def restart_game():
    global bird_y, bird_speed, obstacles
    bird_y = HEIGHT // 2
    bird_speed = 0
    obstacles = []

score = 0
clock = pygame.time.Clock()

running = True
game_over = False
while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_over:
                bird_speed = bird_flap_strength
            elif game_over and event.key == pygame.K_r:
                game_over = False
                restart_game()
                score = 0

    if not game_over:
        bird_speed += gravity
        bird_y += bird_speed

        if bird_y < 50:
            bird_y = 50
        elif bird_y > HEIGHT - bird_img.get_height():
            bird_y = HEIGHT - bird_img.get_height()

        if len(obstacles) == 0 or obstacles[-1].x < WIDTH - 200:
            obstacles.append(Obstacle(WIDTH))

        for obstacle in obstacles:
            obstacle.move()
            obstacle.draw()

            if obstacle.x < bird_x and not obstacle.passed:
                obstacle.passed = True
                score += 1

            if (obstacle.x < bird_x + bird_img.get_width() and
                obstacle.x + 50 > bird_x and
                (bird_y < obstacle.height or bird_y > obstacle.height + 150)):
                game_over = True

    draw_background()
    draw_bird(bird_x, bird_y)
    draw_score(score)

    if game_over:
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over - Press 'R' to Restart", True, TEXT_COLOR)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        win.blit(text, text_rect)

    pygame.display.update()

pygame.quit()