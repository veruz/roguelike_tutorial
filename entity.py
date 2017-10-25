class Entity:
    """
    Generic object for player/enemy/items/etc
    """
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        # Move entity by amount
        self.x += dx
        self.y += dy