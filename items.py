class Item:
    def __init__(self, name:str, description:str, value:int=0):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return self.name
    
    def print_stats(self):
        print(self.name + ": " + self.description)

class Weapon(Item):
    def __init__(self, name:str, description:str, damage:int, value:int=10):
        self.damage = damage
        super().__init__(name, description, value)
    
    def print_stats(self):
        print(self.name + ": " + self.description + " Damage: " + str(self.damage))
    
class Armor(Item):
    def __init__(self, name:str, description:str, block:int, value:int=10):
        self.block = block
        super().__init__(name, description, value)

    def print_stats(self):
        print(self.name + ": " + self.description + " Block: " + str(self.block))

equipmentDictionary = { "Daggers": Weapon("Daggers", "A rogue’s signature: fast, agile, and perfect for quick, lethal strikes", 3),
                        "Rapier": Weapon("Rapier", "A slender, piercing sword that allows for swift, elegant combat", 5), 
                        "Throwing Knives": Weapon("Throwing Knives", "Silent, deadly, and ideal for surprise attacks from a distance", 7), 
                        "Hand Crossbow": Weapon("Hand Crossbow", "A compact ranged weapon, great for assassinations and quick escapes", 9),
                        "Shadow Whip": Weapon("Shadow Whip", "A mystical whip that ensnares foes and delivers vicious strikes", 11),
                        "Greatsword": Weapon("Greatsword", "A massive, two-handed blade that delivers devastating slashes and cleaves through enemies", 3),
                        "Warhammer": Weapon("Warhammer", "A brutal, heavy weapon that crushes armor and bones with raw force", 5), 
                        "Battleaxe": Weapon("Battleaxe", "A hefty axe, ideal for chopping through foes with powerful, sweeping strikes", 7), 
                        "Halberd": Weapon("Halberd", "A polearm with a sharp axe blade and a spear tip, providing reach and versatility", 9),
                        "Flaming Greataxe": Weapon("Flaming Greataxe", "A mystical whip that ensnares foes and delivers vicious strikes", 11)}

protectionDictionary = {    "Leather": Armor("Leather", "A sturdy leather suit", 2),
                            "Chainmail": Armor("Chainmail", "A suit of chainmail", 4),
                            "Plate": Armor("Plate", "A suit of plate armor", 6)}

lootDictionary = {  "Gold": Item("Gold", "A small pile of gold", 1),
                    "Gem": Item("Gem", "A shiny gemstone", 3),
                    "Potion": Item("Potion", "A healing potion", 5)}
