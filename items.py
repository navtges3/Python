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

next_equipment_dictionary = {"Daggers": "Rapier",
                            "Rapier": "Throwing Knives",
                            "Throwing Knives": "Hand Crossbow",
                            "Hand Crossbow": "Shadow Whip",
                            "Shadow Whip": None,
                            "Greatsword": "Warhammer",
                            "Warhammer": "Battleaxe",
                            "Battleaxe": "Halberd",
                            "Halberd": "Flaming Greataxe",
                            "Flaming Greataxe": None}

equipment_dictionary = { "Daggers": Weapon("Daggers", "A rogue’s signature: fast, agile, and perfect for quick, lethal strikes", 3),
                        "Rapier": Weapon("Rapier", "A slender, piercing sword that allows for swift, elegant combat", 5), 
                        "Throwing Knives": Weapon("Throwing Knives", "Silent, deadly, and ideal for surprise attacks from a distance", 7), 
                        "Hand Crossbow": Weapon("Hand Crossbow", "A compact ranged weapon, great for assassinations and quick escapes", 9),
                        "Shadow Whip": Weapon("Shadow Whip", "A mystical whip that ensnares foes and delivers vicious strikes", 11),
                        "Greatsword": Weapon("Greatsword", "A massive, two-handed blade that delivers devastating slashes and cleaves through enemies", 3),
                        "Warhammer": Weapon("Warhammer", "A brutal, heavy weapon that crushes armor and bones with raw force", 5), 
                        "Battleaxe": Weapon("Battleaxe", "A hefty axe, ideal for chopping through foes with powerful, sweeping strikes", 7), 
                        "Halberd": Weapon("Halberd", "A polearm with a sharp axe blade and a spear tip, providing reach and versatility", 9),
                        "Flaming Greataxe": Weapon("Flaming Greataxe", "A mystical whip that ensnares foes and delivers vicious strikes", 11)}

protection_dictionary = {    "Leather": Armor("Leather", "A sturdy leather suit", 0, 10, 5),
                            "Chainmail": Armor("Chainmail", "A suit of chainmail", 1, 0, 5),
                            "Plate": Armor("Plate", "A suit of plate armor", 6, 0, 5),}