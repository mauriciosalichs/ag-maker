from game import *
from character import Character
from object import Object

MAIN_CHARACTER_WALKING = f"{MAIN_CHARACTER_DIR}/walking_left"
SAGRADA_FAMILIA_BCK = f"{BACKGROUNDS_DIR}/sagrada_familia.webp"
CAR_IMG = f"{OBJECTS_DIR}/sf-car.png"

game = Game(SAGRADA_FAMILIA_BCK,1000, 500)
# Añadir un área caminable (polígono de ejemplo)
game.current_scene.add_walkable_area([(166, 300), (161, 450), (678, 780), (1066, 615)])
# Añadir un area prohibida
game.current_scene.add_forbidden_area([(485, 596),(460, 530),(651, 477),(780, 536),(757, 605)])

# Añade un auto a la escena
car_obj = Object(game, CAR_IMG, "Coche", "¿Quien habrá olvidado su coche en medio de la calle?")
car_position = (600,600)
game.current_scene.add_object(car_obj, car_position)
# Crear y añadir un personaje a la escena
character = Character(MAIN_CHARACTER_WALKING)
character_position = (409,421)
game.current_scene.add_character(character, character_position)

game.run()
