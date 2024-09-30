from game import *
from character import Character
from object import Object

MAIN_CHARACTER_WALKING = f"{MAIN_CHARACTER_DIR}/walking_left"
SAGRADA_FAMILIA_BCK = f"{BACKGROUNDS_DIR}/sagrada_familia.webp"
CAR_IMG = f"{OBJECTS_DIR}/Coche.png"

game = Game(SAGRADA_FAMILIA_BCK,1000, 800)
# Añadir un área caminable (polígono de ejemplo)
game.current_scene.add_walkable_area([(166, 300), (161, 450), (678, 780), (1066, 615)])

# Añadir un elemento en el inventario
car = Object(game, CAR_IMG, "Coche", "Un coche feo.")
game.inventory.setup((5,1), 100, pygame.Rect(100,100,500,500), 10, 10)
game.inventory.add_item(car)

# Crear y añadir un personaje a la escena
character = Character(MAIN_CHARACTER_WALKING)
character_position = (409,421)
game.current_scene.add_character(character, character_position)

game.run()
