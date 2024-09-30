import pygame

from utils import *

class Inventory:
    def __init__(self, game, image=None):
        """Initialize an empty inventory."""
        self.game = game
        self.image = image
        self.items = []  # Pair (item, rect) of items in the inventory (check for improvement)
        
        # Information about how to position the objects inside the inventory grid
        self.grid = None # (rows, columns)
        self.cell_size = None
        self.rect = None # (rectangle containing the specifig grid)
        self.hspace = None # Separation between columns
        self.vspace = None # Separation between rows
    
    def setup(self, grid, cell_size, rect, hspace, vspace):
        self.grid = grid
        self.cell_size = cell_size
        self.rect = rect
        self.hspace = hspace
        self.vspace = vspace

    def handle_click(self, pos, button):
        selected_item = None
        for (item, rect) in self.items:
            if rect.collidepoint(pos):
                selected_item = item
                break
        if not selected_item:
            self.game.inventory_is_open = False
        if button == 1:     # Left Click
            selected_item.observe()
        elif button == 3:   # Right click
            self.game.grabbed_object = selected_item


    def add_item(self, item):
        x_offset = len(self.items) * (self.cell_size + self.hspace)
        y_offset = self.rect.topleft # TODO: Calculate this
        rect = pygame.Rect(x_offset, y_offset, self.cell_size, self.cell_size)
        self.items.append((item, rect))
    
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"{item} has been removed from the inventory.")
        else:
            print(f"{item} is not in the inventory.")
    
    def has_item(self, item):
        """Check if an item is in the inventory.
        
        Args:
            item (str): The name or object of the item to check.
        
        Returns:
            bool: True if the item is in the inventory, False otherwise.
        """
        return item in self.items
    
    def use_item(self, item, target=None):
        """Use an item from the inventory on a target.
        
        Args:
            item (str): The name or object of the item to use.
            target (str, optional): The name or object of the target.
        """
        if self.has_item(item):
            if target:
                print(f"Using {item} on {target}.")
                # Logic for item interaction with target
            else:
                print(f"Using {item}.")
                # Logic for item use
            self.remove_item(item)
        else:
            print(f"{item} is not in the inventory to use.")
    
    def show(self):
        """Display the current items in the inventory in the screen"""
        if self.image:
            image_rect = self.image.get_rect()
            image_rect.center = (self.game.camera_width // 2, self.game.camera_height // 2)
            self.game.screen.blit(self.image, image_rect)
        if self.items:
            i = 0
            for (item, rect) in self.items:
                img, rect = rescale_to_rect(item.image, rect)
                self.game.screen.blit(img, rect)
        else:
            print("The inventory is empty.")
