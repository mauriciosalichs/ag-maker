from src.game import Game
from src.scene import Scene
from src.character import Character
from src.object import Object
from src.debug import Debug
from src.inventory import Inventory

import json

# Load json with game data

def parse_file(file_path):
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

config = parse_file('config.ini')

def load_data(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

data = load_data("gameTest.json")["game"]

# Set all image paths

for key, value in data["characters"].items():
    data["characters"][key]['spritesDirs'] = {}
    for state in value['states']:
        data["characters"][key]['spritesDirs'][state] = f"{config['CHARACTERS_DIR']}/{key}/{state}"

for key, value in data["objects"].items():
    if 'img' in value.keys():
        data["objects"][key]['imageDir'] = f"{config['OBJECTS_DIR']}/{value['img']}"

for key, value in data["scenes"].items():
    data["scenes"][key]['backgroundDir'] = f"{config['BACKGROUNDS_DIR']}/{value['backgroundImg']}"

CURSOR_PATH = f"{config['ASSETS_DIR']}/cursor.png"
INVENTORY_PATH = f"{config['ASSETS_DIR']}/inventory.png"

# Inicializamos el juego con la escena inicial

game = Game(data["cameraWidth"], data["cameraHeight"], CURSOR_PATH)

iD = data['inventory']
inventory = Inventory(game, INVENTORY_PATH)
inventory.setup(iD['grid'], iD['leftPadding'], iD['topPadding'], iD['cellSize'], iD['hspace'], iD['vspace'])
for od in iD["items"]:
    object_data = data["objects"][od]
    inventory.add_item(Object(game, object_data))
game.set_inventory(inventory)

current_scene_data = data["scenes"][data["currentScene"]]
current_scene = Scene(game, current_scene_data)
for od in current_scene_data["objects"]:
    object_data = data["objects"][od[0]]
    current_scene.add_object(Object(game, object_data), od[1])
for cd in current_scene_data["characters"]:
    character_data = data["characters"][cd[0]]
    current_scene.add_character(Character(game, character_data), cd[1])

game.set_scene(current_scene)

if config['DEBUG']:
    game.debug = Debug(game, config['OBJECTS_DIR'])

game.run()
