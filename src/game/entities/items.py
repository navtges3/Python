from random import random
from typing import Dict, Union

class Item:
    """
    Base class for all items in the game.
    """
    def __init__(self, name: str, description: str, value: int = 0) -> None:
        """
        :param name:        The name of the item.
        :param description: Description of the item.
        :param value:       Value of the item in the shop.
        """
        self.name: str = name
        self.description: str = description
        self.value: int = value

    def __str__(self) -> str:
        """Returns the name of the item."""
        return f"{self.name}: {self.description} (Value: {self.value})"

class Weapon(Item):
    def __init__(self, name: str, description: str, value: int,
                 damage: int, accuracy: float, crit_chance: float, crit_damage: float) -> None:
        """
        :param damage:      A flat number subtracted from incoming damage.
        :param accuracy:    Probability (0.0 to 1.0) to successfully attack.
        :param crit_chance: Probability (0.0 to 1.0) to multiply damage by crit_damage.
        :param crit_damage: Multiplier applied when a critical hit occurs.
        """
        super().__init__(name, description, value)
        self.damage: int = damage
        self.accuracy: float = accuracy
        self.crit_chance: float = crit_chance
        self.crit_damage: float = crit_damage

    def calculate_damage(self) -> int:
        if random() > self.accuracy:
            print("Attack missed!")
            return 0
        
        if random() < self.crit_chance:
            effective_damage = int(self.damage * self.crit_damage)
            print("Critical Hit!")
        else:
            effective_damage = self.damage
        return effective_damage
    
    def __str__(self) -> str:
        base_info = super().__str__()
        stats = (f" Damage: {self.damage}, Accuracy: {self.accuracy:.0%} "
                 f"Crit Chance: {self.crit_chance:.0%}, Crit Damage: {self.crit_damage:.1}")
        return base_info + stats
    
class Armor(Item):
    def __init__(self, name: str, description: str, value: int,
                 block: int, block_chance: float, dodge_chance: float) -> None:
        """
        :param block:           A flat number subtracted from incoming damage.
        :param block_chance:    Probability (0.0 to 1.0) to successfully block part of the damage.
        :param dodge_chance:    Probability (0.0 to 1.0) to completely avoid the attack.
        """
        super().__init__(name, description, value)
        self.block: int = block
        self.block_chance: float = block_chance
        self.dodge_chance: float = dodge_chance

    def calculate_defence(self, incoming_damage: int) -> int:
        if random() < self.dodge_chance:
            print("Attack dodged!")
            return 0
        
        if random() < self.block_chance:
            final_damage = max(incoming_damage - self.block, 0)
            print(f"Attack blocked! Damage reduced by {self.block} points.")
        else:
            final_damage = incoming_damage
        return final_damage
    
    def __str__(self) -> str:
        base_info = super().__str__()
        stats = (f" Block: {self.block}, Block Chance: {self.block_chance:.0%}, Dodge Chance: {self.dodge_chance:.0%}")
        return base_info + stats

# Dictionary type aliases
PotionDict = Dict[str, Item]
WeaponDict = Dict[str, Weapon]
ArmorDict = Dict[str, Armor]

potion_dictionary: PotionDict = {
    "Health Potion": Item("Health Potion", "Restores 10 health points", 10),
    "Damage Potion": Item("Damage Potion", "Increases damage by 5 for one turn", 10),
    "Block Potion": Item("Block Potion", "Increases block by 5 for one turn", 10),
}

weapon_dictionary: WeaponDict = {
    # Level 1 - Basic Starter Weapons
    "Rusty Sword":      Weapon("Rusty Sword",       "A worn-out blade barely holding together.",    value=15, damage=8, accuracy=0.75, crit_chance=0.1, crit_damage=1.5),
    "Wooden Club":      Weapon("Wooden Club",       "A simple club used for self-defense.",         value=20, damage=10, accuracy=0.80, crit_chance=0.05, crit_damage=1.4),
    "Iron Knife":       Weapon("Iron Knife",        "A small but reliable blade.",                  value=30, damage=12, accuracy=0.85, crit_chance=0.15, crit_damage=1.6),
    "Apprentice's Bow": Weapon("Apprentice's Bow",  "A basic bow meant for beginner archers.",      value=40, damage=14, accuracy=0.70, crit_chance=0.20, crit_damage=1.8),
    "Stone Axe":        Weapon("Stone Axe",         "A crude axe made of stone and wood.",          value=45, damage=16, accuracy=0.78, crit_chance=0.12, crit_damage=1.5),
}

armor_dictionary: ArmorDict = {
    "Iron Chestplate":      Armor("Iron Chestplate",        "A sturdy chestplate made of iron.",                    15, 10, 0.25, 0.05),
    "Steel Greaves":        Armor("Steel Greaves",          "Protective leg armor crafted from hardened steel.",    12,  8, 0.20, 0.08),
    "Knight's Helm":        Armor("Knight's Helm",          "A reinforced helmet worn by seasoned knights.",        10,  6, 0.30, 0.02),
    "Shadow Cloak":         Armor("Shadow Cloak",           "A mystical cloak that enhances evasion.",              20,  4, 0.15, 0.20),
    "Dragon Scale Shield":  Armor("Dragon Scale Shield",    "A legendary shield made from dragon scales.",          30, 15, 0.35, 0.10)
}