# Python Code (Keyboard Controls)

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
pygame.display.set_caption("Space Game")

background_image = pygame.image.load("C:/Users/dhruv/Desktop/ROBOTICS_GAME/Asset 2mdpi.png")
background_image = pygame.transform.scale(background_image, (width, height))


# Set up the spaceship object
spaceship_color = (0, 128, 255)
spaceship_width = 100
spaceship_height = 100
spaceship_x = width // 2 - spaceship_width // 2
spaceship_y = height - 2 * spaceship_height

# Set up the falling balls
ball_color = (255, 0, 0)
ball_radius = 20
balls = []

# Set up game clock
clock = pygame.time.Clock()

def draw_spaceship(x, y):
    pygame.draw.rect(screen, spaceship_color, (x, y, spaceship_width, spaceship_height))

def draw_ball(x, y):
    pygame.draw.circle(screen, ball_color, (x, y), ball_radius)

def game_over():
    font = pygame.font.SysFont(None, 55)
    text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(text, (width // 2 - 120, height // 2 - 30))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit()

spaceship_image = pygame.image.load("C:/Users/dhruv/Desktop/ROBOTICS_GAME/Asset 1xxxhdpi.png")
spaceship_image = pygame.transform.scale(spaceship_image, (spaceship_width, spaceship_height))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the background
    screen.blit(background_image, (0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spaceship_x > 0:
        spaceship_x -= 5
    if keys[pygame.K_RIGHT] and spaceship_x < width - spaceship_width:
        spaceship_x += 5

    # Add falling balls
    if random.random() < 0.02:
        ball_x = random.randint(0, width - ball_radius * 2)
        ball_y = -ball_radius
        balls.append([ball_x, ball_y])

    # Move falling balls
    for ball in balls:
        ball[1] += 5

    # Check for collisions between the spaceship and falling balls
    for ball in balls:
        if (
            spaceship_x < ball[0] < spaceship_x + spaceship_width and
            spaceship_y < ball[1] < spaceship_y + spaceship_height
        ):
            # Handle collision
            game_over()

    # Remove balls that have gone off the screen
    balls = [ball for ball in balls if ball[1] < height]

    # Draw the spaceship and falling balls on the screen
    screen.blit(spaceship_image, (spaceship_x, spaceship_y))
    for ball in balls:
        pygame.draw.circle(screen, ball_color, (ball[0], ball[1]), ball_radius, 1)  # Use 1 for antialiasing


    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(30)  # Adjust the frame rate based on your needs

pygame.quit()
