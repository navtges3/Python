class item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name
    
    def printStats(self):
        print(self.name + ": " + self.description)

class weapon(item):
    def __init__(self, name, description, damage):
        self.damage = damage
        super().__init__(name, description)
    
    def printStats(self):
        print(self.name + ": " + self.description + " Damage: " + str(self.damage))
    
class armor(item):
    def __init__(self, name, description, block):
        self.block = block
        super().__init__(name, description)

    def printStats(self):
        print(self.name + ": " + self.description + " Block: " + str(self.block))

weapons = [weapon("Sword", "A sharp sword", 5), weapon("Axe", "A sharp axe", 7), weapon("Broadsword", "A sharp broadsword", 9)]

armors = [armor("Shield", "A sturdy shield", 2), armor("Chainmail", "A suit of chainmail", 4), armor("Plate", "A suit of plate armor", 6)]