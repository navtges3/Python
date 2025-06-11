from typing import Dict, Union, Optional
from src.game.core.constants import *
from src.game.ui.ui_helpers import *
from src.game.core.combatant import Combatant
from src.game.utils.fileIO import resource_path
import random
import pygame

# Type aliases
MonsterDict = Dict[str, Union[str, int]]

#Base class for all monsters
class Monster(Combatant):
    """A base class for all monsters in the game."""
    # TODO update monsters to use weapons and abilities
    
    def __init__(self, name_or_data: Union[str, MonsterDict], max_hp: int = 10, 
                damage: int = 1, gold: int = 10, image: str = "goblin_image.jpg") -> None:
        """
        Initialize the monster with either individual parameters or a data dictionary.

        Args:
            name_or_data: Either a string representing the monster name or a dictionary of monster data
            max_hp: Monster's max health points
            damage: Monster's damage points
            gold: Monster's gold value
            image: Monster's image filename
        """
        if isinstance(name_or_data, dict):
            # Initialize from dictionary
            self.from_dict(name_or_data)
            print("A returning monster stirs!")
        else:
            super().__init__(name_or_data, max_hp)
            # Initialize from individual parameters
            self.name: str = name_or_data
            self.current_hp: int = max_hp
            self.max_hp: int = max_hp
            self.damage: int = damage
            self.gold: int = gold
            self.image: str = image
            print("A new monster appears!")
        # Always calculate experience based on max_hp and damage
        self.experience: int = (self.max_hp + self.damage) // 2

    def attack(self, target: Combatant) -> None:
        """
        Attack a target combatant.

        Args:
            target: The combatant to attack
        """
        target.take_damage(self.damage)
        
    def __str__(self) -> str:
        """Returns the name of the monster."""
        return self.name

    def to_dict(self) -> MonsterDict:
        """
        Convert monster data to a dictionary for saving.

        Returns:
            A dictionary containing the monster's data
        """
        return {
            "name": self.name,
            "current_hp": self.current_hp,
            "max_hp": self.max_hp,
            "damage": self.damage,
            "gold": self.gold,
            "image": self.image,
            "experience": self.experience,
        }

    def from_dict(self, data: MonsterDict) -> None:
        """
        Load monster data from a dictionary.

        Args:
            data: Dictionary containing monster data
        """
        self.name = str(data.get("name", "Monster"))
        self.current_hp = int(data.get("current_hp", 10))
        self.max_hp = int(data.get("max_hp", 10))
        self.damage = int(data.get("damage", 1))
        self.gold = int(data.get("gold", 10))
        self.image = str(data.get("image", "goblin_image.jpg"))
        # Experience will be calculated in __init__ after from_dict completes

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, 
            x: int, y: int) -> None:
        """
        Draw the monster on the given surface.

        Args:
            surface: Pygame surface to draw on
            font: Font to use for text
            x: X coordinate to draw at
            y: Y coordinate to draw at
        """
        # Border 
        monster_border = pygame.Rect(x, y, GameConstants.SCREEN_WIDTH // 2, 
                                   GameConstants.SCREEN_HEIGHT // 2 - 50)
        pygame.draw.rect(surface, Colors.RED, monster_border, width=5, border_radius=10)
        # Image

        draw_text(self.name, font, Colors.BLACK, surface, 
                    monster_border.x + 20, monster_border.y + 10)
        monster_image = pygame.image.load(resource_path(f"src\\game\\assets\\images\\{self.image}")).convert()
        monster_image = pygame.transform.scale(monster_image, (100, 100))
        surface.blit(monster_image, (monster_border.x + 10, 
                    monster_border.y + font.get_linesize() + 10))
        
        health_bar_width = 90
        health_bar_height = font.get_linesize() + 4
        health_bar_x = monster_border.x + 15
        health_bar_y = monster_border.y + monster_image.get_height() + font.get_linesize() + 15
        draw_health_bar(surface, font, health_bar_x, health_bar_y, 
                        health_bar_width, health_bar_height, 
                        self.current_hp, self.max_hp)

class Goblin(Monster):
    """A class representing a Goblin monster."""
    healthLow: int = 5
    healthHigh: int = 10
    damageLow: int = 1
    damageHigh: int = 3
    goldLow: int = 0
    goldHigh: int = 5

    def __init__(self, name: str = "Goblin") -> None:
        """
        Initialize the Goblin with random health and damage.

        Args:
            name: The name of the goblin
        """
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        gold = random.randrange(self.goldLow, self.goldHigh)
        super().__init__(name, health, damage, gold, image="goblin_image.jpg")

class Orc(Monster):
    """A class representing an Orc monster."""
    healthLow: int = 10
    healthHigh: int = 17
    damageLow: int = 2
    damageHigh: int = 5
    goldLow: int = 6
    goldHigh: int = 10

    def __init__(self, name: str = "Orc") -> None:
        """
        Initialize the Orc with random health and damage.

        Args:
            name: The name of the orc
        """
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        gold = random.randrange(self.goldLow, self.goldHigh)
        super().__init__(name, health, damage, gold, image="orc_image.jpg")

class Ogre(Monster):
    """A class representing an Ogre monster."""
    healthLow: int = 17
    healthHigh: int = 25
    damageLow: int = 4
    damageHigh: int = 8
    goldLow: int = 11
    goldHigh: int = 20

    def __init__(self, name: str = "Ogre") -> None:
        """
        Initialize the Ogre with random health and damage.

        Args:
            name: The name of the ogre
        """
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        gold = random.randrange(self.goldLow, self.goldHigh)
        super().__init__(name, health, damage, gold, image="ogre_image.jpg")

def get_monster(level_or_name: Union[int, str] = "Goblin") -> Monster:
    """
    Get a monster instance based on level or name.

    Args:
        level_or_name: Either an integer level or string monster name

    Returns:
        A new monster instance of the appropriate type
    """
    if isinstance(level_or_name, int):
        level = level_or_name
        if level < 3:
            return Goblin()
        elif level < 6:
            return Orc()
        else:
            return Ogre()
    else:
        name = level_or_name
        if name == "Orc":
            return Orc()
        elif name == "Ogre":
            return Ogre()
        else:
            return Goblin()