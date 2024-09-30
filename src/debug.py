import pygame
import os
from enum import Enum
from config import *
from utils import *
from object import Object

class DebugMode(Enum):
    IDLE = 0
    ADD_WALKABLE_POLYGON = 1
    ADD_FORBIDDEN_POLYGON = 2
    MODIFY_POLYGON = 3
    ADD_OBJECT = 4
    MODIFY_OBJECT = 5

menu_text = [
    "Welcome to debug mode (Press I for go back to this menu):",
    "A - Add Object, M - Modify Object, N-M - Change Object Size",
    "W - Add Walk Polygon, F - Add Forbidden Polygon, P - Modify Polygon",
    "Q - Exit Debug Mode"
]

class Debug:
    def __init__(self, game):
        self.game = game
        self.mode = DebugMode.IDLE
        self.height = 100
        self.rect = None

        # Text and fonts
        self.font = pygame.font.Font(None, 23)
        self.text_adding_objects = self.font.render("Adding objects...", True, (255,255,255))
        self.text_modify_polygon = self.font.render("Click on a point of the polygon to move it, or click on a line to create a new point.", True, (255,255,255))

        # Common variables
        self.ceil = None
        self.mouse_x = None
        self.mouse_y = None
        self.old_x = None
        self.old_y = None

        # Polygons
        self.tmp_polygon = []
        self.new_polygon = []
        self.point_selected = None

        # Add object
        self.object_imgs = None
        self.new_object_image = None
        self.new_object_name = None
        self.scale_factor = 1.0

        # Modify object
        self.grabbed_object = None

    def go_to_idle(self):
        self.mode = DebugMode.IDLE
        pygame.draw.rect(self.game.screen, (0,0,0), self.rect)
        line_spacing = 5  # Espaciado entre líneas
        total_height = sum([self.font.size(line)[1] for line in menu_text]) + (line_spacing * (len(menu_text) - 1))
        y_offset = self.rect.y + (self.rect.height - total_height) // 2  # Centrar verticalmente
        for line in menu_text:
            text_surface = self.font.render(line, True, (255,255,255))
            text_rect = text_surface.get_rect(center=(self.rect.centerx, y_offset))
            self.game.screen.blit(text_surface, text_rect)
            y_offset += self.font.size(line)[1] + line_spacing  # Siguiente línea

    def load_imgs(self):
        pygame.draw.rect(self.game.screen, (0, 0, 0), self.rect)
        text_adding_objects_rect = self.text_adding_objects.get_rect(center=self.rect.center)
        self.game.screen.blit(self.text_adding_objects, text_adding_objects_rect)
        self.object_imgs = []
        obj_imgs = [f for f in os.listdir(OBJECTS_DIR) if os.path.splitext(f)[1].lower() == '.png']
        for img_file in obj_imgs:
            img = pygame.image.load(f"{OBJECTS_DIR}/{img_file}")
            name = img_file.split('.')[0]
            rect = pygame.Rect(len(self.object_imgs)*self.height, self.ceil, self.height, self.height)
            self.object_imgs.append((name, img))
            image_width, image_height = img.get_size()
            scale_w = rect.width / image_width
            scale_h = rect.height / image_height
            scale = min(scale_w, scale_h)  # Elegir la escala más pequeña para mantener la relación de aspecto
            # Calcular el nuevo tamaño de la imagen
            new_size = (int(image_width * scale), int(image_height * scale))
            # Redimensionar la imagen
            img = pygame.transform.scale(img, new_size)
            # Encontrar la posición para centrar la imagen dentro del rectángulo
            resized_rect = img.get_rect(center=rect.center)
            self.game.screen.blit(img, resized_rect)
            name_text = self.font.render(name, True, (255, 255, 255))
            self.game.screen.blit(name_text, resized_rect)

    def add_polygon(self, event=None):
    	text_modify_polygon_rect = self.text_modify_polygon.get_rect(center=self.rect.center)
        self.game.screen.blit(self.text_modify_polygon, text_modify_polygon_rect)
        if event == pygame.MOUSEBUTTONDOWN:
            if self.new_polygon:
                px, py = self.new_polygon[0]
                if abs(self.mouse_x - px) < 10 and abs(self.mouse_y - py) < 10:
                    # Adjust polygon for no-debug mode
                    new_polygon = [(x+self.game.camera.x, y+self.game.camera.y) for (x,y)
                                   in self.new_polygon]
                    self.game.current_scene.forbidden_areas.append(new_polygon)
                    self.tmp_polygon = []
                    self.new_polygon = []
                    self.go_to_idle()
                    return
            self.new_polygon.append((self.mouse_x, self.mouse_y))
        else:
            if not self.new_polygon:
                return
            else:
                self.tmp_polygon = self.new_polygon + [(self.mouse_x, self.mouse_y)]

    def add_object(self, event = None):
        if event == pygame.MOUSEBUTTONDOWN:
            if self.new_object_image and self.mouse_y < self.ceil:
                scaled_image = pygame.transform.scale(self.new_object_image, (
                    int(self.new_object_image.get_rect().width * self.scale_factor),
                    int(self.new_object_image.get_rect().height * self.scale_factor)))
                obj = Object(self.game, None, self.new_object_name, "", scaled_image)
                # Adjust to no-debug world
                px, py = self.mouse_x + self.game.camera.x, self.mouse_y + self.game.camera.y
                self.game.current_scene.add_object(obj, (px, py))
                fp = [obj.rect.topleft,obj.rect.topright,obj.rect.bottomright,obj.rect.bottomleft]
                self.game.current_scene.forbidden_areas.append(fp)
                self.new_object_image = None
                self.go_to_idle()
            elif self.mouse_y > self.ceil and self.mouse_x < len(self.object_imgs)*self.height:
                self.scale_factor = 1.0
                i = int(self.mouse_x / self.height)
                self.new_object_name, self.new_object_image = self.object_imgs[i]
                print(self.new_object_image)

    def modify_polygon(self, event = None):
        if self.point_selected:
            i,j = self.point_selected
            self.game.current_scene.forbidden_areas[i][j] = (self.mouse_x, self.mouse_y)
        if event == pygame.MOUSEBUTTONDOWN:
            for i, poly in enumerate(self.game.current_scene.forbidden_areas):
                if self.point_selected:
                    break
                for j, point in enumerate(poly):
                    if abs(self.mouse_x-point[0]) < 10 and abs(self.mouse_y-point[1]) < 10:
                        self.point_selected = (i, j)
                        break
            # If none of the vertices were selected, try with the lines
            if not self.point_selected:
                for i, poly in enumerate(self.game.current_scene.forbidden_areas):
                    # TODO: Fix problem, is not being able to detect collision after first point of the poly
                    j = point_near_polygon(self.mouse_x, self.mouse_y, poly)
                    if j:
                        # Adjust to no-debug world
                        px,py = self.mouse_x + self.game.camera.x, self.mouse_y + self.game.camera.y
                        self.game.current_scene.forbidden_areas[i].insert(j+1, (px,py))
                        self.point_selected = (i,j+1)
        elif event == pygame.MOUSEBUTTONUP:
            self.point_selected = None
            
    def move_object(self, event = None):
        if self.grabbed_object:
            dx = self.mouse_x - self.old_x
            dy = self.mouse_y - self.old_y
            ox, oy = self.grabbed_object.position
            self.grabbed_object.set_position((ox+dx, oy+dy))
            self.old_x = self.mouse_x
            self.old_y = self.mouse_y
        if event == pygame.MOUSEBUTTONDOWN:
            for obj in self.game.current_scene.objects:
                if obj.rect.collidepoint((self.mouse_x,self.mouse_y)):
                    print("selected",obj.name)
                    self.grabbed_object = obj
                    self.old_x = self.mouse_x
                    self.old_y = self.mouse_y
        elif event == pygame.MOUSEBUTTONUP:
            self.grabbed_object = None

    def perform_action(self, event = None):
        if event and event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            return
        event_type = event.type if event else None
		
        if self.mode == DebugMode.IDLE:
            return
        elif self.mode == DebugMode.ADD_FORBIDDEN_POLYGON:
            self.add_polygon(event_type)
        elif self.mode == DebugMode.MODIFY_POLYGON:
            self.modify_polygon(event_type)
        elif self.mode == DebugMode.ADD_OBJECT:
            self.add_object(event_type)
        elif self.mode == DebugMode.MODIFY_OBJECT:
            self.move_object(event_type)

    def run(self):
        pygame.mouse.set_visible(True)
        running = True
        print(f"Running debug with ceil {self.ceil}")
        while running:
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            self.mouse_x = mouse_pos[0]# + self.game.camera.x
            self.mouse_y = mouse_pos[1]# + self.game.camera.y
            
            if keys[pygame.K_q]:
                running = False
            elif keys[pygame.K_i] and self.mode != DebugMode.IDLE:
                print("DEBUG MODE: IDLE")
                self.go_to_idle()
            elif keys[pygame.K_w] and self.mode != DebugMode.ADD_WALKABLE_POLYGON:
                print("DEBUG MODE: ADD_WALKABLE_POLYGON")
                pygame.draw.rect(self.game.screen, (0,0,0), self.rect)
                self.mode = DebugMode.ADD_WALKABLE_POLYGON
            elif keys[pygame.K_f] and self.mode != DebugMode.ADD_FORBIDDEN_POLYGON:
                print("DEBUG MODE: ADD_FORBIDDEN_POLYGON")
                pygame.draw.rect(self.game.screen, (0,0,0), self.rect)
                self.mode = DebugMode.ADD_FORBIDDEN_POLYGON
            elif keys[pygame.K_p] and self.mode != DebugMode.MODIFY_POLYGON:
                print("DEBUG MODE: MODIFY POLYGON")
                pygame.draw.rect(self.game.screen, (0,0,0), self.rect)
                self.mode = DebugMode.MODIFY_POLYGON
            elif keys[pygame.K_a] and self.mode != DebugMode.ADD_OBJECT:
                print("DEBUG MODE: ADD OBJECT")
                self.load_imgs()
                self.mode = DebugMode.ADD_OBJECT
            elif keys[pygame.K_m] and self.mode != DebugMode.MODIFY_OBJECT:
                print("DEBUG MODE: MOVE OBJECT")
                pygame.draw.rect(self.game.screen, (0,0,0), self.rect)
                self.mode = DebugMode.MODIFY_OBJECT
            elif keys[pygame.K_n] and self.new_object_image and self.scale_factor > 0.01:
                self.scale_factor -= 0.01
            elif keys[pygame.K_m] and self.new_object_image:
                self.scale_factor += 0.01
            
            self.perform_action()
            for event in pygame.event.get():
                self.perform_action(event)
            
            # Actualizar y dibujar la escena
            self.game.current_scene.update()
            self.game.current_scene.draw(self.game.world, self.game.debug)
            self.game.screen.blit(self.game.world, (0, 0), self.game.camera)

            if self.new_object_image and self.mouse_y < self.ceil:
                scaled_image = pygame.transform.scale(self.new_object_image, (
                 int(self.new_object_image.get_rect().width * self.scale_factor),
                 int(self.new_object_image.get_rect().height * self.scale_factor)))
                print("mouse x",self.mouse_x,"mouse y",self.mouse_y)
                rect = scaled_image.get_rect(midbottom=(self.mouse_x,self.mouse_y))
                self.game.screen.blit(scaled_image, rect.topleft)

            if self.tmp_polygon:
                pygame.draw.polygon(self.game.screen, (255,0,0), self.tmp_polygon, 3)
            	
            pygame.display.flip()
        pygame.mouse.set_visible(False)
