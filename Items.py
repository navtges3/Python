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

equipmentDictionary = { "Dagger": Weapon("Dagger", "A sharp dagger", 3),
                        "Sword": Weapon("Sword", "A sharp sword", 5), 
                        "Axe": Weapon("Axe", "A sharp axe", 7), 
                        "Longsword": Weapon("Longsword", "A sharp Longsword", 9)}

protectionDictionary = {    "Leather": Armor("Leather", "A sturdy leather suit", 2),
                            "Chainmail": Armor("Chainmail", "A suit of chainmail", 4),
                            "Plate": Armor("Plate", "A suit of plate armor", 6)}

lootDictionary = {  "Gold": Item("Gold", "A small pile of gold", 1),
                    "Gem": Item("Gem", "A shiny gemstone", 3),
                    "Potion": Item("Potion", "A healing potion", 5)}