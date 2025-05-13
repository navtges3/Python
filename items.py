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
    def __init__(self, name:str, description:str, damage:int, level:int=1, value:int=10):
        """Initialize the weapon with a name, description, and damage."""
        self.level = level
        self.damage = damage
        super().__init__(name, description, value)
    
    def print_stats(self):
        """Prints the weapon's stats."""
        print(f"{self.name}: Damage: {self.damage}")
    
class Armor(Item):
    """A class representing an armor item."""
    def __init__(self, name:str, description:str, block:int, dodge:int, duration:int, value:int=10):
        """Initialize the armor with a name, description, block, dodge, and cooldown."""
        self.block = block
        self.dodge = dodge
        self.duration = duration
        self.counter = 0
        super().__init__(name, description, value)

    def update(self):
        self.counter -= 1

    def use(self):
        """Use the armor, activating its effects."""
        if self.is_available():
            self.counter = self.duration * 2

    def is_active(self) -> bool:
        """Check if the armor is currently active."""
        return self.counter >= self.duration
    
    def is_available(self) -> bool:
        """Check if the armor is on cooldown."""
        return self.counter < 1
    
    def print_stats(self):
        """Prints the armor's stats."""
        print(f"{self.name} Block: {self.block} Dodge: {self.dodge}")

potion_dictionary = {
    "Health Potion": Item("Health Potion", "Restores 10 health points", 10),
    "Damage Potion": Item("Damage Potion", "Increases damage by 5 for one turn", 10),
    "Block Potion": Item("Block Potion", "Increases block by 5 for one turn", 10),
}

weapon_dictionary = { 
    # Level 1 - Basic Starter Weapons
    1 : {
    "Rusty Sword": Weapon("Rusty Sword", "A worn-out blade barely holding together.", damage=8, value=15),
    "Wooden Club": Weapon("Wooden Club", "A simple club used for self-defense.", damage=10, value=20),
    "Iron Knife": Weapon("Iron Knife", "A small but reliable blade.", damage=12, value=30),
    "Apprentice's Bow": Weapon("Apprentice's Bow", "A basic bow meant for beginner archers.", damage=14, value=40),
    "Stone Axe": Weapon("Stone Axe", "A crude axe made of stone and wood.", damage=16, value=45),
    },
    2 : {
    # Level 2 - Common Warrior's Arsenal
    "Iron Sword": Weapon("Iron Sword", "A sturdy, reliable blade favored by novice warriors.", damage=15, level=2, value=50),
    "Steel Axe": Weapon("Steel Axe", "A heavy axe that delivers powerful strikes.", damage=22, level=2, value=85),
    "Arcane Dagger": Weapon("Arcane Dagger", "A magically infused dagger, swift and lethal.", damage=18, level=2, value=120),
    "Hunter's Longbow": Weapon("Hunter's Longbow", "A well-crafted bow with improved range.", damage=19, level=2, value=130),
    "Serrated Mace": Weapon("Serrated Mace", "A spiked mace, excellent at breaking armor.", damage=20, level=2, value=150),
    },
    3 : {
    # Level 3 - Advanced Combat Equipment
    "Dragonfang Spear": Weapon("Dragonfang Spear", "A spear crafted from the fang of an ancient dragon.", damage=30, level=3, value=200),
    "Shadow Katana": Weapon("Shadow Katana", "Forged in darkness, strikes swift and silent.", damage=25, level=3, value=150),
    "Titan Warhammer": Weapon("Titan Warhammer", "A massive hammer capable of shattering armor with ease.", damage=35, level=3, value=300),
    "Blazing Rapier": Weapon("Blazing Rapier", "A slender sword imbued with fiery magic.", damage=28, level=3, value=250),
    "Windfury Chakrams": Weapon("Windfury Chakrams", "Pair of throwing blades guided by wind magic.", damage=27, level=3, value=280),
    },
    4 : {
    # Level 4 - Mastercrafted and Legendary Artifacts
    "Celestial Greatsword": Weapon("Celestial Greatsword", "A divine blade blessed by the stars.", damage=40, level=4, value=500),
    "Stormforged Halberd": Weapon("Stormforged Halberd", "A mighty halberd crackling with electricity.", damage=38, level=4, value=450),
    "Voidfang Dagger": Weapon("Voidfang Dagger", "A dagger infused with the abyss's power.", damage=36, level=4, value=400),
    "Moonlit Bow": Weapon("Moonlit Bow", "A bow blessed by lunar energy, firing enchanted arrows.", damage=39, level=4, value=480),
    "Frozen Pike": Weapon("Frozen Pike", "A chilling spear capable of slowing enemies.", damage=37, level=4, value=420),
    },
    5 : {
    # Level 5 - Mythical and Legendary Relics
    "Apocalypse Blade": Weapon("Apocalypse Blade", "A cursed sword overflowing with destructive energy.", damage=50, level=5, value=700),
    "Fang of the Eternal Beast": Weapon("Fang of the Eternal Beast", "A dagger said to drain the life force of foes.", damage=48, level=5, value=650),
    "Solarflare Gauntlets": Weapon("Solarflare Gauntlets", "Gauntlets capable of channeling blinding solar energy.", damage=47, level=5, value=600),
    "Worldbreaker Hammer": Weapon("Worldbreaker Hammer", "A colossal hammer said to shake the earth itself.", damage=52, level=5, value=750),
    "Godslayer Spear": Weapon("Godslayer Spear", "A spear rumored to pierce the fabric of reality.", damage=55, level=5, value=900),
    },
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