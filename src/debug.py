import pygame
from enum import Enum

class DebugMode(Enum):
    IDLE = 0
    CHANGE_POLYGONS = 1
    ADD_OBJECT = 2
    MOVE_OBJECT = 3
    CHANGE_OBJECT_SIZE = 4

class Debug:
    def __init__(self, game):
        self.game = game
        self.working = False
        self.point_selected = None
        self.mouse_x = None
        self.mouse_y = None
        self.old_x = None
        self.old_y = None
        self.grabbed_object = None
        self.mode = DebugMode.IDLE
        self.new_object_image = None
        
    def open_file(self):
        try:
            import pyperclip
        except:
            print("No tienes instalado pyperclip")
            return
        try:
            clipboard_content = pyperclip.paste()
            self.new_object_image = pygame.image.load(clipboard_content).convert_alpha()
        except:
           print("No has copiado la ruta de una imagen")
           return
		
    def change_polygon(self, event = None):
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
        elif self.mode == DebugMode.CHANGE_POLYGONS:
            self.change_polygon(event_type)
        elif self.mode == DebugMode.MOVE_OBJECT:
            self.move_object(event_type)

    def run(self):
        pygame.mouse.set_visible(True)
        while self.working:
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            self.mouse_x = mouse_pos[0] + self.game.camera.x
            self.mouse_y = mouse_pos[1] + self.game.camera.y
            
            if keys[pygame.K_f]:
                self.working = False
            elif keys[pygame.K_i] and self.mode != DebugMode.IDLE:
                print("DEBUG MODE: IDLE")
                self.mode = DebugMode.IDLE
            elif keys[pygame.K_p] and self.mode != DebugMode.CHANGE_POLYGONS:
                print("DEBUG MODE: CHANGE POLYGONS")
                self.mode = DebugMode.CHANGE_POLYGONS
            elif keys[pygame.K_a] and self.mode != DebugMode.ADD_OBJECT:
                print("DEBUG MODE: ADD OBJECT")
                img_path = self.open_file()
                self.mode = DebugMode.ADD_OBJECT
            elif keys[pygame.K_m] and self.mode != DebugMode.MOVE_OBJECT:
                print("DEBUG MODE: MOVE OBJECT")
                self.mode = DebugMode.MOVE_OBJECT
            elif keys[pygame.K_s] and self.mode != DebugMode.CHANGE_OBJECT_SIZE:
                print("DEBUG MODE: CHANGE OBJECT SIZE")
                self.mode = DebugMode.CHANGE_OBJECT_SIZE
            
            self.perform_action()
            for event in pygame.event.get():
                self.perform_action(event)
            
            # Actualizar y dibujar la escena
            self.game.current_scene.update()
            self.game.current_scene.draw(self.game.world, self.game.debug)
            self.game.screen.blit(self.game.world, (0, 0), self.game.camera)
            
            if self.new_object_image:
                rect = self.new_object_image.get_rect(midbottom=(self.mouse_x,self.mouse_y))
                self.game.screen.blit(self.new_object_image, rect.topleft)
            	
            pygame.display.flip()
        pygame.mouse.set_visible(False)
