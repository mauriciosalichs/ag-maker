import pygame

class Object:
    def __init__(self, image_path):
        image = pygame.image.load(image_path).convert_alpha()  # Carga la imagen del objeto
        new_size = (image.get_width() // 2, image.get_height() // 2)
        self.image = pygame.transform.scale(image, new_size)
        self.position = None
        #self.rect = self.image.get_rect(center=self.position)  # Rectángulo de colisión
    
    def draw(self, screen):
        """Dibuja el objeto en la pantalla."""
        draw_position = self.position - pygame.Vector2(self.image.get_width() / 2, self.image.get_height())
        screen.blit(self.image, draw_position)

