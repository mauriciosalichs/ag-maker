import pygame
from debug import Debug
from scene import Scene
from inventory import Inventory
from config import *
import pickle

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
        
        self.debug = Debug(self)
        self.debug_running = False
        
        inventory_image = pygame.image.load(f"{ASSETS_DIR}/inventory.png").convert_alpha()
        self.inventory = Inventory(self, inventory_image)
        self.inventory_is_open = False
        

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
            	self.inventory_is_open = not self.inventory_is_open =

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                	if self.inventory_is_open:
                		self.handle_inventory_click(self.mouse_pos, event.button) # CHECK IF THE CAMERA IS IMPORTANT HERE
                	else:
                		self.current_scene.handle_click(self.mouse_pos, event.button)

            # Actualizar y dibujar la escena
            self.current_scene.update()
            self.current_scene.draw(self.world)
            self.screen.blit(self.world, (0, 0), self.camera)
            
            if self.inventory_is_open:
            	self.inventory.show()
            
            self.screen.blit(self.cursor, cursor_rect)
            pygame.display.flip()

        pygame.quit()
