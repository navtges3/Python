from random import randint
from items import Item, Weapon, Armor
from actions import ClassAction

class Inventory:
    def __init__(self):
        self.stuff = []
    
    def addItem(self, item:Item):
        self.stuff.append(item)
    
    def removeItem(self, item:Item):
        if item in self.stuff:
            self.stuff.remove(item)
            print(f"{item} removed from inventory.")
        else:
            print(f"{item} not found in inventory.")

    def printInventory(self):
        if self.stuff:
            print("Inventory:")
            for item in self.stuff:
                print(item)
        else:
            print("Inventory is empty.")

class Hero:
    #Base class for all heroes
    def __init__(self, name:str="Hero", health:int=10, equipment:Item=None, protection:Item=None, special:ClassAction=ClassAction("Mighty Swing")):
        self.name = name
        self.health = health
        self.equipment = equipment
        self.protection = protection
        self.special = special
        self.level = 1
        self.experience = 0
        self.inventory = Inventory()

    #Print the hero's name
    def __str__(self):
        return self.name
    
    #Check if the hero is alive
    def isAlive(self) -> bool:
        return self.health > 0
    
    #Get the damage of the hero's special ability
    def useSpecial(self):
        return self.special.useAction(self)
    
    #Take damage from an attacker
    def takeDamage(self, damage:int):
        self.health = self.health - damage
        print(self.name + " has " + str(self.health) + " health remaining.")

    #Get the hero's block
    def getBlock(self):
        if self.protection is None:
            return 0
        else:
            return self.protection.block

    def gainExperience(self, experience:int):
        self.experience += experience
        if self.experience >= (10 * self.level):
            self.experience = 0
            self.levelUp()

    #Level up the hero
    #Increase health and damage
    def levelUp(self):
        self.health += 5
        self.level += 1
        print(self.name + " has leveled up!")
        self.printStats()
    
    #Print the hero's stats
    def printStats(self):
        print()
        print(self.name + " has " + str(self.health) + " health.")
        print(self.name + " is level " + str(self.level) + " with " + str(self.experience) + " experience.")

        if self.equipment is not None:
            print(self.name + " is wielding a " + str(self.equipment) + ".")
        else:
            print(self.name + " is not wielding any equipment.")

        if self.protection is not None:
            print(self.name + " is wearing " + str(self.protection) + ".")
        else:
            print(self.name + " is not wearing any protection.")
        print()

class Rogue(Hero):
    def __init__(self, name:str):
        health = randint(5, 10)
        dagger = Weapon("Dagger", "A sharp dagger", 2)
        leather = Armor("Leather", "A suit of leather armor", 1)
        special = ClassAction("Backstab")
        super().__init__(name, health, dagger, leather, special)

class Fighter(Hero):
    def __init__(self, name:str):
        health = randint(10, 15)
        sword = Weapon("Sword", "A sharp sword", 5)
        chainmail = Armor("Chainmail", "A suit of chainmail armor", 3)
        special = ClassAction("Power Attack")
        super().__init__(name, health, sword, chainmail, special)

def makeHero() -> Hero:
    theHero = None
    while theHero is None:
        print()
        print("1. Rogue")
        print("2. Fighter")
        print()
        choice = input("What type of hero would you like to be? ")
        if choice == "1":
            name = input("What is your name? ")
            theHero = Rogue(name)
        elif choice == "2":
            name = input("What is your name? ")
            theHero = Fighter(name)
        else:
            print("Invalid choice!")
            theHero = None
    theHero.printStats()
    return theHero 