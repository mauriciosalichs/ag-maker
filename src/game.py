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
        self.debug = debug

    def change_polygon(self):
        running = True
        point = None
        point_selected = False
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.mouse_pos = (mouse_x + self.camera.x, mouse_y + self.camera.y)
            cursor_rect = self.cursor.get_rect(center=(mouse_x, mouse_y))

            if point_selected:
                self.current_scene.forbidden_areas[ind_i][ind_j] = (mouse_x, mouse_y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, poly in enumerate(self.current_scene.forbidden_areas):
                        if point_selected:
                            break
                        for j, point in enumerate(poly):
                            if abs(mouse_x-point[0]) < 10 and  abs(mouse_y-point[1]) < 10:
                                point_selected = True
                                ind_i, ind_j = i, j
                                print("selected",i,j)
                                break
                elif event.type == pygame.MOUSEBUTTONUP:
                    point_selected = False
                    point = None

            # Actualizar y dibujar la escena
            self.current_scene.update()
            self.current_scene.draw(self.world, self.debug)
            self.screen.blit(self.world, (0, 0), self.camera)
            self.screen.blit(self.cursor, cursor_rect)
            pygame.display.flip()


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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open("game.pkl", "wb") as file:
                        pickle.dump(self, file)
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.current_scene.handle_mouse_event(self.mouse_pos)

            # Actualizar y dibujar la escena
            self.current_scene.update()
            self.current_scene.draw(self.world, self.debug)
            self.screen.blit(self.world, (0, 0), self.camera)
            self.screen.blit(self.cursor, cursor_rect)
            pygame.display.flip()

        pygame.quit()