import pygame
from scene import Scene
from character import Character
from object import Object
from utils import *

ASSETS_DIR = "../assets"
CHARACTERS_DIR = f"{ASSETS_DIR}/characters"
MAIN_CHARACTER_DIR = f"{CHARACTERS_DIR}/main"
BACKGROUNDS_DIR = f"{ASSETS_DIR}/backgrounds"
OBJECTS_DIR = f"{ASSETS_DIR}/objects"

MAIN_CHARACTER_WALKING = f"{MAIN_CHARACTER_DIR}/walking_left"
SAGRADA_FAMILIA_BCK = f"{BACKGROUNDS_DIR}/sagrada_familia.webp"
CAR_IMG = f"{OBJECTS_DIR}/sf-car.png"

# Inicializamos pygame
pygame.init()
sf_background = pygame.image.load(SAGRADA_FAMILIA_BCK)
WORLD_WIDTH = sf_background.get_width()
WORLD_HEIGHT = sf_background.get_height()
CAMERA_WIDTH = 600
CAMERA_HEIGHT = 600
screen = pygame.display.set_mode((CAMERA_WIDTH, CAMERA_HEIGHT))
world = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))
camera = pygame.Rect(0, 0, CAMERA_WIDTH, CAMERA_HEIGHT)

# Crear una escena con una imagen de fondo
scene = Scene(sf_background)
# Añadir un área caminable (polígono de ejemplo)
scene.set_walkable_area([(495, 599), (682, 761), (1039, 605), (770, 516)])
# Añade un auto a la escena
car_obj = Object(CAR_IMG)
car_position = (700,700)
scene.add_object(car_obj, car_position)
# Crear y añadir un personaje a la escena
character = Character(MAIN_CHARACTER_WALKING)
character_position = (409,421)
scene.add_character(character, character_position)


# Bucle principal del juego
running = True
while running:
    
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
    if camera.left < 0:
        camera.left = 0
    if camera.right > WORLD_WIDTH:
        camera.right = WORLD_WIDTH
    if camera.top < 0:
        camera.top = 0
    if camera.bottom > WORLD_HEIGHT:
        camera.bottom = WORLD_HEIGHT
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_position = (event.pos[0] + camera.x, event.pos[1] + camera.y)
            scene.handle_mouse_event(click_position)
    
    # Actualizar la escena
    scene.update()
    # Dibujar la escena
    scene.draw(world)
    
    screen.blit(world, (0, 0), camera)
    pygame.display.flip()

pygame.quit()
