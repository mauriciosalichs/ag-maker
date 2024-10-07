from src.game import Game
from src.scene import Scene
from src.character import Character
from src.object import Object
from src.debug import Debug
from src.inventory import Inventory
from src.actions import Actions

import json

# Save game information to json file

def save_state(scene, inventory, data):
    data['inventory']['items'] = []
    for item in inventory.items:
        data['inventory']['items'].append(item[0].id)

    data['scenes'][scene.id]["walkableAreas"] = scene.walkable_areas
    data['scenes'][scene.id]["forbiddenAreas"] = scene.forbidden_areas
    data['scenes'][scene.id]['objects'] = []
    data['scenes'][scene.id]['characters'] = []
    for obj in scene.objects:
        data['scenes'][scene.id]['objects'].append([obj.id,obj.position])
    for char in scene.characters:
        data['scenes'][scene.id]['characters'].append([char.id,char.position])
    return data
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

game_data = load_data("games/gameTest.json")['game']
scenes_data = load_data("games/gameTestScenes.json")['scenes']
characters_data = load_data("games/gameTestCharacters.json")['characters']
objects_data = load_data("games/gameTestObjects.json")['objects']
dialogues_data = load_data("games/gameTestDialogues.json")['dialogues']
actions_data = load_data("games/gameTestActions.json")['actions']

# Set all image paths

for key, value in characters_data.items():
    characters_data[key]['spritesDirs'] = {}
    for state in value['states']:
        characters_data[key]['spritesDirs'][state] = f"{config['CHARACTERS_DIR']}/{key}/{state}"

for key, value in objects_data.items():
    if 'img' in value.keys():
        objects_data[key]['imageDir'] = f"{config['OBJECTS_DIR']}/{value['img']}"

for key, value in scenes_data.items():
    scenes_data[key]['backgroundDir'] = f"{config['BACKGROUNDS_DIR']}/{value['backgroundImg']}"

CURSOR_PATH = f"{config['ASSETS_DIR']}/cursor.png"
INVENTORY_PATH = f"{config['ASSETS_DIR']}/inventory.png"

# We setup the game with initial scene

game = Game(game_data["cameraWidth"], game_data["cameraHeight"], CURSOR_PATH)

iD = game_data['inventory']
inventory = Inventory(game, INVENTORY_PATH)
inventory.setup(iD['grid'], iD['leftPadding'], iD['topPadding'], iD['cellSize'], iD['hspace'], iD['vspace'])
for od in iD["items"]:
    object_data = objects_data[od]
    inventory.add_item(Object(game, od, object_data))

actions = Actions(game, actions_data)

current_scene_data = scenes_data[game_data["currentScene"]]
current_scene = Scene(game, game_data["currentScene"], current_scene_data)
for od in current_scene_data["objects"]:
    object_data = objects_data[od[0]]
    current_scene.add_object(Object(game, od[0], object_data), od[1])
for cd in current_scene_data["characters"]:
    character_data = characters_data[cd[0]]
    char_dialogues = dialogues_data[cd[0]] if cd[0] in dialogues_data.keys() else None
    current_scene.add_character(Character(game, cd[0], character_data, char_dialogues), cd[1])

game.set_inventory(inventory)
game.set_actions(actions)
game.set_scene(current_scene)


if config['DEBUG']:
    game.debug = Debug(game, config['OBJECTS_DIR'])

game.run()

# Before we close, we save the data (if the character isn't moving)
if game.current_scene.main_character.is_moving:
    print("We dont save data as character is moving")
    exit()
game_data['game'] = save_state(game.current_scene, game.inventory, data)
with open('games/savedState.json', 'w') as f:
    json.dump(game_data, f, indent=2)