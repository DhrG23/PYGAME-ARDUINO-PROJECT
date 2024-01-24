# Python Code
import pygame
import serial
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Game")

# Set up the spaceship object
spaceship_color = (0, 128, 255)
spaceship_width = 50
spaceship_height = 50
spaceship_x = width // 2 - spaceship_width // 2
spaceship_y = height - 2 * spaceship_height

# Set up the falling balls
ball_color = (255, 0, 0)
ball_radius = 20
balls = []

# Set up the Arduino serial connection
arduino_port = "COMX"  # Change this to your Arduino port
arduino_baud = 9600
ser = serial.Serial(arduino_port, arduino_baud, timeout=1)

# Set up game clock
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read distance data from Arduino
    try:
        distance = int(ser.readline().decode('utf-8').strip())
        print(f"Distance: {distance} cm")

        # Use distance data to control spaceship movement
        spaceship_x = width - distance * 5  # Adjust this based on your needs

    except ValueError:
        print("Invalid distance data")

    # Add falling balls
    if random.random() < 0.02:  # Adjust the probability based on your needs
        ball_x = random.randint(0, width - ball_radius)
        ball_y = -ball_radius
        balls.append([ball_x, ball_y])

    # Move falling balls
    for ball in balls:
        ball[1] += 5  # Adjust the speed based on your needs

    # Check for collisions between the spaceship and falling balls
    for ball in balls:
        ball_rect = pygame.Rect(ball[0], ball[1], ball_radius * 2, ball_radius * 2)
        spaceship_rect = pygame.Rect(spaceship_x, spaceship_y, spaceship_width, spaceship_height)

        if ball_rect.colliderect(spaceship_rect):
            # Handle collision (you can add sound effects, scoring, etc.)
            print("Collision!")
            balls.remove(ball)

    # Remove balls that have gone off the screen
    balls = [ball for ball in balls if ball[1] < height]

    # Draw the spaceship and falling balls on the screen
    screen.fill((0, 0, 0))  # Black background
    pygame.draw.rect(screen, spaceship_color, (spaceship_x, spaceship_y, spaceship_width, spaceship_height))

    for ball in balls:
        pygame.draw.circle(screen, ball_color, (ball[0] + ball_radius, ball[1] + ball_radius), ball_radius)

    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(30)  # Adjust the frame rate based on your needs

pygame.quit()
ser.close()
