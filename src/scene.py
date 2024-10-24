import os
from src.utils import *

class Scene:
    def __init__(self, game, id, data):
        self.game = game
        self.id = id
        self.background_image = pygame.image.load(data['backgroundDir'])
        self.background_music = pygame.mixer.Sound(f'assets/sounds/{id}.mp3') if os.path.exists(f'assets/sounds/{id}.mp3') else None
        self.width = self.background_image.get_width()
        self.height = self.background_image.get_height()

        self.is_map = data['isMap'] if 'isMap' in data.keys() else False
        self.marks = data['marks'] if 'marks' in data.keys() else []
        self.selected_mark = None

        self.walkable_areas = data['walkableAreas'] if 'walkableAreas' in data.keys() else []
        self.forbidden_areas = data['forbiddenAreas'] if 'forbiddenAreas' in data.keys() else []
        self.objects = []  # Lista de objetos en la escena
        self.characters = []  # Lista de personajes en la escena
        self.main_character = None
        self.walkable_path = None
        self.dialogue_sound = dict()

        self.walkable_graph = create_walkable_graph(self.walkable_areas, self.forbidden_areas)

    def add_walkable_area(self, polygon):
        """Añade un área caminable definida por un polígono."""
        self.walkable_areas.append(polygon)
        self.walkable_graph = create_walkable_graph(self.walkable_areas, self.forbidden_areas)
        
    def add_forbidden_area(self, polygon):
        """Añade un área pohibida definida por un polígono."""
        self.forbidden_areas.append(polygon)
        self.walkable_graph = create_walkable_graph(self.walkable_areas, self.forbidden_areas)
    
    def add_object(self, game_object, data=None):
        """Añade un objeto a la escena en una posición específica."""
        if data:
            game_object.set_position(data[1]) # Rectángulo de colisión
            game_object.interact_position = data[2] if len(data) > 2 else None
        self.objects.append(game_object)
    
    def add_character(self, character, data):
        """Añade un personaje a la escena en una posición específica."""
        if not self.characters:
            self.main_character = character
            self.game.main_character = character
        character.position = data[1]  # Inicializar la posición del personaje
        character.interact_position = data[2] if len(data) > 2 else None
        character.rect = character.image.get_rect(midbottom=character.position)  # Rectángulo de colisión
        self.characters.append(character)
        self.dialogue_sound[freq_to_col(character.dialogue_color)] = character.dialogue_sound
    
    def draw(self, screen, debug = False):
        """Dibuja la escena en la pantalla."""
        screen.blit(self.background_image, (0, 0))
        
        # DEBUG: Dibuja los poligonos
        if debug:
            for walkable in self.walkable_areas:
                pygame.draw.polygon(screen, (0,0,255), walkable, 3)
            for forbidden in self.forbidden_areas:
                pygame.draw.polygon(screen, (255,0,0), forbidden, 3)
            if self.walkable_path:
                pygame.draw.lines(screen, (0,255,0), False, self.walkable_path, 3)
        
        main_char_drawn = False
        for obj in self.objects + self.characters[1:]:
            if not main_char_drawn and obj.rect and \
               self.main_character.rect.colliderect(obj.rect) and \
               self.main_character.position[1] < obj.position[1]:
                # El objeto debe aparecer adelante, entonces el personaje se dibujara primero
                # TODO: Tener un poligono asociado a cada objeto, y calcular en base al POLIGONO
                self.main_character.draw(screen)
                main_char_drawn = True
            obj.draw(screen)
        if self.main_character and not main_char_drawn:		# Si el personaje aun no fue dibujado, lo hacemos aquí
            self.main_character.draw(screen)
    
    def update(self):
        for character in self.characters:
            character.update()
        # Something else to update?
    
    def handle_click(self, position, button, selected_object):
        x,y = position
        if button == 1: 	# Left click
            if self.is_map:
                print("clicking in map at",position)
                return
            for char in self.characters:
                if char.area_includes(x, y):
                    char.observe()
                    return
            for obj in self.objects:
                if obj.area_includes(x,y):
                    obj.observe()
                    return
            # No object or character clicked, then we try to walk
            self.walk_to(self.main_character, position)

        elif button == 3: 	# Right click
            if self.is_map:
                if self.selected_mark:
                    self.game.change_scene(self.selected_mark)
                return
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

    def walk_to(self, character, position):
        self.walkable_path = self.gen_walkable_path(position)
        if self.walkable_path:
            character.move_to(self.walkable_path[1])
            if len(self.walkable_path) > 2:
                character.walking_path = self.walkable_path[2:]
        else:
            self.game.current_action_finished(f"NOT POSSIBLE TO WALK {character.id} TO {position}")

    def gen_walkable_path(self, end_position): # Por ahora, solo consideraremos un unico poligono caminable
        """Genera un camino hacia un punto dentro del área caminable."""
        polygon = self.walkable_areas[0] # for polygon in self.walkable_areas...
        if point_inside_polygon(end_position, polygon):
            for forb_pol in self.forbidden_areas:
                if point_inside_polygon(end_position, forb_pol):
                    return None
            return calculate_path(tuple(self.main_character.position), tuple(end_position),
                                  self.walkable_graph, self.walkable_areas, self.forbidden_areas)
        return None