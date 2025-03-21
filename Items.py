class Item:
    def __init__(self, name:str, description:str):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name
    
    def printStats(self):
        print(self.name + ": " + self.description)

class Weapon(Item):
    def __init__(self, name, description, damage):
        self.damage = damage
        super().__init__(name, description)
    
    def printStats(self):
        print(self.name + ": " + self.description + " Damage: " + str(self.damage))
    
class Armor(Item):
    def __init__(self, name, description, block):
        self.block = block
        super().__init__(name, description)

    def printStats(self):
        print(self.name + ": " + self.description + " Block: " + str(self.block))

equipmentDictionary = {"Dagger": Weapon("Dagger", "A sharp dagger", 3),
            "Sword": Weapon("Sword", "A sharp sword", 5), 
           "Axe": Weapon("Axe", "A sharp axe", 7), 
           "Longsword": Weapon("Longsword", "A sharp Longsword", 9)}

protectionDictionary = {"Leather": Armor("Leather", "A sturdy leather suit", 2),
          "Chainmail": Armor("Chainmail", "A suit of chainmail", 4),
           "Plate": Armor("Plate", "A suit of plate armor", 6)}

lootDictionary = {"Gold": Item("Gold", "A small pile of gold"),
         "Gem": Item("Gem", "A shiny gemstone"),
          "Potion": Item("Potion", "A healing potion")}