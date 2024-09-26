import pygame

class Object:
    def __init__(self, game, image_path, name, description):
        self.game = game
        self.image = pygame.image.load(image_path).convert_alpha()  # Carga la imagen del objeto
        self.name = name
        self.description = description
        self.position = None
        self.rect = None
    
    def draw(self, screen):
        """Dibuja el objeto en la pantalla."""
        screen.blit(self.image, self.rect.topleft)
        
        x, y = self.game.mouse_pos
        if self.rect.collidepoint((x,y)):
            fix_x = x - self.rect.left
            fix_y = y - self.rect.top
            if self.image.get_at((fix_x, fix_y)).a > 0:
                font = pygame.font.SysFont("Courier", 24)
                text_surface = font.render(self.name, True, (0, 0, 0))
                text_rect = text_surface.get_rect()
                text_rect.centerx = x
                text_rect.bottom = y - 20
                screen.blit(text_surface, text_rect)
