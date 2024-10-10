import pygame
from src.utils import *

class Scene:
    def __init__(self, game, id, data):
        self.game = game
        self.id = id
        self.background_image = pygame.image.load(data['backgroundDir'])
        self.width = self.background_image.get_width()
        self.height = self.background_image.get_height()
        self.walkable_areas = data['walkableAreas']
        self.forbidden_areas = data['forbiddenAreas']
        self.objects = []  # Lista de objetos en la escena
        self.characters = []  # Lista de personajes en la escena
        self.walkable_path = None
        self.main_character = None

    def add_walkable_area(self, polygon):
        """Añade un área caminable definida por un polígono."""
        self.walkable_areas.append(polygon)
        
    def add_forbidden_area(self, polygon):
        """Añade un área pohibida definida por un polígono."""
        self.forbidden_areas.append(polygon)
    
    def add_object(self, game_object, position=None):
        """Añade un objeto a la escena en una posición específica."""
        if position:
        	game_object.set_position(position)  # Rectángulo de colisión
        self.objects.append(game_object)
    
    def add_character(self, character, position):
        """Añade un personaje a la escena en una posición específica."""
        if not self.characters:
            self.main_character = character
        character.position = position  # Inicializar la posición del personaje
        character.rect = character.image.get_rect(midbottom=character.position)  # Rectángulo de colisión
        self.characters.append(character)
    
    def draw(self, screen, debug = False):
        """Dibuja la escena en la pantalla."""
        screen.blit(self.background_image, (0, 0))
        
        # DEBUG: Dibuja los poligonos
        if debug:
            if self.walkable_areas:
                pygame.draw.polygon(screen, (0,0,255), self.walkable_areas[0], 3)
            for forbidden in self.forbidden_areas:
                pygame.draw.polygon(screen, (255,0,0), forbidden, 3)
            if self.walkable_path:
                pygame.draw.lines(screen, (0,255,0), False, self.walkable_path, 3)
        
        main_char_drawn = False
        for obj in self.objects:
            if not main_char_drawn and obj.rect and \
               self.main_character.rect.colliderect(obj.rect) and \
               self.main_character.position[1] < obj.position[1]:	# El objeto debe aparecer adelante, entonces el personaje se dibujara primero
                self.main_character.draw(screen)
                main_char_drawn = True
            obj.draw(screen)
        if not main_char_drawn:		# Si el personaje aun no fue dibujado, lo hacemos aquí
            self.main_character.draw(screen)
            
        for character in self.characters[1:]:
            character.draw(screen)
    
    def update(self):
        for character in self.characters:
            character.update()
        # Something else to update?
    
    def handle_click(self, position, button, selected_object):
        x,y = position
        object_clicked = False
        if button == 1: 	# Left click
            for char in self.characters:
                if char.area_includes(x, y):
                    char.observe()
                    return
            for obj in self.objects:
                if obj.area_includes(x,y):
                    obj.observe()
                    return
            # No object or character clicked, then we try to walk
            self.walkable_path = self.gen_walkable_path(position)
            if self.walkable_path:
                self.characters[0].walking_path = self.walkable_path[1:]
                self.characters[0].move_to(self.walkable_path[0])
        elif button == 3: 	# Right click
            for char in self.characters:
                if char.area_includes(x,y):
                    char.use(selected_object)
                    return
            for obj in self.objects:
                if obj.area_includes(x,y):
                    obj.use(selected_object)
                    return
            # No object or character clicked, then we open the inventory
            if not self.game.grabbed_object:
                self.game.inventory_is_open = True
    
    def gen_walkable_path(self, end_position): # Por ahora, solo consideraremos un unico poligono caminable
        """Genera un camino hacia un punto dentro del área caminable."""
        polygon = self.walkable_areas[0] # for polygon in self.walkable_areas:
        if point_inside_polygon(end_position, polygon):
            for forb_pol in self.forbidden_areas:
                if point_inside_polygon(end_position, forb_pol):
                    return None
            polygons = self.walkable_areas + self.forbidden_areas
            return calculate_path(self.main_character.position, end_position, polygons)
        return None

