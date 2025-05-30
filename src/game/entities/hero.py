from random import randint
from typing import Dict, Union, Optional, Tuple, Any, List
from src.game.entities.items import Item, Armor, Weapon, weapon_dictionary, armor_dictionary
from src.game.entities.ability import Ability, ability_dictionary
from src.game.ui.ui_helpers import *
from src.game.core.combatant import Combatant
from src.game.utils.fileIO import resource_path
import pygame

# Type aliases
PotionBag = Dict[str, int]
HeroDict = Dict[str, Any]

class Hero(Combatant):
    """Base class for all heroes in the game."""

    def __init__(self, name: str = "Hero", max_hp: int = 10, 
                image: Optional[pygame.Surface] = None, 
                weapon: Optional[Weapon] = None, 
                armor: Optional[Armor] = None, 
                gold: int = 50, 
                border_color: Colors = Colors.BLUE, 
                class_name: str = "Hero") -> None:
        """
        Initialize the hero with a name, health, weapon, armor, and gold.
        
        Args:
            name: The hero's name
            max_hp: Maximum hit points
            image: Hero's sprite image
            weapon: Hero's equipped weapon
            armor: Hero's equipped armor
            gold: Starting gold amount
            border_color: Color of the hero's UI border
            class_name: Name of the hero's class
        """
        super().__init__(name, max_hp)
        self.weapon: Optional[Weapon] = weapon
        self.armor: Optional[Armor] = armor
        self.level: int = 1
        self.experience: int = 0
        self.gold: int = gold
        self.potion_bag: PotionBag = {
            "Health Potion": 2,
            "Damage Potion": 1,
            "Block Potion": 1,
        }
        self.potion_damage: int = 0
        self.potion_block: int = 0
        self.border_color: Colors = border_color
        self.image: Optional[pygame.Surface] = image
        self.class_name: str = class_name
        self.abilities: List[Ability] = []
        self.energy: int = 10
        self.max_energy: int = 10

        # TODO Change Hero Abilities to be three lists of Attack Defense and Utility abilities

    def attack(self, target:Combatant) -> tuple[int, bool, bool]:
        """Attack a target and return the damage dealt along with miss/crit flags.
        
        Returns:
            tuple containing:
            - damage dealt (int)
            - whether the attack missed (bool)
            - whether the attack was a critical hit (bool)
        """
        damage = self.weapon.calculate_damage()
        # A damage of 0 means the attack missed
        missed = (damage == 0)
        # If damage is greater than base weapon damage, it was a crit
        crit = (damage > self.weapon.damage)
        target.take_damage(damage)
        return damage, missed, crit

    def take_damage(self, incoming_damage: int) -> None:
        """
        Take damage after applying armor defense.
        
        Args:
            incoming_damage: Amount of damage to take
        """
        if self.armor:
            incoming_damage = self.armor.calculate_defence(incoming_damage)
        super().take_damage(incoming_damage)

    def rest(self) -> None:
        """
        The hero gains health and restores all energy
        """

        self.energy = self.max_energy
        self.current_hp += self.level * 5
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

    def add_item(self, item: Item) -> None:
        """
        Add an item to the hero's inventory.
        
        Args:
            item: The item to add
        """
        if isinstance(item, Weapon):
            self.weapon = item
            print(f"{self.name} equipped a {item.name}!")
        elif isinstance(item, Armor):
            self.armor = item
            print(f"{self.name} equipped a {item.name}!")
        elif isinstance(item, Item):
            self.add_potion(item.name, 1)

    def has_potions(self) -> bool:
        return any(amount > 0 for amount in self.potion_bag.values())
    
    def add_potion(self, potion_name: str, amount: int) -> None:
        """
        Add a potion to the hero's inventory.
        
        Args:
            potion_name: Name of the potion to add
            amount: Number of potions to add
        """
        if potion_name in self.potion_bag:
            self.potion_bag[potion_name] += amount
        else:
            self.potion_bag[potion_name] = amount
        print(f"{amount} {potion_name}(s) added to your inventory!")

    def use_potion(self, potion_name: str) -> None:
        """
        Use a potion from the hero's inventory.
        
        Args:
            potion_name: Name of the potion to use
        """
        if potion_name in self.potion_bag and self.potion_bag[potion_name] > 0:
            if potion_name == "Health Potion":
                self.current_hp += 5
                if self.current_hp > self.max_hp:
                    self.current_hp = self.max_hp
                print(f"{self.name} used a Health Potion! Health is now {self.current_hp}.")
            elif potion_name == "Damage Potion":
                self.potion_damage = 3
                print(f"{self.name} used a Damage Potion! Damage increased by {self.potion_damage}.")
            elif potion_name == "Block Potion":
                self.potion_block = 2
                print(f"{self.name} used a Block Potion! Block increased by {self.potion_block}.")
            self.potion_bag[potion_name] -= 1
        else:
            print(f"You don't have any {potion_name}(s) left!")

    def add_gold(self, amount: int) -> None:
        """
        Add gold to the hero's inventory.
        
        Args:
            amount: Amount of gold to add
        """
        self.gold += amount
        print(f"You gained {amount} gold! Total gold: {self.gold}")

    def spend_gold(self, amount) -> bool:
        """Spend gold from the hero's inventory."""
        if self.gold >= amount:
            self.gold -= amount
            print(f"You spent {amount} gold. Remaining gold: {self.gold}")
            return True
        else:
            print("Not enough gold!")
            return False

    def gain_experience(self, experience:int):
        """Gain experience points."""
        self.experience += experience
        if self.experience >= (10 * self.level):
            self.experience = 0
            self.level_up()

    def level_up(self):
        """Level up the hero."""
        self.current_hp += 5
        if self.current_hp > self.max_hp:
            self.max_hp = self.current_hp
        self.level += 1
        print(self.name + " has leveled up!")

    def __str__(self):
        """Returns the name of the hero."""
        return self.name
    
    def add_ability(self, ability_name: str) -> None:
        """
        Add an ability to the hero's ability list.
        
        Args:
            ability_name: Name of the ability to add
        """
        if ability_name in ability_dictionary:
            ability = ability_dictionary[ability_name]
            if ability not in self.abilities:
                self.abilities.append(ability)
                print(f"{self.name} learned {ability_name}!")
            else:
                print(f"{self.name} already knows {ability_name}!")
        else:
            print(f"Unknown ability: {ability_name}")

    def remove_ability(self, ability_name: str) -> None:
        """
        Remove an ability from the hero's ability list.
        
        Args:
            ability_name: Name of the ability to remove
        """
        for ability in self.abilities:
            if ability.name == ability_name:
                self.abilities.remove(ability)
                print(f"{self.name} forgot {ability_name}!")
                return
        print(f"{self.name} doesn't know {ability_name}!")

    def use_ability(self, ability_name: str, target: Optional[Combatant] = None) -> bool:
        """
        Use an ability from the hero's ability list.
        
        Args:
            ability_name: Name of the ability to use
            target: Target of the ability (if required)
            
        Returns:
            bool: Whether the ability was successfully used
        """
        for ability in self.abilities:
            if ability.name == ability_name:
                if not ability.can_use(self):
                    print(f"{ability_name} is still on cooldown!")
                    return False
                if self.energy < ability.energy_cost:
                    print(f"Not enough energy to use {ability_name}!")
                    return False
                
                effect = ability.use(self, target)
                self.energy -= ability.energy_cost
                
                # Print appropriate message based on the effect
                if hasattr(effect, 'missed') and effect.missed:
                    print(f"{self.name}'s {ability_name} missed!")
                elif hasattr(effect, 'critical') and effect.critical:
                    print(f"{self.name}'s {ability_name} landed a critical hit for {effect.damage} damage!")
                elif effect.damage > 0:
                    print(f"{self.name} used {ability_name} dealing {effect.damage} damage!")
                elif effect.healing > 0:
                    print(f"{self.name} used {ability_name} restoring {effect.healing} health!")
                elif effect.block > 0:
                    print(f"{self.name} used {ability_name} gaining {effect.block} block for {effect.duration} turns!")
                
                return True
                
        print(f"{self.name} doesn't know {ability_name}!")
        return False

    def update_abilities(self) -> None:
        """Update cooldowns of all abilities at the end of turn."""
        for ability in self.abilities:
            ability.update_cooldown()

    def restore_energy(self, amount: int) -> None:
        """
        Restore energy to the hero.
        
        Args:
            amount: Amount of energy to restore
        """
        self.energy = min(self.energy + amount, self.max_energy)

    def to_dict(self) -> HeroDict:
        """
        Convert the hero object to a dictionary for saving.
        
        Returns:
            Dictionary containing the hero's data
        """
        return {
            "name": self.name,
            "class_name": self.class_name,
            "max_hp": self.max_hp,
            "current_hp": self.current_hp,
            "level": self.level,
            "experience": self.experience,
            "gold": self.gold,
            "weapon": self.weapon.name if self.weapon else None,
            "armor": self.armor.name if self.armor else None,
            "potion_bag": self.potion_bag,
            "abilities": [ability.name for ability in self.abilities],
            "energy": self.energy,
            "max_energy": self.max_energy
        }
    
    def from_dict(self, data: HeroDict) -> None:
        """
        Load the hero object from a dictionary.
        
        Args:
            data: Dictionary containing hero data to load
        """
        self.name = data["name"]
        self.class_name = data["class_name"]
        self.max_hp = data["max_hp"]
        self.current_hp = data["current_hp"]
        self.level = data["level"]
        self.experience = data["experience"]
        self.gold = data["gold"]
        self.weapon = weapon_dictionary[data["weapon"]] if data["weapon"] else None
        self.armor = armor_dictionary[data["armor"]] if data["armor"] else None
        self.potion_bag = data["potion_bag"]
        self.abilities = []
        for ability_name in data.get("abilities", []):
            self.add_ability(ability_name)
        self.energy = data.get("energy", 10)
        self.max_energy = data.get("max_energy", 10)
        if self.class_name == "Knight":
            self.image = pygame.image.load(resource_path("images/knight.png")).convert()
        else:
            self.image = pygame.image.load(resource_path("images/assassin.png")).convert()
        self.image = pygame.transform.scale(self.image, (100, 100))

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, 
            x: int = 0, y: int = 0) -> None:
        """
        Draw the hero and their stats on the given surface.
        
        Args:
            surface: Pygame surface to draw on
            font: Font to use for text
            x: X coordinate to draw at
            y: Y coordinate to draw at
        """
        # Border
        hero_border = pygame.Rect(x, y, GameConstants.SCREEN_WIDTH // 2, GameConstants.SCREEN_HEIGHT // 2 - 50)

        # Hero Name
        draw_text(self.name, font, Colors.BLACK, surface, hero_border.x + 20, hero_border.y + 10)

        # Hero Image
        surface.blit(self.image, (hero_border.x + 10, hero_border.y + font.get_linesize() + 10))

        # Health and Energy Bars
        health_bar_width = 90
        health_bar_height = font.get_linesize() + 4
        health_bar_x = hero_border.x + 15
        health_bar_y = hero_border.y + font.get_linesize() + self.image.get_height() + 15
        
        # Draw Health Bar
        draw_health_bar(surface, font, health_bar_x, health_bar_y, health_bar_width, health_bar_height, 
                        self.current_hp, self.max_hp)
        
        # Draw Energy Bar
        energy_bar_y = health_bar_y + health_bar_height + 5
        draw_energy_bar(surface, font, health_bar_x, energy_bar_y, health_bar_width, health_bar_height,
                        self.energy, self.max_energy)

        # Hero Stats
        hero_text = f"Level: {self.level}\nExp: {self.experience}\nGold: {self.gold}"
        draw_multiple_lines(hero_text, font, Colors.BLACK, surface, 
                            hero_border.x + self.image.get_width() + 10, 
                            hero_border.y + font.get_linesize() + 20)

        # Draw Abilities
        ability_text = "Abilities:"
        for ability in self.abilities:
            cooldown_text = f" ({ability.current_cooldown})" if ability.current_cooldown > 0 else ""
            ability_text += f"\n-{ability.name} ({ability.energy_cost} energy){cooldown_text}"
        
        draw_multiple_lines(ability_text, font, Colors.BLACK, surface,
                            hero_border.x + 10,
                            energy_bar_y + health_bar_height + 10)

        # Draw the hero's weapon and armor
        if self.weapon is not None:
            weapon_border = pygame.Rect(hero_border.x + hero_border.width // 2, 
                                     hero_border.y, hero_border.width // 2, 
                                     hero_border.height // 3)
            draw_text_centered(self.weapon.name, font, Colors.BLACK, surface,
                             weapon_border.x + weapon_border.width // 2,
                             weapon_border.y + font.get_linesize() // 2 + 10)
            draw_multiple_lines(f"Damage {self.weapon.damage}", font, Colors.BLACK, surface,
                                weapon_border.x + 10, weapon_border.y + font.get_linesize() + 25)
            pygame.draw.rect(surface, Colors.LIGHT_RED, weapon_border, width=3, border_radius=10)

        if self.armor is not None:
            armor_border = pygame.Rect(hero_border.x + hero_border.width // 2,
                                        hero_border.y + hero_border.height // 3,
                                        hero_border.width // 2,
                                        hero_border.height // 3 * 2)
            draw_text_centered(self.armor.name, font, Colors.BLACK, surface,
                                armor_border.x + armor_border.width // 2,
                                armor_border.y + font.get_linesize() // 2 + 10)
            armor_text = f"Block: {self.armor.block}\nChance: {self.armor.block_chance:.0%}\nDodge: {self.armor.dodge_chance:.0%}"
            draw_multiple_lines(armor_text, font, Colors.BLACK, surface,
                                armor_border.x + 10,
                                armor_border.y + font.get_linesize() + 25)
            pygame.draw.rect(surface, Colors.LIGHT_BLUE, armor_border, width=3, border_radius=10)
        
        pygame.draw.rect(surface, Colors.BLUE, hero_border, width=5, border_radius=10)

class Assassin(Hero):
    """A class representing a Assassin hero."""

    def __init__(self, name: str) -> None:
        """
        Initialize the Assassin with random health and a dagger.
        
        Args:
            name: The assassin's name
        """
        image = pygame.image.load(resource_path("images/assassin.png")).convert()
        image = pygame.transform.scale(image, (100, 100))
        health = randint(7, 12)
        weapon = weapon_dictionary["Iron Knife"]
        armor = armor_dictionary["Shadow Cloak"]
        super().__init__(name, health, image, weapon, armor, border_color=Colors.GREEN, class_name="Assassin")
        # Add Assassin starting abilities
        self.add_ability("Precise Strike")
        self.add_ability("Critical Strike")

class Knight(Hero):
    """A class representing a Knight hero."""

    def __init__(self, name: str) -> None:
        """
        Initialize the Knight with random health and a greatsword.
        
        Args:
            name: The knight's name
        """
        image = pygame.image.load(resource_path("images/knight.png")).convert()
        image = pygame.transform.scale(image, (100, 100))
        health = randint(10, 15)
        weapon = weapon_dictionary["Rusty Sword"]
        armor = armor_dictionary["Iron Chestplate"]
        super().__init__(name, health, image, weapon, armor, border_color=Colors.RED, class_name="Knight")
        # Add Knight starting abilities
        self.add_ability("Power Attack")
        self.add_ability("Guard")

def make_hero(hero_name: str, hero_class: str) -> Hero:
    """
    Create a hero based on the given name and class.
    
    Args:
        hero_name: Name of the hero
        hero_class: Class of the hero ("Assassin" or "Knight")
        
    Returns:
        A new hero instance of the specified class
    """
    the_hero = None
    if hero_class == "Assassin":
        the_hero = Assassin(hero_name)
    elif hero_class == "Knight":
        the_hero = Knight(hero_name)
    else:
        the_hero = Hero(hero_name)
    return the_hero 
