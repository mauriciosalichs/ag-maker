import pygame
from utils import *
from character import Character

import pygame

class Scene:
    def __init__(self, background_image):
        # Cargar la imagen de fondo
        self.background_image = pygame.image.load(background_image)
        self.walkable_areas = []  # Lista de polígonos que definen las áreas caminables
        self.objects = []  # Lista de objetos en la escena
        self.characters = []  # Lista de personajes en la escena
    
    def set_walkable_area(self, polygon):
        """Añade un área caminable definida por un polígono."""
        self.walkable_areas.append(polygon)
    
    def add_object(self, game_object, position):
        """Añade un objeto a la escena en una posición específica."""
        self.objects.append((game_object, position))
    
    def add_character(self, character, position):
        """Añade un personaje a la escena en una posición específica."""
        character.position = position  # Inicializar la posición del personaje
        self.characters.append(character)
    
    def draw(self, screen):
        """Dibuja la escena en la pantalla."""
        screen.blit(self.background_image, (0, 0))
        
        # Dibuja todos los objetos
        for game_object, position in self.objects:
            game_object.draw(screen, position)
        
        # Dibuja todos los personajes
        for character in self.characters:
            character.draw(screen)
    
    def update(self):
        """Actualiza la lógica de la escena."""
        for character in self.characters:
            character.update()
    
    def handle_mouse_event(self, position):
        """Maneja el evento de clic del mouse."""
        print("click",position)
        # Si clickeas en un área caminable, mueve al personaje principal
        if self.is_within_walkable_area(position):
            if self.characters:
                main_character = self.characters[0]  # Supongamos que el primer personaje es el jugador
                main_character.move_to(position)
    
    def is_within_walkable_area(self, position):
        """Verifica si una posición está dentro de alguna área caminable."""
        for polygon in self.walkable_areas:
            if is_inside_polygon(position, polygon):
                return True
        return False

# Ejemplo de uso
pygame.init()
screen = pygame.display.set_mode((1200, 800))

# Crear una escena con una imagen de fondo
scene = Scene("sagrada_familia.webp")

# Añadir un área caminable (polígono de ejemplo)
scene.set_walkable_area([(495, 599), (682, 761), (1039, 605), (770, 516)])


# Crear y añadir un personaje a la escena
character = Character("sprites", (663, 647))
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

