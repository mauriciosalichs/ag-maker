# For now, we dont implement fucking dialogues

import pygame
from src.utils import *

class Conversation:
    def __init__(self, dialogue_data):
        self.dialogue_root = dialogue_data
        self.dialogue_in_action = True
        self.choose_dialogue = False
        self.current_id = 'start'
        self.new_lines = None
        self.options = []
        self.options_rects = []

        self.font = pygame.font.SysFont("Courier", 24, bold=True)

    def answer(self):
        self.dialogue_in_action = False
        if self.dialogue_root[self.current_id]['responses']:
            self.choose_dialogue = True
            for response in self.dialogue_root[self.current_id]['responses']:
                self.options.append(response['text'])

    def draw_options(self, screen):
        for i, opt in enumerate(self.options):
            text_surface = self.font.render(opt, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(600,400+i*30))
            self.options_rects.append(text_rect)
            screen.blit(text_surface, text_rect)

    def handle_click(self, pos):
        for i, o_r in enumerate(self.options_rects):
            if o_r.collidepoint(pos):
                self.current_id = self.dialogue_root[self.current_id]['responses'][i]['next']
                self.choose_dialogue = False
                if self.dialogue_root[self.current_id]['text']:
                    self.dialogue_in_action = True
                    self.new_lines = self.dialogue_root[self.current_id]['text']
                else:
                    print('Fin')

    def start(self):
        selected_option = 0
        self.dialogue_in_action = True