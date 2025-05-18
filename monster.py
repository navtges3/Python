from constants import *
from ui_helpers import *
from combatant import Combatant
import random
import pygame
import fileIO

#Base class for all monsters
class Monster(Combatant):
    """A base class for all monsters in the game."""

    def __init__(self, name_or_data: str | dict, max_hp: int = 10, damage: int = 1, gold: int = 10, image: str = "goblin_image.jpg"):
        """
        Initialize the monster with either individual parameters or a data dictionary.
        Args:
            name_or_data: Either a string representing the monster name or a dictionary of monster data
            max_hp: Monster's max health points (default: 10)
            damage: Monster's damage points (default: 1)
            gold: Monster's gold value (default: 10)
            image: Monster's image filename (default: "goblin_image.jpg")
        """
        if isinstance(name_or_data, dict):
            # Initialize from dictionary
            self.from_dict(name_or_data)
            print("A returning monster stirs!")
        else:
            super().__init__(name_or_data, max_hp)
            # Initialize from individual parameters
            self.name = name_or_data
            self.current_hp = max_hp
            self.max_hp = max_hp
            self.damage = damage
            self.experience = (max_hp + damage) // 2
            self.gold = gold
            self.image = image
            print("A new monster appears!")

    def attack(self, target:Combatant) -> None:
        target.take_damage(self.damage)
        
    def __str__(self):
        """Returns the name of the monster."""
        return self.name

    def to_dict(self) -> dict:
        """Convert monster data to a dictionary for saving."""
        return {
            "name": self.name,
            "current_hp": self.current_hp,
            "max_hp": self.max_hp,
            "damage": self.damage,
            "gold": self.gold,
            "image": self.image,
        }

    def from_dict(self, data: dict) -> None:
        """Load monster data from a dictionary."""
        self.name = data.get("name", "Monster")
        self.current_hp = data.get("current_hp", 10)
        self.max_hp = data.get("max_hp", 10)
        self.damage = data.get("damage", 1)
        self.gold = data.get("gold", 10)
        self.image = data.get("image", "goblin_image.jpg")

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
        draw_health_bar(surface, font, health_bar_x, health_bar_y, health_bar_width, health_bar_height, self.current_hp, self.max_hp)

class Goblin(Monster):
    """A class representing a Goblin monster."""
    healthLow = 5
    healthHigh = 10
    damageLow = 1
    damageHigh = 3
    goldLow = 0
    goldHigh = 5

    def __init__(self, name:str="Goblin"):
        """Initialize the Goblin with random health and damage."""
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        gold = random.randrange(self.goldLow, self.goldHigh)
        super().__init__(name, health, damage, gold, image="goblin_image.jpg")

class Orc(Monster):
    """A class representing an Orc monster."""
    healthLow = 10
    healthHigh = 17
    damageLow = 2
    damageHigh = 5
    goldLow =6
    goldHigh = 10

    def __init__(self, name:str="Orc"):
        """Initialize the Orc with random health and damage."""
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        gold = random.randrange(self.goldLow, self.goldHigh)
        super().__init__(name, health, damage, gold, image="orc_image.jpg")

class Ogre(Monster):
    """A class representing an Ogre monster."""
    healthLow = 17
    healthHigh = 25
    damageLow = 4
    damageHigh = 8
    goldLow = 11
    goldHigh = 20

    def __init__(self, name:str="Ogre"):
        """Initialize the Ogre with random health and damage."""
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        gold = random.randrange(self.goldLow, self.goldHigh)
        super().__init__(name, health, damage, gold, image="ogre_image.jpg")

def get_monster(level:int) -> Monster:
    """Returns a monster based on the level."""
    if level < 3:
        return Goblin()
    elif level < 6:
        return Orc()
    else:
        return Ogre()
    
def get_monster(name:str="Goblin") -> Monster:
    """Returns a monster based on the name."""
    if name == "Orc":
        return Orc()
    elif name == "Ogre":
        return Ogre()
    else:
        return Goblin()