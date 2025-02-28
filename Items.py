class item:
    def __init__(self, name, description, damage):
        self.name = name
        self.description = description
        self.damage = damage

    def __str__(self):
        return self.name
    
    def printStats(self):
        print(self.name + " is a " + self.description + " dealing " + str(self.damage) + " damage.")
    
items = [item("Sword", "A sharp sword", 5), item("Axe", "A sharp axe", 7), item("Dagger", "A sharp dagger", 3)]