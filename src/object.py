import pygame

class Object:
    def __init__(self, game, image_path, name, description):
        self.game = game
        self.image = pygame.image.load(image_path).convert_alpha()  # Carga la imagen del objeto
        self.name = name
        self.description = description
        self.position = None
        self.rect = None
        self.font = pygame.font.SysFont("Courier", 24, bold=True)
        self.text_surface = self.font.render(self.name, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
                
    
    def draw(self, screen):
        """Dibuja el objeto en la pantalla."""
        if self.game.debug.working:
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
