import pygame
from debug import Debug
from scene import Scene
from inventory import Inventory
from config import *
from utils import *
import pickle

# Main game class
class Game:
    def __init__(self, background, camera_width=600, camera_height=600, debug=False):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.main_text_font = pygame.font.SysFont("Courier", 24, bold=True)
        self.clock = pygame.time.Clock()

        self.mouse_pos = None
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.initial_screen = pygame.image.load(background)
        self.world_width = self.initial_screen.get_width()
        self.world_height = self.initial_screen.get_height()

        self.current_scene = Scene(self, self.initial_screen)
        self.screen = pygame.display.set_mode((self.camera_width, self.camera_height))
        self.cursor = pygame.image.load(f"{ASSETS_DIR}/cursor.png").convert_alpha()
        self.world = pygame.Surface((self.world_width, self.world_height))
        self.camera = pygame.Rect(0, 0, self.camera_width, self.camera_height)
        
        self.debug = Debug(self)
        self.debug_running = False
        
        inventory_image = pygame.image.load(f"{ASSETS_DIR}/inventory.png").convert_alpha()
        self.inventory = Inventory(self, inventory_image)
        self.inventory_is_open = False
        self.grabbed_object = None
        self.remaining_lines = None

        self.text_duration = 2000
        self.start_time = None
        self.text_surface = None
        self.text_rect = None

    def show_text(self, text):
        if type(text) == str:
            text = [text]
        self.remaining_lines = text[1:]
        self.show_line(text[0])

    def show_line(self, line):
        self.start_time = pygame.time.get_ticks()
        self.text_surface = self.main_text_font.render(line, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.midbottom = (self.camera_width / 2, self.camera_height - 50)

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
                
            if keys[pygame.K_ESCAPE]:
                    running = False
            if keys[pygame.K_d]:
                # Go to Debug Mode
                self.debug_running = True
                self.screen = pygame.display.set_mode((self.camera_width, self.camera_height + self.debug.height))
                self.debug.ceil = self.camera_height
                self.debug.rect = pygame.Rect(0, self.camera_height, self.camera_width, self.debug.height)
                self.debug.go_to_idle()
                self.debug.run()
                # Screen go back to normal after Debugging
                self.screen = pygame.display.set_mode((self.camera_width, self.camera_height))
                self.debug_running = False
            if keys[pygame.K_i]:
                self.inventory_is_open = not self.inventory_is_open

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    tmp_og = self.grabbed_object
                    if self.inventory_is_open:
                        self.inventory.handle_click(self.mouse_pos, event.button, self.grabbed_object)
                    else:
                        self.current_scene.handle_click(self.mouse_pos, event.button, self.grabbed_object)
                    if tmp_og and event.button == 3:
                        self.grabbed_object = None
                
            # Actualizar y dibujar la escena
            self.current_scene.update()
            self.current_scene.draw(self.world)
            self.screen.blit(self.world, (0, 0), self.camera)
            
            if self.inventory_is_open:
                self.inventory.show()

            if self.text_surface:
                if pygame.time.get_ticks() - self.start_time < self.text_duration:
                    background_rect = pygame.Rect(self.text_rect.left - 10, self.text_rect.top - 5,
                                                  self.text_rect.width + 20, self.text_rect.height + 10)
                    pygame.draw.rect(self.screen, (255, 255, 255, 50), background_rect)
                    self.screen.blit(self.text_surface, self.text_rect)
                else:
                    if self.remaining_lines:
                        line = self.remaining_lines[0]
                        self.remaining_lines = self.remaining_lines[1:]
                        self.show_line(line)
                    else:
                        self.text_surface = None

            if self.grabbed_object:
                img = self.grabbed_object.image.copy()
                img,rect = rescale_to_rect(img, size=130)
                img.set_alpha(180)
                rect.center=(mouse_x, mouse_y)
                self.screen.blit(img, rect)
            
            self.screen.blit(self.cursor, cursor_rect)
            pygame.display.flip()

        pygame.quit()
