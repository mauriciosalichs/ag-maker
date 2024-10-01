import pygame
from src.utils import *

class Inventory:
    def __init__(self, game, image):
        """Initialize an empty inventory."""
        self.game = game
        self.image = image
        self.items = []  # Pair (item, rect) of items in the inventory (check for improvement)

        self.rect = image.get_rect()
        self.rect.center = (self.game.camera_width // 2, self.game.camera_height // 2)

        # Information about how to position the objects inside the inventory grid
        self.left_padding = None
        self.top_padding = None
        self.grid = None # (rows, columns)
        self.cell_size = None
        self.hspace = None # Separation between columns
        self.vspace = None # Separation between rows
    
    def setup(self, grid, left_padding, top_padding, cell_size, hspace, vspace):
        self.grid = grid
        self.left_padding = left_padding
        self.top_padding = top_padding
        self.cell_size = cell_size
        self.hspace = hspace
        self.vspace = vspace

    def handle_click(self, pos, button, selected_object):
        pos = (pos[0]-self.game.camera.x,pos[1]-self.game.camera.y)
        selected_item = None
        for (item, rect) in self.items:
            if rect.collidepoint(pos):
                selected_item = item
                break
        if not selected_item:
            self.game.inventory_is_open = False
            return
        if selected_object:
            self.game.show_text(f"Using {selected_object.name} with {selected_item.name}")
        elif button == 1:     # Left Click
            selected_item.observe()
        elif button == 3:   # Right click
            self.game.grabbed_object = selected_item

    def add_item(self, item):
        n = len(self.items)
        if n == self.grid[0]*self.grid[1]:
            self.game.show_text("There is no more space for objects.")
            return
        x = n %  self.grid[0]
        y = n // self.grid[0]
        x_offset = self.rect.topleft[0] + self.left_padding + x * (self.cell_size + self.hspace)
        y_offset = self.rect.topleft[1] + self.top_padding  + y * (self.cell_size + self.vspace)
        rect = pygame.Rect(x_offset, y_offset, self.cell_size, self.cell_size)
        self.items.append((item, rect))
    
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"{item} has been removed from the inventory.")
        else:
            print(f"{item} is not in the inventory.")
    
    def has_item(self, item):
        return item in self.items
    
    def show(self):
        """Display the current items in the inventory in the screen"""
        if self.image:
            self.game.screen.blit(self.image, self.rect)
        if self.items:
            i = 0
            for (item, rect) in self.items:
                img, rect = rescale_to_rect(item.image, rect)
                self.game.screen.blit(img, rect)
        else:
            self.game.show_text("The inventory is empty.")
