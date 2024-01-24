import pygame
import serial
import random
import sys
import time

pygame.init()

# Set up the initial game window size
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Game")

# Load the custom font
custom_font = "Caveat-VariableFont_wght.ttf"  # Replace with the path to your font file
font = pygame.font.Font(custom_font, 36)

# Set up the initial spaceship size
spaceship_width, spaceship_height = 100, 100
spaceship_x = width // 2 - spaceship_width // 2
spaceship_y = height - 2 * spaceship_height

background_image = pygame.image.load("bg3.png")  # Replace with your image path
background_image = pygame.transform.scale(background_image, (width, height))

# Load the spaceship image
spaceship_image = pygame.image.load("your_spaceship_image.png")
spaceship_image = pygame.transform.scale(spaceship_image, (spaceship_width, spaceship_height))

# Load the collision object sprites
collision_sprite1 = pygame.image.load("collision_sprite1.png")
collision_sprite1 = pygame.transform.scale(collision_sprite1, (50, 50))

collision_sprite2 = pygame.image.load("collision_sprite2.png")
collision_sprite2 = pygame.transform.scale(collision_sprite2, (50, 50))

shield_sprite = pygame.image.load("shield_sprite.png")
shield_sprite = pygame.transform.scale(shield_sprite, (50, 50))

health_sprite = pygame.image.load("health_sprite.png")  # Replace with your health power-up sprite
health_sprite = pygame.transform.scale(health_sprite, (50, 50))

objects = []

star_color = (255, 255, 255)
stars = [(random.randint(0, width), random.randint(0, height)) for _ in range(50)]

health = 100
shield_duration = 15  # in seconds
shield_end_time = 0

clock = pygame.time.Clock()

def draw_spaceship(x, y):
    screen.blit(spaceship_image, (x, y))

def draw_objects():
    for obj in objects:
        if obj[2] == "collision":
            if obj[3] == 1:
                screen.blit(collision_sprite1, (obj[0], obj[1]))
            else:
                screen.blit(collision_sprite2, (obj[0], obj[1]))
        elif obj[2] == "shield":
            screen.blit(shield_sprite, (obj[0], obj[1]))
        elif obj[2] == "health":
            screen.blit(health_sprite, (obj[0], obj[1]))

def draw_stars():
    for star in stars:
        pygame.draw.circle(screen, star_color, star, 1)

def draw_health_bar():
    pygame.draw.rect(screen, (0, 255, 0), (10, 10, health * 2, 20))
    pygame.draw.rect(screen, (255, 255, 255), (10, 10, 200, 20), 2)

    # Use the custom font for rendering text
    health_text = font.render("Health: {}".format(health), True, (255, 255, 255))
    screen.blit(health_text, (220, 10))

def draw_menu():
    title_font = pygame.font.Font(custom_font, 72)
    title_text = title_font.render("Space Game", True, (255, 255, 255))
    start_text = font.render("Press SPACE to start", True, (255, 255, 255))
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 4))
    screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2))

def draw_game_over():
    game_over_font = pygame.font.Font(custom_font, 72)
    game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
    retry_text = font.render("Press R to retry", True, (255, 255, 255))
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 4))
    screen.blit(retry_text, (width // 2 - retry_text.get_width() // 2, height // 2))

def handle_menu():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return "game"
    return "menu"

def handle_game_over():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return "retry"
    return "game_over"

def rigth():
    global spaceship_x 
    spaceship_x += 5

def left():
    global spaceship_x 
    spaceship_x -= 5

def nomov():
    global spaceship_x 
    spaceship_x +=0

def Movement():
        # Read data from the Arduino
        dis[0] = ser.readline().decode().strip()
        if dis[0]:
            dis[0] = int(dis[0])
            if dis[0] > 21:
                nomov()  
            elif dis[0] < THRESHOLD_DISTANCE:
                rigth() # Move right
            elif dis[0] > THRESHOLD_DISTANCE:
                left() # Move left

# Set initial background position
background_y = 0

# Variables for power-ups and collision speed
power_up_spawn_probability = 0.1  # Adjust as needed
collision_spawn_probability = 0.5  # Adjust as needed
speed_increase_interval = 15  # in seconds
initial_falling_speed = 5
speed_increase_amount = 5

#Set up the serial connection
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the correct port

# Replace 'COM3' with the correct port for your Arduino
THRESHOLD_DISTANCE = 10
dis = [None,1]

def game_loop():
    global health, shield_end_time, objects, spaceship_x, spaceship_y, falling_speed, background_y, THRESHOLD_DISTANCE

    falling_speed = initial_falling_speed
    shield_end_time = 0
    time_since_speed_increase = 0

    # Create initial objects
    for _ in range(5):
        obj_x = random.randint(0, width - 50)
        obj_y = random.randint(-height, 0)
        obj_type = random.choice(["shield", "health", "collision"])
        if obj_type == "collision":
            obj_subtype = random.randint(1, 2)
            damage = 10 if obj_subtype == 1 else 20
            objects.append([obj_x, obj_y, "collision", obj_subtype, damage])
        else:
            objects.append([obj_x, obj_y, obj_type])
   
    while True:
            screen.fill((0, 0, 0))  # Black background

            state = handle_menu()
            if state == "game":
                break
            elif state == "quit":
                pygame.quit()
                sys.exit()
            draw_stars()
            draw_menu()
            pygame.display.flip()
            clock.tick(30)


    while True:
        screen.fill((0, 0, 0))  # Black background

        # Move the background
        background_y += falling_speed
        if background_y > height:
            background_y = 0

        # Draw the background
        screen.blit(background_image, (0, background_y - height))
        screen.blit(background_image, (0, background_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        for obj in objects:
            if (
                spaceship_x < obj[0] < spaceship_x + spaceship_width and
                spaceship_y < obj[1] < spaceship_y + spaceship_height
            ):
                if obj[2] == "collision":
                    damage = obj[3]
                    health -= damage
                elif obj[2] == "shield":
                    shield_duration = 15
                    shield_end_time = time.time() + shield_duration
                elif obj[2] == "health":
                    health += 20
                    if health > 100:
                        health = 100
                objects.remove(obj)

        objects = [obj for obj in objects if obj[1] < height]

        if random.random() < collision_spawn_probability:
            obj_x = random.randint(0, width - 50)
            obj_y = -50
            obj_subtype = random.randint(1, 2)
            damage = 10 if obj_subtype == 1 else 20
            objects.append([obj_x, obj_y, "collision", obj_subtype, damage])

        if random.random() < power_up_spawn_probability:
            obj_x = random.randint(0, width - 50)
            obj_y = -50
            obj_type = random.choice(["shield", "health"])
            objects.append([obj_x, obj_y, obj_type])

        draw_stars()
        draw_spaceship(spaceship_x, spaceship_y)
        draw_objects()
        draw_health_bar()

        if health <= 0:
            state = "game_over"

        if time.time() < shield_end_time:
            pygame.draw.rect(screen, (0, 0, 255), (spaceship_x, spaceship_y, spaceship_width, spaceship_height), 3)

        pygame.display.flip()
        clock.tick(30)

        if state == "game_over":
            while True:
                screen.fill((0, 0, 0))  # Black background
                draw_game_over()
                pygame.display.flip()
                state = handle_game_over()
                if state == "retry":
                    health = 100
                    shield_end_time = 0
                    objects = []
                    falling_speed = initial_falling_speed  # Reset falling speed
                    time_since_speed_increase = 0  # Reset time counter
                    break
                elif state == "quit":
                    pygame.quit()
                    sys.exit()
                clock.tick(30)

        # Increase collision speed after a certain interval
        time_since_speed_increase += 1 / 30  # Assuming 30 frames per second
        if time_since_speed_increase >= speed_increase_interval:
            falling_speed += speed_increase_amount
            time_since_speed_increase = 0  # Reset time counter

if __name__ == "__main__":
    game_loop()

