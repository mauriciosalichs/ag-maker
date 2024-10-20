import os
import numpy as np
from src.utils import *

# Colors for dialogue
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)

def generate_beep(frequency, duration):
    num_samples = int(44100 * duration)
    t = np.linspace(0, duration, num_samples, False)
    waveform = 0.5 * np.sin(2 * np.pi * frequency * t)
    waveform = (waveform * (2 ** 15 - 1)).astype(np.int16)
    stereo_waveform = np.column_stack((waveform, waveform))
    sound = pygame.sndarray.make_sound(stereo_waveform)
    return sound

class Character:
    def __init__(self, game, char_id, data, dialogues):
        self.game = game
        self.id = char_id
        self.image = None
        self.name = data['name'] if 'name' in data.keys() else 'Figura desconocida'
        self.description = data['description'] if 'description' in data.keys() else 'Nada interesante que comentar.'
        self.currentState = data['currentState'] if 'currentState' in data.keys() else 'idle'
        self.dialogue_color = eval(data['dialogueColor']) if 'dialogueColor' in data.keys() else BLACK
        self.dialogue_sound = generate_beep(freq_to_col(self.dialogue_color), 0.1)
        self.sprite_dirs = data["spritesDirs"]
        self.sprites = self.load_sprites(self.sprite_dirs[self.currentState])
        self.dialogue_data = dialogues
        self.current_frame = 0

        self.position = None
        self.interact_position = None # [x,y,side]
        self.rect = None
        self.face_right = True
        
        self.target_position = self.position  # Posición objetivo (a dónde se moverá)
        self.speed = 0.5  # Velocidad de movimiento del personaje
        self.is_moving = False
        self.states = data["states"]
        self.currentState = 'idle'
        self.walking_path = []
        self.frame_delay = data['frameDelay'] if 'frameDelay' in data.keys() else 10
        self.frame_counter = 0  # Contador de frames

        self.font = pygame.font.SysFont("Courier", 24, bold=True)
        self.text_surface = self.font.render(self.name, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()

    def change_name(self, name):
        self.name = name
        self.game.current_action_finished(f"changed name {self.id} to {name}")

    def change_description(self, description):
        self.description = description
        self.game.current_action_finished(f"changed description {self.id} to {description}")

    def change_conversation(self, conversation_id):
        self.dialogue_data = self.game.conversations_data[conversation_id]
        self.game.current_action_finished(f"changed conversation {self.id} to {conversation_id}")

    def area_includes(self, x, y):
        if not self.rect.collidepoint((x, y)):
            return False
        fix_x = x - self.rect.left
        fix_y = y - self.rect.top
        try:
            return self.image.get_at((fix_x, fix_y)).a > 0
        except:
            return False

    def load_sprites(self, folder):
        """Carga todas las imágenes de una carpeta y las devuelve como una lista."""
        sprites = []
        root_dir = os.path.dirname(__file__)+'/../'
        for filename in sorted(os.listdir(root_dir+folder)):
            path = os.path.join(folder, filename)
            image = pygame.image.load(path).convert_alpha()
            # Redimensionar la imagen si es necesario (esto debería hacerse en el archivo)
            new_size = (image.get_width() // 3, image.get_height() // 3)
            image = pygame.transform.scale(image, new_size)
            sprites.append(image)
        self.image = sprites[0]
        return sprites

    def observe(self, ret=False):
        self.game.show_text(self.description)
        if ret:
            self.game.current_action_finished(f"observe {self.id}")

    def use(self, grabbed_object):
        if self.interact_position:
            x, y, side = self.interact_position
            if self.game.main_character.position != [x, y]:
                self.game.actions.add_action(self.game.main_character, "walk_to", (x, y))
                self.game.actions.add_action(self.game.main_character, "turn", side)
                self.game.actions.add_action(self, "use_", grabbed_object)
                self.game.actions.continue_current_actions()
            else:
                self.use_(grabbed_object)
        elif euclidean_distance(self.game.main_character.position, self.position) > 250:
            self.game.show_text(f"Estoy demasiado lejos.")
        elif grabbed_object and not self.game.use_object_with_target(self.id, grabbed_object.id):
            self.game.show_text("No se porque haría eso.")
        elif grabbed_object:
            self.game.show_text(f"USAMOS {grabbed_object} en {self.name}")
        else:
            self.use_(grabbed_object)

    def use_(self, grabbed_object=None):
        print("USE_",self.id)
        if grabbed_object:
            if not self.game.use_object_with_target(self.id, grabbed_object.id):
                self.game.show_text("No se porque haría eso.")
        else:
            self.run_dialogue()

    def run_dialogue(self):
        if self.dialogue_data:
            self.game.start_conversation(self)
        else:
            self.speak("¿Por que demonios le hablaría?")

    def end_dialogue(self):
        self.game.end_conversation(self)

    def speak(self, text):
        # TODO: Add voice? Change animation when speaking?
        self.change_state('speak')
        self.game.show_text(text, self.dialogue_color)

    def draw(self, screen):
        """Dibuja el personaje en la pantalla usando su referencia inferior central."""
        self.image = self.sprites[self.current_frame]
        self.rect = self.image.get_rect(midbottom=self.position)
        screen.blit(self.image, self.rect.topleft)

    def flip(self):
        self.sprites = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites]

    def turn(self, side):
        if (side == 'left' and self.face_right) or (side == 'right' and not self.face_right):
            self.flip()
            self.face_right = not self.face_right
        self.game.current_action_finished(f"turn {side}")

    def update(self):
        """Actualiza la posición del personaje y la animación."""
        # Cambiar al siguiente frame de la animación con retraso
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.sprites)
            self.frame_counter = 0

        if self.is_moving:
            direction = self.target_position - self.position
            distance = direction.length()
            
            if distance > self.speed:
                # Mover en dirección al objetivo
                direction.scale_to_length(self.speed)
                self.position += direction
                self.rect = self.image.get_rect(midbottom=self.position)  # Rectángulo de colisión

            else:
                if self.walking_path:
                    position = self.walking_path[0]
                    self.walking_path = self.walking_path[1:]
                    self.move_to(position)
                else:
                    # Detenerse al llegar al destino
                    self.position = [int(self.target_position.x), int(self.target_position.y)]
                    self.rect = self.image.get_rect(midbottom=self.position)  # Rectángulo de colisión
                    self.is_moving = False
                    self.change_state('idle')
                    self.game.current_action_finished(f"moving {self.id}")

    def add_conv_id(self, id_to_remove):
        for value in self.dialogue_data.values():
            for resp in value['responses']:
                if 'textHiddenID' in resp.keys() and resp['textHiddenID'] == id_to_remove:
                    del resp['textHiddenID']
        self.game.current_action_finished(f"add_conv_id {id_to_remove}")

    def walk_to(self, position):
        if self in self.game.current_scene.characters:
            self.game.current_scene.walk_to(self, position)

    def move_to(self, position):
        """Mueve el personaje a una posición dada usando como referencia el centro inferior."""
        self.target_position = pygame.Vector2(position)
        going_left = (self.target_position[0] < self.position[0])
        self.is_moving = True
        self.change_state('walkingLeft')
        # Reflejar la imagen si el camino está a la izquierda o derecha del personaje
        if self.face_right == going_left:
            self.flip()
            self.face_right = not self.face_right

    def change_state(self, newState):
        self.currentState = newState
        try:
            self.sprites = self.load_sprites(self.sprite_dirs[self.currentState])
            if not self.face_right:
                self.flip()
            self.current_frame = 0
        except:
            print("not a drawable state")

    def update_from_data(self, new_data, ret=False):
        eval(f"self.{new_data[0]} = {new_data[1]}")
        if ret:
            self.game.current_action_finished(f"update_from_data {new_data}")