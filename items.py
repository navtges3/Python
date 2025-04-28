class Item:
    """
    Base class for all items in the game.
    Each item has a name, description, and value.
    """
    def __init__(self, name:str, description:str, value:int=0):
        """Initialize the item with a name, description, and value."""
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        """Returns the name of the item."""
        return self.name
    
    def print_stats(self):
        """Prints the item's stats."""
        print(f"{self.name}: {self.description}")

class Weapon(Item):
    """A class representing a weapon item."""
    def __init__(self, name:str, description:str, damage:int, value:int=10):
        """Initialize the weapon with a name, description, and damage."""
        self.damage = damage
        super().__init__(name, description, value)
    
    def print_stats(self):
        """Prints the weapon's stats."""
        print(f"{self.name}: Damage: {self.damage}")
    
class Armor(Item):
    """A class representing an armor item."""
    def __init__(self, name:str, description:str, block:int, dodge:int, cooldown:int, value:int=10):
        """Initialize the armor with a name, description, block, dodge, and cooldown."""
        self.block = block
        self.dodge = dodge
        self.cooldown = cooldown
        self.active = 0
        super().__init__(name, description, value)        

    def print_stats(self):
        """Prints the armor's stats."""
        print(f"{self.name} Block: {self.block} Dodge: {self.dodge}")

potion_dictionary = {
    "Health Potion": Item("Health Potion", "Restores 10 health points", 10),
    "Damage Potion": Item("Damage Potion", "Increases damage by 5 for one turn", 10),
    "Block Potion": Item("Block Potion", "Increases block by 5 for one turn", 10),
}

weapon_dictionary = { 
    "Daggers": Weapon("Daggers", "A rogue’s signature: fast, agile, and perfect for quick, lethal strikes", 3),
    "Rapier": Weapon("Rapier", "A slender, piercing sword that allows for swift, elegant combat", 5), 
    "Throwing Knives": Weapon("Throwing Knives", "Silent, deadly, and ideal for surprise attacks from a distance", 7), 
    "Hand Crossbow": Weapon("Hand Crossbow", "A compact ranged weapon, great for assassinations and quick escapes", 9),
    "Shadow Whip": Weapon("Shadow Whip", "A mystical whip that ensnares foes and delivers vicious strikes", 11),
    "Greatsword": Weapon("Greatsword", "A massive, two-handed blade that delivers devastating slashes and cleaves through enemies", 3),
    "Warhammer": Weapon("Warhammer", "A brutal, heavy weapon that crushes armor and bones with raw force", 5), 
    "Battleaxe": Weapon("Battleaxe", "A hefty axe, ideal for chopping through foes with powerful, sweeping strikes", 7), 
    "Halberd": Weapon("Halberd", "A polearm with a sharp axe blade and a spear tip, providing reach and versatility", 9),
    "Flaming Greataxe": Weapon("Flaming Greataxe", "A massive, fiery axe that burns enemies with each devastating strike", 11),
    "Longbow": Weapon("Longbow", "A classic ranged weapon, perfect for precise, long-distance attacks", 6),
    "Scythe": Weapon("Scythe", "A reaper's tool turned weapon, delivering wide, arcing strikes with grim efficiency", 4),
    "Twin Chakrams": Weapon("Twin Chakrams", "Razor-sharp, circular blades that return when thrown, combining elegance with lethality", 8),
    "Lightning Spear": Weapon("Lightning Spear", "A spear infused with the power of storms, striking enemies with shocking force", 10),
    "Frostfang": Weapon("Frostfang", "A chilling sword that freezes enemies with each cut, slowing them down", 7),
    "Venom Dagger": Weapon("Venom Dagger", "A blade laced with deadly poison, ideal for those who prefer subtle kills", 5),
    "Storm Hammer": Weapon("Storm Hammer", "A thunderous weapon that calls down lightning with every powerful swing", 9),
    "Crystal Staff": Weapon("Crystal Staff", "A staff radiating mystical energy, amplifying magical attacks and spells", 8),
    "Bladed Gauntlets": Weapon("Bladed Gauntlets", "Close-combat weapons with sharp edges for brutal, quick strikes", 6),
    "Infernal Flail": Weapon("Infernal Flail", "A chain weapon engulfed in hellfire, smashing enemies with devastating impact", 10)
}

armor_dictionary = {
    "Leather Armor": Armor("Leather Armor", "Light and flexible, offering decent mobility and basic protection", 3, 5, 1, 10),
    "Chainmail": Armor("Chainmail", "Interlinked metal rings that provide balanced defense without sacrificing agility", 5, 3, 2, 20),
    "Plate Armor": Armor("Plate Armor", "Heavy and robust, designed for maximum protection at the expense of mobility", 8, 1, 3, 30),
    "Shadow Cloak": Armor("Shadow Cloak", "An enchanted cloak that boosts stealth and evasion, perfect for rogues", 2, 7, 1, 15),
    "Dragon Scale": Armor("Dragon Scale", "Forged from dragon scales, offering immense resistance and fiery style", 7, 3, 3, 40),
    "Mystic Robes": Armor("Mystic Robes", "Light robes infused with arcane energy, boosting magical resistance and agility", 3, 6, 1, 25),
    "Frozen Guard": Armor("Frozen Guard", "Armor imbued with ice magic, slowing enemies on contact", 6, 2, 2, 30),
    "Spiked Armor": Armor("Spiked Armor", "A menacing armor covered in spikes, damaging enemies who strike the wearer", 6, 2, 2, 25),
    "Battle Harness": Armor("Battle Harness", "A light, tactical armor designed for agility and quick skirmishes", 4, 6, 1, 20),
    "Celestial Plate": Armor("Celestial Plate", "Glowing armor blessed by the heavens, granting unparalleled protection", 9, 2, 3, 50)
}