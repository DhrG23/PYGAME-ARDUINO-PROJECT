import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()

# Set up display in fullscreen mode
width, height = 1920, 1080  # Adjust these values based on your screen resolution
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.OPENGL)

# Set up the perspective
gluPerspective(45, (width / height), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glRotatef(1, 3, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw a simple cube
    glBegin(GL_QUADS)
    # ... (Same cube drawing code as before)
    glEnd()

    pygame.display.flip()
    pygame.time.wait(10)
