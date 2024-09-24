import pygame
from scene import Scene
from character import Character
from utils import *

ASSETS_DIR = "../assets"
CHARACTERS_DIR = f"{ASSETS_DIR}/characters"
MAIN_CHARACTER_DIR = f"{CHARACTERS_DIR}/main"
BACKGROUNDS_DIR = f"{ASSETS_DIR}/backgrounds"

MAIN_CHARACTER_WALKING = f"{MAIN_CHARACTER_DIR}/walking_left"
SAGRADA_FAMILIA_BCK = f"{BACKGROUNDS_DIR}/sagrada_familia.webp"


# Ejemplo de uso
pygame.init()
screen = pygame.display.set_mode((1200, 800))

# Crear una escena con una imagen de fondo
scene = Scene(pygame.image.load(SAGRADA_FAMILIA_BCK))
# Añadir un área caminable (polígono de ejemplo)
scene.set_walkable_area([(495, 599), (682, 761), (1039, 605), (770, 516)])
# Crear y añadir un personaje a la escena
character = Character(MAIN_CHARACTER_WALKING, (663, 647))
scene.add_character(character, (663, 647))

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            scene.handle_mouse_event(event.pos)
    
    # Actualizar la escena
    scene.update()
    
    # Dibujar la escena
    scene.draw(screen)
    
    # Actualizar pantalla
    pygame.display.flip()

pygame.quit()
