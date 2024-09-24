import pygame
import os

class Character:
    def __init__(self, sprite_folder):
        # Cargar las imágenes de la animación
        self.sprites = self.load_sprites(sprite_folder)
        self.current_frame = 0
        self.position = None
        self.target_position = self.position  # Posición objetivo (a dónde se moverá)
        self.speed = 0.5  # Velocidad de movimiento del personaje
        self.is_moving = False
        self.frame_delay = 10  # Cuántos frames de actualización se esperan antes de cambiar el sprite
        self.frame_counter = 0  # Contador de frames
        self.face_left = True
    
    def load_sprites(self, folder):
        """Carga todas las imágenes de una carpeta y las devuelve como una lista."""
        sprites = []
        for filename in sorted(os.listdir(folder)):
            path = os.path.join(folder, filename)
            image = pygame.image.load(path).convert_alpha()
            # Redimensionar la imagen si es necesario
            new_size = (image.get_width() // 3, image.get_height() // 3)
            image = pygame.transform.scale(image, new_size)
            sprites.append(image)
        return sprites
    
    def draw(self, screen):
        """Dibuja el personaje en la pantalla usando su referencia inferior central."""
        sprite = self.sprites[self.current_frame]
        # Ajustar posición para dibujar la imagen
        draw_position = self.position - pygame.Vector2(sprite.get_width() / 2, sprite.get_height())
        screen.blit(sprite, draw_position)
    
    def update(self):
        """Actualiza la posición del personaje y la animación."""
        if self.is_moving:
            direction = self.target_position - self.position
            distance = direction.length()
            
            if distance > self.speed:
                # Mover en dirección al objetivo
                direction.scale_to_length(self.speed)
                self.position += direction

                # Cambiar al siguiente frame de la animación con retraso
                self.frame_counter += 1
                if self.frame_counter >= self.frame_delay:
                    self.current_frame = (self.current_frame + 1) % len(self.sprites)
                    self.frame_counter = 0
            else:
                # Detenerse al llegar al destino
                self.position = self.target_position
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

