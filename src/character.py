import pygame, os
from src.utils import *

class Character:
    def __init__(self, game, char_id, data, dialogues):
        self.game = game
        self.id = char_id
        self.image = None
        self.name = data['name']
        self.description = data['description']
        self.currentState = data['currentState']
        self.sprites = self.load_sprites(data["spritesDirs"][self.currentState])
        self.dialogues = dialogues
        self.current_frame = 0
        self.position = None
        self.rect = None
        
        self.target_position = self.position  # Posición objetivo (a dónde se moverá)
        self.speed = 0.5  # Velocidad de movimiento del personaje
        self.is_moving = False
        self.walking_path = []
        self.frame_delay = 10  # Cuántos frames de actualización se esperan antes de cambiar el sprite
        self.frame_counter = 0  # Contador de frames
        self.face_left = True

        self.font = pygame.font.SysFont("Courier", 24, bold=True)
        self.text_surface = self.font.render(self.name, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
    
    def load_sprites(self, folder):
        """Carga todas las imágenes de una carpeta y las devuelve como una lista."""
        sprites = []
        root_dir = os.path.dirname(__file__)+'/../'
        for filename in sorted(os.listdir(root_dir+folder)):
            path = os.path.join(folder, filename)
            image = pygame.image.load(path).convert_alpha()
            # Redimensionar la imagen si es necesario
            new_size = (image.get_width() // 3, image.get_height() // 3)
            image = pygame.transform.scale(image, new_size)
            sprites.append(image)
        self.image = sprites[0]
        return sprites

    def area_includes(self, x, y):
        if not self.rect.collidepoint((x, y)):
            return False
        fix_x = x - self.rect.left
        fix_y = y - self.rect.top
        try:
            return self.image.get_at((fix_x, fix_y)).a > 0
        except:
            return False

    def observe(self):
        self.game.show_text(self.description)

    def use(self, grabbed_object):
        if grabbed_object:
            self.game.show_text(f"USAMOS {grabbed_object.name} SOBRE {self.name}")
        else:
            if euclidean_distance(self.game.current_scene.main_character.position, self.position) < 70:
                self.run_dialogue()
            else:
                self.game.show_text(f"Estoy demasiado lejos como para hablar.")

    def run_dialogue(self):
        if not self.dialogues:
            self.game.show_text("¿Por que demonios le hablaría?")
            return
        # self.game.start_conversation(self.dialogues)

    def draw(self, screen):
        """Dibuja el personaje en la pantalla usando su referencia inferior central."""
        self.image = self.sprites[self.current_frame]
        screen.blit(self.image, self.rect.topleft)

        x, y = self.game.mouse_pos
        if self.area_includes(x, y):
            self.text_rect.centerx = x
            self.text_rect.bottom = y - 20
            screen.blit(self.text_surface, self.text_rect)
    
    def update(self):
        """Actualiza la posición del personaje y la animación."""
        if self.is_moving:
            direction = self.target_position - self.position
            distance = direction.length()
            
            if distance > self.speed:
                # Mover en dirección al objetivo
                direction.scale_to_length(self.speed)
                self.position += direction
                self.rect = self.image.get_rect(midbottom=self.position)  # Rectángulo de colisión

                # Cambiar al siguiente frame de la animación con retraso
                self.frame_counter += 1
                if self.frame_counter >= self.frame_delay:
                    self.current_frame = (self.current_frame + 1) % len(self.sprites)
                    self.frame_counter = 0
            else:
                if self.walking_path:
                    position = self.walking_path[0]
                    self.walking_path = self.walking_path[1:]
                    self.move_to(position)
                else:
                    # Detenerse al llegar al destino
                    self.position = [self.target_position.x, self.target_position.y]
                    self.rect = self.image.get_rect(midbottom=self.position)  # Rectángulo de colisión
                    self.is_moving = False
                    self.current_frame = 0  # Frame estático inicial
    
    def move_to(self, position):
        """Mueve el personaje a una posición dada usando como referencia el centro inferior."""
        self.target_position = pygame.Vector2(position)
        self.is_moving = True
        # Reflejar la imagen si el clic está a la izquierda o derecha del personaje
        if (self.face_left and self.target_position[0] < self.position[0]) or (not self.face_left and self.target_position[0] > self.position[0]):
            self.sprites = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites]
            self.face_left = not self.face_left

    def change_state(self, data, newState):
        self.currentState = newState
        try:
            self.sprites = self.load_sprites(data["spritesDirs"][self.currentState])
        except:
            print("not a drawable state")

    def update_from_data(self, new_data):
        eval(f"self.{new_data[0]} = {new_data[1]}")
