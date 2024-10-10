# For now, we dont implement fucking dialogues

import pygame
from src.utils import *

class Conversation:
    def __init__(self, game, character):
        self.game = game
        self.character = character
        self.dialogue_root = character.dialogue_data
        self.current_id = 'start'
        self.options_rects = []

        self.font = pygame.font.SysFont("Courier", 24, bold=True)
	
    def answer(self):
        self.game.check_for_actions_about_conversation(self.character.id, self.current_id)
        if self.dialogue_root[self.current_id]['responses']:
            self.game.choose_response = True
            for response in self.dialogue_root[self.current_id]['responses']:
                opt = response['text']
                t_surf = self.font.render(opt, True, (0, 0, 0))
                t_rect = t_surf.get_rect()
                self.options_rects.append((t_surf, t_rect))
        else:
            print("la Conversacion ha finalizado")
            self.game.conversation = None

    def draw_options(self, screen):
        for i, (t_surf, t_rect) in enumerate(self.options_rects):
            background_rect = pygame.Rect(t_rect.left - 10, t_rect.top - 5,
                                          t_rect.width + 20, t_rect.height + 10)
            pygame.draw.rect(self.game.screen, (0, 255, 0, 30), background_rect)
            pygame.draw.rect(self.game.screen, (0, 0, 0), background_rect, 2)
            t_rect.midbottom = (self.game.camera_width / 2, self.game.camera_height - (i+1)*40)
            self.game.screen.blit(t_surf, t_rect)

    def handle_click(self, pos):
        print("HANDLE CLICK IN OPTIONS",pos)
        for i, (t_surf, t_rect) in enumerate(self.options_rects):
            print(t_rect)
            if t_rect.collidepoint(pos):
                self.current_id = self.dialogue_root[self.current_id]['responses'][i]['next']
                self.options_rects = []
                self.game.choose_response = False
                if self.dialogue_root[self.current_id]['text']:
                    self.start()
                else:
                    print('Fin')

    def start(self):
        self.character.speak(self.dialogue_root[self.current_id]['text'])
        
