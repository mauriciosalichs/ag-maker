import pygame

# Initialize Pygame
pygame.init()

# Constants
WORLD_WIDTH = 2000
WORLD_HEIGHT = 1500
CAMERA_WIDTH = 800
CAMERA_HEIGHT = 600

# Create the main game window
screen = pygame.display.set_mode((CAMERA_WIDTH, CAMERA_HEIGHT))
pygame.display.set_caption('Camera Example in Pygame')

# Create the world surface (the "world" is larger than the screen)
world = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))

# Define the camera view (initially positioned at (0, 0))
camera = pygame.Rect(0, 0, CAMERA_WIDTH, CAMERA_HEIGHT)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game loop flag
running = True

# Example positions and objects to render
object_positions = [(100, 100), (400, 300), (1600, 1200), (1900, 1400)]
object_size = 50

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Control the camera with arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera.x -= 5
    if keys[pygame.K_RIGHT]:
        camera.x += 5
    if keys[pygame.K_UP]:
        camera.y -= 5
    if keys[pygame.K_DOWN]:
        camera.y += 5

    # Limit the camera movement to the bounds of the world
    if camera.left < 0:
        camera.left = 0
    if camera.right > WORLD_WIDTH:
        camera.right = WORLD_WIDTH
    if camera.top < 0:
        camera.top = 0
    if camera.bottom > WORLD_HEIGHT:
        camera.bottom = WORLD_HEIGHT

    # Fill the world with a background color
    world.fill(WHITE)

    # Draw example objects in the world
    for position in object_positions:
        pygame.draw.rect(world, RED, (position[0], position[1], object_size, object_size))

    # Draw a "camera" view indicator on the world (just for reference)
    pygame.draw.rect(world, BLUE, (camera.x, camera.y, camera.width, camera.height), 2)

    # Blit the camera portion of the world to the screen
    screen.blit(world, (0, 0), camera)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

