from constants import *
from ui_helpers import *
import random
import pygame
import fileIO

#Base class for all monsters
class Monster:
    """A base class for all monsters in the game."""

    def __init__(self, name:str, health:int, damage:int, image:str="goblin_image.jpg"):
        """Initialize the monster with a name, health, damage, and an image."""
        self.name = name
        self.health = health
        self.start_health = health
        self.alive = True
        self.damage = damage
        self.experience = (health + damage) // 2
        self.image = image
        print("A new monster appears!")
        self.print_stats()
        
    def __str__(self):
        """Returns the name of the monster."""
        return self.name

    def get_damage(self) -> int:
        """Returns the damage of the monster."""
        return self.damage
    
    def take_damage(self, damage:int):
        """Reduces the monster's health by the damage taken."""
        self.health = self.health - damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
        print(f"{self.name} has {self.health} health remaining.")

    def draw(self, surface, font, x:int, y:int) -> None:
        # Border 
        monster_border = pygame.Rect(x, y, Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT // 2 - 50)
        pygame.draw.rect(surface, Colors.RED, monster_border, width=5, border_radius=10)
        # Image

        draw_text(self.name, font, Colors.BLACK, surface, monster_border.x + 20, monster_border.y + 10)
        monster_image = pygame.image.load(fileIO.resource_path(f"images\\{self.image}")).convert()
        monster_image = pygame.transform.scale(monster_image, (100, 100))
        surface.blit(monster_image, (monster_border.x + 10, monster_border.y + font.get_linesize() + 10))
        
        health_bar_width = 90
        health_bar_height = font.get_linesize() + 4
        health_bar_x = monster_border.x + 15
        health_bar_y = monster_border.y + monster_image.get_height() + font.get_linesize() + 15
        draw_health_bar(surface, font, health_bar_x, health_bar_y, health_bar_width, health_bar_height, self.health, self.start_health)

    def print_stats(self):
        """Prints the monster's stats."""
        print(f"{self.name} has {self.health} health and {self.damage} damage and {self.experience} experience.")

class Goblin(Monster):
    """A class representing a Goblin monster."""
    healthLow = 5
    healthHigh = 10
    damageLow = 1
    damageHigh = 3

    def __init__(self, name:str="Goblin"):
        """Initialize the Goblin with random health and damage."""
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        super().__init__(name, health, damage, image="goblin_image.jpg")

class Orc(Monster):
    """A class representing an Orc monster."""
    healthLow = 10
    healthHigh = 17
    damageLow = 2
    damageHigh = 5
    experience = 2

    def __init__(self, name:str="Orc"):
        """Initialize the Orc with random health and damage."""
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        super().__init__(name, health, damage, image="orc_image.jpg")

class Ogre(Monster):
    """A class representing an Ogre monster."""
    healthLow = 17
    healthHigh = 25
    damageLow = 4
    damageHigh = 8
    experience = 3

    def __init__(self, name:str="Ogre"):
        """Initialize the Ogre with random health and damage."""
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        super().__init__(name, health, damage, image="ogre_image.jpg")

def get_monster(level:int) -> Monster:
    """Returns a monster based on the level."""
    if level < 3:
        return Goblin()
    elif level < 6:
        return Orc()
    else:
        return Ogre()
    
def get_monster(name:str) -> Monster:
    """Returns a monster based on the name."""
    if name == "Orc":
        return Orc()
    elif name == "Ogre":
        return Ogre()
    else:
        return Goblin()