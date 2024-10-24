import pygame
from src.utils import *

class Object:
    def __init__(self, game, id, data, image=None):
        self.game = game
        self.id = id

        if image:
            self.image = image
        elif "imageDir" in data.keys():
            self.image = pygame.image.load(data["imageDir"]).convert_alpha()
        else:
            self.image = None

        self.name = data["name"]
        self.description = data["description"]
        self.grab_description = data["grabDescription"] if "grabDescription" in data.keys() else None

        self.position = None
        self.rect = None
        self.interact_position = None  # [x,y,side]

        self.font = pygame.font.SysFont("Courier", 24, bold=True)
        self.text_surface = self.font.render(self.name, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
        self.not_usable_text = data["notUsable"] if "notUsable" in data.keys() else ""
        
        # Logic properties of an object
        self.position_to_interact = None
        self.is_place = ("place" in data["properties"])
        self.is_grabbable = ("grabbable" in data["properties"])
        self.is_in_inventory = ("in_inventory" in data["properties"])
        self.standalone_use = ("standalone_use" in data["properties"])

    def change_name(self, name):
        self.name = name
        self.game.objects_data[self.id]['name'] = name
        self.text_surface = self.font.render(self.name, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
        self.game.current_action_finished(f"change_name {name}")

    def change_description(self, description):
        self.description = description
        self.game.objects_data[self.id]['description'] = description
        self.game.current_action_finished(f"change_description {description}")

    def area_includes(self, x, y):
        if self.is_place:	# Object inherent of the scene
            return euclidean_distance((x,y), self.position) < 100
        if not self.rect.collidepoint((x, y)):
            return False
        fix_x = x - self.rect.left
        fix_y = y - self.rect.top
        return self.image.get_at((fix_x, fix_y)).a > 0

    def set_position(self, position):
        self.position = position
        if self.image:
            self.rect = self.image.get_rect(midbottom=position)

    def observe(self):
        self.game.show_text(self.description)

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
        elif euclidean_distance(self.game.main_character.position, self.position) > 100:
            self.game.show_text(f"Estoy demasiado lejos.")
        else:
            self.use_(grabbed_object)

    def use_(self, grabbed_object=None):
        if (not grabbed_object) and self.is_grabbable:
            if self.game.grab_object(self):
                self.game.show_text(self.grab_description if self.grab_description else f"COJEMOS {self.name}")
        else:
            if grabbed_object:
                if not self.game.use_object_with_target(self.id, grabbed_object.id):
                    self.game.show_text("No se porque haría eso.")
            elif not self.game.use_object(self.id):
                if self.not_usable_text:
                    self.game.show_text(self.not_usable_text)
                else:
                    self.game.show_text("No se porque haría eso.")
        # self.game.current_action_finished(f"using {self.id}")
        
    def draw(self, screen):
        """Dibuja el objeto en la pantalla, excepto si esta dentro de la escena misma."""
        if self.image:
            if self.game.debug_running:
                self.image.set_alpha(100)
            else:
                self.image.set_alpha(255)
            screen.blit(self.image, self.rect.topleft)
