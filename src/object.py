import pygame
from src.utils import *

class Object:
    def __init__(self, game, image_path, name, description, image = None):
        self.game = game
        self.image = image if image else pygame.image.load(image_path).convert_alpha()  # Carga la imagen del objeto
        self.name = name
        self.description = description
        self.position = None
        self.rect = None
        self.font = pygame.font.SysFont("Courier", 24, bold=True)
        self.text_surface = self.font.render(self.name, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
        
        # Logic properties of an object
        self.position_to_interact = None
        self.is_grabbable = False
        self.is_in_inventory = False
        self.standalone_use = False

    def area_includes(self, x, y):
        if not self.rect.collidepoint((x, y)):
            return False
        fix_x = x - self.rect.left
        fix_y = y - self.rect.top
        return self.image.get_at((fix_x, fix_y)).a > 0

    def set_position(self, position):
        self.position = position
        self.rect = self.image.get_rect(midbottom=position)

    def observe(self):
        self.game.show_text(self.description)

    def use(self, grabbed_object):
        if self.is_grabbable:
            if euclidean_distance(self.game.current_scene.main_character.position, self.position) < 70:
                self.game.grab_object(self)
                self.game.show_text(f"COJEMOS {self.name}")
            else:
                self.game.show_text(f"Estoy demasiado lejos como para cogerlo.")
        else:
            extra_text = f" CON {grabbed_object.name}" if grabbed_object else ""
            self.game.show_text(f"USAMOS {self.name}{extra_text}")
        
    def draw(self, screen):
        """Dibuja el objeto en la pantalla."""
        if self.game.debug_running:
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)
        screen.blit(self.image, self.rect.topleft)
        
        x, y = self.game.mouse_pos
        if self.rect.collidepoint((x,y)):
            fix_x = x - self.rect.left
            fix_y = y - self.rect.top
            if self.image.get_at((fix_x, fix_y)).a > 0:
                self.text_rect.centerx = x
                self.text_rect.bottom = y - 20
                screen.blit(self.text_surface, self.text_rect)
