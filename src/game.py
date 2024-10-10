import pygame
from src.debug import Debug
from src.scene import Scene
from src.inventory import Inventory
from src.conversation import Conversation
from src.utils import *

# Main game class
class Game:
    def __init__(self, camera_width=600, camera_height=600, cursor_img_path=None):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.main_text_font = pygame.font.SysFont("Courier", 24, bold=True)
        self.clock = pygame.time.Clock()

        self.mouse_pos = None
        self.mouse_camera_pos = None
        self.camera_width = camera_width
        self.camera_height = camera_height

        self.screen = pygame.display.set_mode((self.camera_width, self.camera_height))
        self.camera = pygame.Rect(0, 0, self.camera_width, self.camera_height)
        self.cursor = pygame.image.load(cursor_img_path).convert_alpha() if cursor_img_path else None

        self.current_scene = None
        self.world_width = None
        self.world_height = None
        self.world = None

        self.debug = None
        self.debug_running = False

        self.inventory = None
        self.inventory_is_open = False
        self.grabbed_object = None

        # Subtitles of dialogue
        self.current_color = None
        self.remaining_lines = None
        self.text_duration = 2000
        self.start_time = None
        self.text_surface = None
        self.text_rect = None

        # Things still not implemented
        self.conversation = None
        self.actions = None
        self.action_in_place = False
        self.choose_response = False

    # Set other components of the game

    def set_actions(self, actions):
        self.actions = actions
        
    def start_conversation(self, character):
        self.conversation = Conversation(self, character)
        self.conversation.start()

    def current_action_finished(self):
        self.actions.continue_current_actions()
        if self.conversation:
            self.current_color = None
            self.conversation.answer()

    def set_inventory(self, inventory):
        self.inventory = inventory

    def set_scene(self, scene):
        self.current_scene = scene
        self.world_width = scene.width
        self.world_height = scene.height
        self.world = pygame.Surface((self.world_width, self.world_height))

    # Define some main actions game-wide

    def grab_object(self, obj):
        if self.actions.allowGrab(obj.id):
            self.inventory.add_item(obj)
            self.current_scene.objects.remove(obj)
            return True
        else:
            return False

    def use_object(self, obj_id):
        return self.actions.allowUse(obj_id)

    def use_object_with_target(self, obj_id, target_id):
        return self.actions.allowUseWithTarget(obj_id, target_id)
        
    def check_for_actions_about_conversation(self, char_id, text_id):
        return self.actions.checkForConversationId(char_id, text_id)

    # TODO: def playAnimation(self, animation):

    # Show a line of dialogue as a subtitle

    def show_line(self, line, color=(0,0,0)):
        self.start_time = pygame.time.get_ticks()
        self.text_surface = self.main_text_font.render(line, True, color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.midbottom = (self.camera_width / 2, self.camera_height - 50)

    def show_text(self, text, color=(0,0,0)):
        if type(text) == str:
            text = [text]
        self.remaining_lines = text[1:]
        self.current_color = color
        self.show_line(text[0], color)

    # Handle mouse click and redirect to appropiate component

    def handle_click(self, button):
        if self.action_in_place:     # wherever we have a running animation or any
            return                  # other special event, we ignore the click
        if self.choose_response:
            self.conversation.handle_click(self.mouse_camera_pos)
        tmp_og = self.grabbed_object
        if self.inventory_is_open:
            self.inventory.handle_click(self.mouse_pos, button, self.grabbed_object)
        else:
            self.current_scene.handle_click(self.mouse_pos, button, self.grabbed_object)
        if tmp_og and button == 3:
            self.grabbed_object = None

    def run(self):
        # Main Loop
        running = True
        while running:
            keys = pygame.key.get_pressed()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.mouse_camera_pos = (mouse_x, mouse_y)

            # Camera reposition
            mc_x, mc_y = self.current_scene.main_character.position
            mc_x -= self.camera.x
            mc_y -= self.camera.y
            if mc_x < 300:
                self.camera.x -= 1
            if mc_x > self.camera_width - 300:
                self.camera.x += 1
            if mc_y < 300:
                self.camera.y -= 1
            if mc_y > self.camera_height - 300:
                self.camera.y += 1
            if self.camera.left < 0:
                self.camera.left = 0
            if self.camera.right > self.world_width:
                self.camera.right = self.world_width
            if self.camera.top < 0:
                self.camera.top = 0
            if self.camera.bottom > self.world_height:
                self.camera.bottom = self.world_height

            # Adjust the position of the cursor to the camera
            self.mouse_pos = (mouse_x + self.camera.x, mouse_y + self.camera.y)
            cursor_rect = self.cursor.get_rect(center=(mouse_x, mouse_y)) if self.cursor else None

            if not (self.action_in_place or self.choose_response):
                if keys[pygame.K_ESCAPE]:
                        running = False
                if keys[pygame.K_d]:
                    if self.debug:
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
                # Other keys...

            # Handle mouse click
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.button)
                
            # We update the scene and then draw everything in a specific order

            # We update the scene and the world inside the camera view
            self.current_scene.update()
            self.current_scene.draw(self.world)
            self.screen.blit(self.world, (0, 0), self.camera)

            # If the inventory is open, we show it now
            # TODO: Close it when there is a grabbed object and the mouse is outside of the inventory rect
            if self.inventory_is_open:
                self.inventory.show()

            # If there is text to show as subtitles, we show it now
            if self.text_surface:
                if pygame.time.get_ticks() - self.start_time < self.text_duration:
                    background_rect = pygame.Rect(self.text_rect.left - 10, self.text_rect.top - 5,
                                                  self.text_rect.width + 20, self.text_rect.height + 10)
                    pygame.draw.rect(self.screen, (255, 255, 255, 50), background_rect)
                    #pygame.draw.rect(self.screen, (255, 0, 0), background_rect, 2)
                    self.screen.blit(self.text_surface, self.text_rect)
                else:
                    if self.remaining_lines:
                        line = self.remaining_lines[0]
                        self.remaining_lines = self.remaining_lines[1:]
                        self.show_line(line, self.current_color)
                    else:
                        self.text_surface = None
                        self.current_action_finished()

            # If there is a grabbed object, we show it now
            if self.grabbed_object:
                img = self.grabbed_object.image.copy()
                img,rect = rescale_to_rect(img, size=130)
                img.set_alpha(180)
                rect.center=(mouse_x, mouse_y)
                self.screen.blit(img, rect)

            # We show the name of whichever element is being pointed
            tmpy = 0
            x, y = self.mouse_pos
            pointed_e = None
            for e in self.current_scene.objects + self.current_scene.characters:
                if e.area_includes(x, y):
                    if e.position and e.position[1] > tmpy:
                        pointed_e = e
                        tmpy = e.position[1]
            if pointed_e:
                pointed_e.text_rect.centerx = mouse_x
                pointed_e.text_rect.bottom = mouse_y - 20
                self.screen.blit(pointed_e.text_surface, pointed_e.text_rect)
                
            # We show response options, if any
            if self.choose_response:
                self.conversation.draw_options(self.screen)

            if self.cursor: self.screen.blit(self.cursor, cursor_rect)
            pygame.display.flip()

        pygame.quit()
