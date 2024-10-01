import pygame
from src.utils import *

class Scene:
    def __init__(self, game, background_image):
        self.game = game
        self.background_image = background_image # Cargar la imagen de fondo
        self.walkable_areas = []  # Lista de polígonos que definen las áreas caminables
        self.forbidden_areas = []  # Lista de polígonos que definen las áreas prohibidas
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
    
    def add_object(self, game_object, position):
        """Añade un objeto a la escena en una posición específica."""
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
            pygame.draw.polygon(screen, (0,0,255), self.walkable_areas[0], 3)
            for forbidden in self.forbidden_areas:
                pygame.draw.polygon(screen, (255,0,0), forbidden, 3)
            if self.walkable_path:
                pygame.draw.lines(screen, (0,255,0), False, self.walkable_path, 3)
        
        main_char_drawn = False
        for obj in self.objects:
            if not main_char_drawn and \
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
        """Actualiza la lógica de la escena."""
        for character in self.characters:
            character.update()
    
    def handle_click(self, position, button, selected_object):
        """Maneja el evento de clic del mouse."""
        x,y = position
        object_clicked = False
        if button == 1: 	# Left click
            for obj in self.objects:
                if obj.area_includes(x,y):
                    obj.observe()
                    object_clicked = True
                    break
            if not object_clicked: # No object clicked, then we try to walk
                self.walkable_path = self.gen_walkable_path(position)
                if self.walkable_path:
                    self.characters[0].walking_path = self.walkable_path[1:]
                    self.characters[0].move_to(self.walkable_path[0])
        elif button == 3: 	# Right click
            for obj in self.objects:
                if obj.area_includes(x,y):
                    obj.use(selected_object)
                    object_clicked = True
                    break
            if not object_clicked and not self.game.grabbed_object:
                # No object clicked, then we open the inventory
                self.game.inventory_is_open = True
        			
    
    def gen_walkable_path(self, end_position): # Por ahora, solo consideraremos un unico poligono caminable
        """Genera un camino hacia un punto dentro del área caminable."""
        polygon = self.walkable_areas[0] # for polygon in self.walkable_areas:
        if point_inside_polygon(end_position, polygon):
            for forb_pol in self.forbidden_areas:
                if point_inside_polygon(end_position, forb_pol):
                    return None
            return generate_path(self.main_character.position, end_position, polygon, self.forbidden_areas)
        return None

