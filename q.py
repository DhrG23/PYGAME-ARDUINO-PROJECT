import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

# Game variables
score = 0
cybersecurity_question = {
    "question": "What is a VPN?",
    "options": ["A: Virtual Private Network", "B: Very Private Network", "C: Visible Public Network", "D: Vast Personal Network"],
    "correct_option": "A: Virtual Private Network"
}
current_question_index = 0
falling_speed = 5
initial_falling_speed = falling_speed
speed_increase_factor = 0.5
ship_speed = 10

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cybersecurity Quiz Game")

# Functions
def display_question():
    question_text = FONT.render(cybersecurity_question["question"], True, WHITE)
    screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, 20))

def display_score():
    score_text = FONT.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

def spawn_answer():
    correct_option = cybersecurity_question["correct_option"]
    answer_rect = pygame.Rect(random.randint(50, WIDTH - 50), 0, 30, 30)
    return answer_rect, correct_option

def game_over():
    game_over_text = FONT.render("Game Over. Your score is: " + str(score), True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

# Game loop
clock = pygame.time.Clock()

ship_rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 50, 50, 50)
bullets = []
answer_rect, correct_option = spawn_answer()

spawn_answer_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_answer_event, 5000)  # spawn new answers every 5000 milliseconds

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == spawn_answer_event:
            answer_rect, correct_option = spawn_answer()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship_rect.left > 0:
        ship_rect.x -= ship_speed
    if keys[pygame.K_RIGHT] and ship_rect.right < WIDTH:
        ship_rect.x += ship_speed

    # Shoot bullet
    if keys[pygame.K_SPACE]:
        bullet_rect = pygame.Rect(ship_rect.centerx - 10, ship_rect.centery - 20, 20, 20)
        bullets.append(bullet_rect)

    # Move bullets
    bullets = [bullet.move(0, -10) for bullet in bullets]

    # Move answer
    answer_rect.y += falling_speed

    # Check collision with correct answer
    for bullet in bullets:
        if bullet.colliderect(answer_rect):
            if correct_option == cybersecurity_question["options"][0]:
                score += 1
                falling_speed = initial_falling_speed + speed_increase_factor * score
            else:
                game_over()
            bullets.remove(bullet)

    # Display background
    screen.fill(BLACK)

    # Display question
    display_question()

    # Display score
    display_score()

    # Display spaceship
    pygame.draw.rect(screen, WHITE, ship_rect)

    # Display bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    # Display answer
    pygame.draw.rect(screen, WHITE, answer_rect)
    answer_surface = FONT.render(correct_option, True, BLACK)
    screen.blit(answer_surface, (answer_rect.centerx - answer_surface.get_width() // 2, answer_rect.centery - answer_surface.get_height() // 2))

    pygame.display.flip()
    clock.tick(FPS)
