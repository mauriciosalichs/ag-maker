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
        self.mouse_pos = None
        self.grabbed_object = None
        self.mode = DebugMode.IDLE
        

    def change_polygon(self, event = None):
        mouse_x, mouse_y = self.mouse_pos
        if self.point_selected:
            i,j = self.point_selected
            self.game.current_scene.forbidden_areas[i][j] = (mouse_x, mouse_y)
        if event == pygame.MOUSEBUTTONDOWN:
            for i, poly in enumerate(self.current_scene.forbidden_areas):
                if self.point_selected:
                    break
                for j, point in enumerate(poly):
                    if abs(mouse_x-point[0]) < 10 and abs(mouse_y-point[1]) < 10:
                        self.point_selected = (i, j)
                        print("selected",i,j)
                        break
        elif event == pygame.MOUSEBUTTONUP:
            self.point_selected = None
            
    def move_object(self, event = None):
        if self.grabbed_object:
            self.grabbed_object.position = mouse_pos
        if event == pygame.MOUSEBUTTONDOWN:
            for obj in self.current_scene.objects:
                if obj.rect.collidepoint(self.mouse_pos):
                    self.grabbed_object = obj
        elif event == pygame.MOUSEBUTTONUP:
            self.grabbed_object = None

    def perform_action(self, event = None):
        if event and event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            return
        event_type = event.type if event else None
		
        if self.mode == DebugMode.IDLE:
            return
        elif self.mode == DebugMode.CHANGE_POLYGONS:
            change_polygon(event_type)
        elif self.mode == DebugMode.MOVE_OBJECT:
            move_object(event_type)

    def run(self):
        pygame.mouse.set_visible(True)
        while self.working:
            keys = pygame.key.get_pressed()
            self.mouse_pos = pygame.mouse.get_pos()
            
            if keys[pygame.K_f]:
                self.working = False
            elif keys[pygame.K_i]:
                self.mode = DebugMode.IDLE
            elif keys[pygame.K_p]:
                self.mode = DebugMode.CHANGE_POLYGONS
            elif keys[pygame.K_a]:
                self.mode = DebugMode.ADD_OBJECT
            elif keys[pygame.K_m]:
                self.mode = DebugMode.MOVE_OBJECT
            elif keys[pygame.K_s]:
                self.mode = DebugMode.CHANGE_OBJECT_SIZE
            
            self.perform_action()
            for event in pygame.event.get():
                self.perform_action(event)
            
            # Actualizar y dibujar la escena
            self.game.current_scene.update()
            self.game.current_scene.draw(self.game.world, self.game.debug)
            self.game.screen.blit(self.game.world, (0, 0), self.game.camera)
            pygame.display.flip()
        pygame.mouse.set_visible(False)
