import pygame
from scene import Scene
import pickle

ASSETS_DIR = "../assets"
CHARACTERS_DIR = f"{ASSETS_DIR}/characters"
MAIN_CHARACTER_DIR = f"{CHARACTERS_DIR}/main"
BACKGROUNDS_DIR = f"{ASSETS_DIR}/backgrounds"
OBJECTS_DIR = f"{ASSETS_DIR}/objects"

# Main game class
class Game:
    def __init__(self, background, camera_width=600, camera_height=600, debug=False):
        pygame.init()
        pygame.mouse.set_visible(False)

        self.mouse_pos = None
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.initial_screen = pygame.image.load(background)
        self.world_width = self.initial_screen.get_width()
        self.world_height = self.initial_screen.get_height()

        self.current_scene = Scene(self.initial_screen)
        self.screen = pygame.display.set_mode((self.camera_width, self.camera_height))
        self.cursor = pygame.image.load(f"{ASSETS_DIR}/cursor.png").convert_alpha()
        self.world = pygame.Surface((self.world_width, self.world_height))
        self.camera = pygame.Rect(0, 0, self.camera_width, self.camera_height)
        
        # Debug Mode
        self.debug = debug
        self.point_selected = None

    def debug_mode(self, keys, mouse_pos, event = None):
        mouse_x, mouse_y = mouse_pos
        if self.point_selected:
            i,j = self.point_selected
            self.current_scene.forbidden_areas[i][j] = (mouse_x, mouse_y)
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
            

    def handle_mouse_click(self, mouse_pos):
        if self.debug:
            self.debug_mode([], mouse_pos, pygame.MOUSEBUTTONDOWN)
        else:
            self.current_scene.handle_mouse_event(mouse_pos)
    	  
    def handle_mouse_release(self, mouse_pos):
        if self.debug:
            self.debug_mode([], mouse_pos, pygame.MOUSEBUTTONUP)
        else:
            pass

    def run(self):
        # Bucle principal del juego
        running = True
        while running:
            keys = pygame.key.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Camera control
            mc_x, mc_y = self.current_scene.main_character.position
            mc_x -= self.camera.x
            mc_y -= self.camera.y
            if keys[pygame.K_LEFT] or mc_x < 300:
                self.camera.x -= 1
            if keys[pygame.K_RIGHT] or mc_x > self.camera_width - 300:
                self.camera.x += 1
            if keys[pygame.K_UP] or mc_y < 300:
                self.camera.y -= 1
            if keys[pygame.K_DOWN] or mc_y > self.camera_height - 300:
                self.camera.y += 1
            if self.camera.left < 0:
                self.camera.left = 0
            if self.camera.right > self.world_width:
                self.camera.right = self.world_width
            if self.camera.top < 0:
                self.camera.top = 0
            if self.camera.bottom > self.world_height:
                self.camera.bottom = self.world_height
                
            self.mouse_pos = (mouse_x + self.camera.x, mouse_y + self.camera.y)
            cursor_rect = self.cursor.get_rect(center=(mouse_x, mouse_y))
                
            if keys[pygame.K_q]:
                    running = False
            if keys[pygame.K_d]:
                if self.debug:
                    self.debug = False
                    self.screen = pygame.display.set_mode((self.camera_width, self.camera_height))
                else:
                    self.debug = True
                    self.screen = pygame.display.set_mode((self.camera_width, self.camera_height+200))
            # Actions to perform in Debug Mode:
            if self.debug:
               self.debug_mode(keys, self.mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(self.mouse_pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_release(self.mouse_pos)

            # Actualizar y dibujar la escena
            self.current_scene.update()
            self.current_scene.draw(self.world, self.debug)
            self.screen.blit(self.world, (0, 0), self.camera)
            self.screen.blit(self.cursor, cursor_rect)
            pygame.display.flip()

        pygame.quit()
