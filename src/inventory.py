class Inventory:
    def __init__(self, game, image=None):
        """Initialize an empty inventory."""
        self.game = game
        self.image = image
        self.items = []  # A list to hold items (objects) in the inventory
        
        # Information about how to position the objects inside the inventory grid
        self.grid = None # (rows, columns)
        self.rect = None # (rectangle containing the specifig grid
        self.hspace = None # Separation between columns
        self.vspace = None # Separation between rows
    
    def setup(self, grid, rect, hspace, vspace):
    	self.grid = grid
        self.rect = rect
        self.hspace = hspace
        self.vspace = vspace
    	
    def add_item(self, item):
        """Add an item to the inventory.
        
        Args:
            item (str): The name or object of the item to add.
        """
        if item not in self.items:
            self.items.append(item)
            print(f"{item} has been added to the inventory.")
        else:
            print(f"{item} is already in the inventory.")
    
    def remove_item(self, item):
        """Remove an item from the inventory.
        
        Args:
            item (str): The name or object of the item to remove.
        """
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
            for item in self.items:
            	image_rect = item.image.get_rect()
            	image_rect.topleft = (i,100)
                self.game.screen.blit(item.image, image_rect)
                i+=120
        else:
            print("The inventory is empty.")
