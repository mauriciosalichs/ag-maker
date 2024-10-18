# For now, we dont implement fucking dialogues

import pygame
from src.utils import *

class Conversation:
    def __init__(self, game, character):
        self.game = game
        self.character = character
        self.dialogue_root = character.dialogue_data
        self.current_id = 'start'
        self.options_rects = dict() # {responseID: [text, t_rect]}
        self.answered = False

        self.font = pygame.font.SysFont("Courier", 16, bold=True)
        self.dialogue_root[self.current_id]['responses'].append({'text': '¡Hasta Luego!', 'next': 'end'})
	
    def answer(self):
        print("ANSWERING",self.answered)
        if self.answered: # Ya se ha elegido una respuesta
            self.answered = False
            if self.current_id == 'end':
                self.game.conversation = None
                return
            if self.dialogue_root[self.current_id]['text']:
                self.start()
        elif self.game.check_for_actions_about_conversation(self.character.id, self.current_id):
            self.game.choose_response = True
            for response in self.dialogue_root[self.current_id]['responses']:
                if 'textHiddenID' in response.keys():
                    continue
                topic, text = response['next'], response['text']
                self.options_rects[topic] = [text, None]

    def draw_options(self, screen):
        for i, topic in enumerate(self.options_rects.keys()):
            text = self.options_rects[topic][0]
            t_surf = self.font.render(text, True, (0, 0, 0))
            t_rect = t_surf.get_rect()
            t_rect.midbottom = (self.game.camera_width / 2, self.game.camera_height - (i+1)*40)
            self.options_rects[topic][1] = t_rect
            background_rect = pygame.Rect(t_rect.left - 10, t_rect.top - 5,
                                          t_rect.width + 20, t_rect.height + 10)
            pygame.draw.rect(self.game.screen, (0, 255, 0), background_rect)
            self.game.screen.blit(t_surf, t_rect)

    def handle_click(self, pos):
        if not self.game.choose_response:
            return
        for topic in self.options_rects.keys():
            if self.options_rects[topic][1].collidepoint(pos):
                self.current_id = topic
                text = self.options_rects[topic][0]
                del self.options_rects[topic]
                self.game.choose_response = False
                self.answered = True
                self.game.current_scene.main_character.speak(text)
                break

    def start(self):
        self.character.speak(self.dialogue_root[self.current_id]['text'])

    def end(self):
        self.game.choose_response = False
        print("CONVERSATION ENDED")
