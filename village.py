from ui_helpers import *
from constants import *

class Village:
    
    def __init__(self, name:int, health:int):
        self.name = name
        self.health = health
        self.max_health = health
        self.level = 1
    
    def take_damage(self, damage:int) -> None:
        """Take damage from the village."""
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def draw(self, surface, font, x: int, y: int):
        """Draw the village and its health bar."""
        # Draw the village name
        draw_text(self.name, font, Colors.BLACK, surface, x, y)

        # Draw the health bar
        health_bar_width = 200
        health_bar_height = 20
        health_bar_x = x
        health_bar_y = y + 30
        draw_health_bar(surface, font, health_bar_x, health_bar_y, health_bar_width, health_bar_height, self.health, self.max_health)