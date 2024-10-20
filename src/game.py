from src.scene import Scene
from src.character import Character
from src.object import Object
from src.conversation import Conversation
from src.utils import *

# Main game class
class Game:
    def __init__(self, data, s_data, ch_data, o_data, cv_data, cursor_img_path=None):
        pygame.init()
        pygame.mixer.init()
        pygame.mouse.set_visible(False)
        self.main_text_font = pygame.font.SysFont("Courier", 18, bold=True)
        self.clock = pygame.time.Clock()

        self.id = data["id"]
        self.mouse_pos = None
        self.mouse_camera_pos = None
        self.camera_width = data["cameraWidth"]
        self.camera_height = data["cameraHeight"]

        self.screen = pygame.display.set_mode((self.camera_width, self.camera_height))
        self.camera = pygame.Rect(0, 0, self.camera_width, self.camera_height)
        self.cursor = pygame.image.load(cursor_img_path).convert_alpha() if cursor_img_path else None

        self.scenes = dict()
        self.current_scene = None
        self.current_scene_id = data['currentScene']
        self.world_width = None
        self.world_height = None
        self.world = None

        self.main_character = None

        self.debug = None
        self.debug_running = False
        self.show_help = False
        self.help_img = pygame.image.load('assets/help.png').convert_alpha()

        self.inventory = None
        self.inventory_is_open = False
        self.grabbed_object = None

        # Store data of everything
        self.scenes_data = s_data
        self.characters_data = ch_data
        self.objects_data = o_data
        self.conversations_data = cv_data

        # Subtitles of dialogue
        self.current_line = None
        self.remaining_lines = None
        self.current_color = None
        self.frame_delay = 10

        # Things still not implemented
        self.conversation = None
        self.actions = None
        self.action_in_place = False
        self.choose_response = False

    def camera_reposition(self):
        mc_x, mc_y = self.main_character.position
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

    def interactive_mode(self):
        return not (self.action_in_place or self.show_help)

    def enter_debug_mode(self):
        self.debug_running = True
        self.screen = pygame.display.set_mode((self.camera_width, self.camera_height + self.debug.height))
        self.debug.ceil = self.camera_height
        self.debug.rect = pygame.Rect(0, self.camera_height, self.camera_width, self.debug.height)
        self.debug.go_to_idle()
        self.debug.run()
        # Screen go back to normal after Debugging
        self.screen = pygame.display.set_mode((self.camera_width, self.camera_height))
        self.debug_running = False

    def set_actions(self, actions):
        self.actions = actions

    def end_conversation(self, character):
        self.conversation.end()
        self.conversation = None

    def start_conversation(self, character):
        self.conversation = Conversation(self, character)
        self.conversation.start()

    def current_action_finished(self, action=""):
        if action != "showing text": print("FINISHED", action)
        if self.conversation:
            self.current_color = None
            self.conversation.answer()
        self.actions.continue_current_actions()

    def handle_input_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif not self.interactive_mode():
                break
            elif event.type == pygame.KEYDOWN and not self.choose_response:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_i:
                    self.inventory_is_open = not self.inventory_is_open
                elif event.key == pygame.K_h:
                    self.show_help = not self.show_help
                elif event.key == pygame.K_d:
                    self.enter_debug_mode()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.button)
        return True

    def set_inventory(self, inventory):
        self.inventory = inventory

    def change_scene(self, scene):
        if scene not in self.scenes_data.keys():
            print(f"Scene {scene} not yet implemented.")
            return
        if self.current_scene.background_music:
            self.current_scene.background_music.stop()
        self.scenes[self.current_scene_id] = self.current_scene
        clock = pygame.time.Clock()
        fade_surface = pygame.Surface((self.camera_width, self.camera_height))
        fade_surface.fill((0,0,0))
        alpha = 0
        while alpha < 100:
            # Increase alpha value to make the screen darker
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            alpha += 1
            clock.tick(60)  # Control the speed of the fade effect
        self.set_scene(scene)

    def set_scene(self, scene=''):
        if scene == '': scene = self.current_scene_id
        current_scene_data = self.scenes_data[scene]
        if scene in self.scenes.keys():
            self.current_scene = self.scenes[scene]
        else:
            self.current_scene_id = scene
            self.current_scene = Scene(self, scene, current_scene_data)
            data_objects = current_scene_data["objects"] if "objects" in current_scene_data.keys() else []
            for od in data_objects:
                object_data = self.objects_data[od[0]]
                self.current_scene.add_object(Object(self, od[0], object_data), od)
            data_chars = current_scene_data["characters"] if "characters" in current_scene_data.keys() else []
            for cd in data_chars:
                character_data = self.characters_data[cd[0]]
                char_dialogues = self.conversations_data[cd[0]] if cd[0] in self.conversations_data.keys() else None
                self.current_scene.add_character(Character(self, cd[0], character_data, char_dialogues), cd)
            self.scenes[scene] = self.current_scene

        self.world_width = self.current_scene.width
        self.world_height = self.current_scene.height
        if "cameraX" in current_scene_data.keys() and "cameraY" in current_scene_data.keys():
            self.camera.x = current_scene_data["cameraX"]
            self.camera.y = current_scene_data["cameraY"]
        self.world = pygame.Surface((self.world_width, self.world_height))
        if self.current_scene.background_music:
            self.current_scene.background_music.play(loops=-1)
        self.current_action_finished(f"set_scece {scene}")

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

    # TODO: def play_animation(self, animation):

    def show_text(self, text, color=(0,0,0)):
        if type(text) == str:
            text = [text]
        self.current_line = text[0]
        self.remaining_lines = text[1:]
        self.current_color = color

    # Handle mouse click and redirect to appropiate component

    def handle_click(self, button):
        if self.action_in_place:     # wherever we have a running animation or any
            return                  # other special event, we ignore the click
        if self.conversation:
            self.conversation.handle_click(self.mouse_camera_pos)
            return
        tmp_og = self.grabbed_object
        if self.inventory_is_open:
            self.inventory.handle_click(self.mouse_pos, button, self.grabbed_object)
        else:
            self.current_scene.handle_click(self.mouse_pos, button, self.grabbed_object)
        if tmp_og and button == 3:
            self.grabbed_object = None

    def mouse_over_map(self):
        for m in self.current_scene.marks:
            if euclidean_distance((m[1], m[2]), self.mouse_pos) < 50:
                self.current_scene.selected_mark = m[0]
                ts = self.main_text_font.render(m[0], True, self.current_color)
                tr = ts.get_rect(center=(m[1]-self.camera.x,m[2]-self.camera.y))
                br = pygame.Rect(tr.left - 10, tr.top - 5, tr.width + 20, tr.height + 10)
                pygame.draw.rect(self.screen, (255, 255, 255, 50), br)
                self.screen.blit(ts, tr)
                return
        self.current_scene.selected_mark = None

    def run(self):
        # Main Loop
        running = True
        text_rect = None
        tmp_i,tmp_frame = 0,0 # Indexes for subtitles
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.mouse_camera_pos = (mouse_x, mouse_y)
            if self.main_character: self.camera_reposition()
            # Adjust the position of the cursor to the camera
            self.mouse_pos = (mouse_x + self.camera.x, mouse_y + self.camera.y)
            cursor_rect = self.cursor.get_rect(center=(mouse_x, mouse_y)) if self.cursor else None
            #if keys[pygame.K_SPACE]:
            #    tmp_i = 1000
            running = self.handle_input_events()

            # We update the scene and the world inside the camera view
            self.current_scene.update()
            self.current_scene.draw(self.world)
            self.screen.blit(self.world, (0, 0), self.camera)

            # If the inventory is open, we show it now
            if self.inventory_is_open:
                self.inventory.show()

            # If there is text to show as subtitles, we show it now
            if self.current_line:
                if tmp_i < len(self.current_line)*1.3:
                    if tmp_i == 0 or tmp_frame == self.frame_delay:
                        text_surface = self.main_text_font.render(self.current_line[:tmp_i], True, self.current_color)
                        text_rect = text_surface.get_rect()
                        text_rect.midbottom = (self.camera_width / 2, self.camera_height - 50)
                        background_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 5,
                                                      text_rect.width + 20, text_rect.height + 10)
                        tmp_i+=1
                        tmp_frame=0
                        if tmp_i%3==0 and tmp_i < len(self.current_line):
                            self.current_scene.dialogue_sound[freq_to_col(self.current_color)].play()
                    if background_rect: pygame.draw.rect(self.screen, (255, 255, 255, 50), background_rect)
                    if text_rect: self.screen.blit(text_surface, text_rect)
                    tmp_frame+=1
                else:
                    tmp_i = 0
                    if self.remaining_lines:
                        self.current_line = self.remaining_lines[0]
                        self.remaining_lines = self.remaining_lines[1:]
                        self.start_time = pygame.time.get_ticks()
                    else:
                        self.current_line = None
                        self.current_action_finished("showing text")

            if self.grabbed_object:
                if not self.inventory.rect.collidepoint((mouse_x,mouse_y)):
                    self.inventory_is_open = False
                img = self.grabbed_object.image.copy()
                img,rect = rescale_to_rect(img, size=130)
                img.set_alpha(180)
                rect.center=(mouse_x, mouse_y)
                self.screen.blit(img, rect)

            # We show the name of whichever element is being pointed
            tmpy = 0
            x, y = self.mouse_pos
            pointed_e = None
            if self.current_scene.is_map:
                self.mouse_over_map()
            else:
                # TODO: All of these can go to a dedicated function
                for e in self.current_scene.objects + self.current_scene.characters:
                    if e.area_includes(x, y):
                        if e.position and e.position[1] > tmpy:
                            pointed_e = e
                            tmpy = e.position[1]
                if pointed_e:
                    pointed_e.text_rect.centerx = mouse_x
                    pointed_e.text_rect.bottom = mouse_y - 20
                    self.screen.blit(pointed_e.text_surface, pointed_e.text_rect)

            if self.choose_response: self.conversation.draw_options(self.screen)
            if self.show_help:
                img_rect = self.help_img.get_rect(center=(self.camera_width//2,self.camera_height//2))
                self.screen.blit(self.help_img, img_rect)
            if self.cursor: self.screen.blit(self.cursor, cursor_rect)
            pygame.display.flip()

        pygame.quit()
