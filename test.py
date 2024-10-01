from src.game import Game
from src.character import Character
from src.object import Object

def read_file(file_path):
    config_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Strip whitespace and skip empty lines or comments
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Split line by '=' and strip whitespace
            key_value = line.split('=')
            if len(key_value) == 2:  # Ensure there are exactly two parts
                key = key_value[0].strip()
                value = eval(key_value[1].strip())
                config_dict[key] = value
    
    return config_dict


config = read_file('config.ini')
#assets = read_file('assets.ini')



MAIN_CHARACTER_WALKING = f"{config['MAIN_CHARACTER_DIR']}/walking_left"
SAGRADA_FAMILIA_BCK = f"{config['BACKGROUNDS_DIR']}/sagrada_familia.webp"
CURSOR_PATH = f"{config['ASSETS_DIR']}/cursor.png"
INVENTORY_PATH = f"{config['ASSETS_DIR']}/inventory.png"
CAR_IMG = f"{config['OBJECTS_DIR']}/Coche.png"
TENT_IMG = f"{config['OBJECTS_DIR']}/Carpa.png"
LAMP_IMG = f"{config['OBJECTS_DIR']}/Lampara.png"

# Inciamos el juego
game = Game(SAGRADA_FAMILIA_BCK,1000, 800, cursor_img_path=CURSOR_PATH, inventory_img_path=INVENTORY_PATH)
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
# Ejecutamos el juego
game.run()
