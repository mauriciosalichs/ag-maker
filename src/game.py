import pygame
from scene import Scene
from character import Character
from object import Object
from utils import *

ASSETS_DIR = "../assets"
CHARACTERS_DIR = f"{ASSETS_DIR}/characters"
MAIN_CHARACTER_DIR = f"{CHARACTERS_DIR}/main"
BACKGROUNDS_DIR = f"{ASSETS_DIR}/backgrounds"
OBJECTS_DIR = f"{ASSETS_DIR}/objects"

# Main game class
class Game:
    def __init__(self, background, camera_width=600, camera_height=600, debug=False):
        pygame.init()
        self.mouse_pos = None
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.initial_screen = pygame.image.load(background)
        self.world_width = self.initial_screen.get_width()
        self.world_height = self.initial_screen.get_height()
        self.current_scene = Scene(self.initial_screen)
        self.debug = debug
        self.screen = pygame.display.set_mode((self.camera_width, self.camera_height))

    def run(self):
        pygame.mouse.set_visible(False)
        cursor = pygame.image.load(f"{ASSETS_DIR}/cursor.png").convert_alpha()
        world = pygame.Surface((self.world_width, self.world_height))
        camera = pygame.Rect(0, 0, self.camera_width, self.camera_height)
        # Bucle principal del juego
        running = True
        while running:
            # Control the camera with arrow keys
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                camera.x -= 5
            if keys[pygame.K_RIGHT]:
                camera.x += 5
            if keys[pygame.K_UP]:
                camera.y -= 5
            if keys[pygame.K_DOWN]:
                camera.y += 5
            if camera.left < 0:
                camera.left = 0
            if camera.right > self.world_width:
                camera.right = self.world_width
            if camera.top < 0:
                camera.top = 0
            if camera.bottom > self.world_height:
                camera.bottom = self.world_height

            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.mouse_pos = (mouse_x + camera.x, mouse_y + camera.y)
            cursor_rect = cursor.get_rect(center=(mouse_x, mouse_y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.current_scene.handle_mouse_event(self.mouse_pos)

            # Actualizar y dibujar la escena
            self.current_scene.update()
            self.current_scene.draw(world, self.debug)
            self.screen.blit(world, (0, 0), camera)
            self.screen.blit(cursor, cursor_rect)
            pygame.display.flip()

        pygame.quit()