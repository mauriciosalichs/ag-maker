from game import *
from character import Character
from object import Object

MAIN_CHARACTER_WALKING = f"{MAIN_CHARACTER_DIR}/walking_left"
SAGRADA_FAMILIA_BCK = f"{BACKGROUNDS_DIR}/sagrada_familia.webp"
CAR_IMG = f"{OBJECTS_DIR}/Coche.png"
TENT_IMG = f"{OBJECTS_DIR}/Carpa.png"
LAMP_IMG = f"{OBJECTS_DIR}/Lampara.png"

game = Game(SAGRADA_FAMILIA_BCK,1000, 800)
# Añadir un área caminable (polígono de ejemplo)
game.current_scene.add_walkable_area([(166, 300), (161, 450), (678, 780), (1066, 615)])

#Añadir un objeto a la escena
lamp = Object(game, LAMP_IMG, "Lampara", ["Una lámpara alta, de metal negro, con un diseño minimalista.","Su luz es tenue, casi como si","estuviera luchando por mantenerse encendida."])
car = Object(game, CAR_IMG, "Coche", ["Es un coche de aspecto antiguo, con la pintura desconchada","y las ruedas ligeramente desinfladas.","No parece que haya nadie dentro,","pero no se mueve desde hace un buen rato.","¿Quién lo habrá dejado aquí?"])
tent = Object(game, TENT_IMG, "Carpa", ["Una tienda de campaña plantada justo en medio de la calle.","Está algo sucia y parece haber resistido","varias noches a la intemperie.","¿Qué clase de persona decide acampar aquí?"])
game.current_scene.add_object(lamp, (330,500))
game.current_scene.add_object(car, (580,600))

# Añadir elementos en el inventario
game.inventory.setup(grid=(4,3), left_padding=8, top_padding= 12, cell_size=130, hspace=8, vspace=8)
game.inventory.add_item(tent)

# Crear y añadir un personaje a la escena
character = Character(MAIN_CHARACTER_WALKING)
character_position = (409,421)
game.current_scene.add_character(character, character_position)

game.run()
