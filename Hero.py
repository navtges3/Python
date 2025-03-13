from random import randint
from items import item, weapon, armor

class classAction:
    def __init__(self, name:str, description:str, damage_func):
        self.name = name
        self.description = description
        self.damage_func = damage_func
    
    def __str__(self):
        return self.name
            
    def useAction(self, myHero):
        print(myHero.name + " uses " + self.name + "!")
        print(self.description)
        damage = self.damage_func(myHero)
        print(myHero.name + " does " + str(damage) + " damage!")
        return damage

class inventory:
    def __init__(self):
        self.items = []
    
    def addItem(self, item):
        self.items.append(item)
    
    def removeItem(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"{item} removed from inventory.")
        else:
            print(f"{item} not found in inventory.")

    def printInventory(self):
        if self.items:
            print("Inventory:")
            for item in self.items:
                print(item)
        else:
            print("Inventory is empty.")

class hero:
    #Mighty Swing
    #Default attack when the hero has no class
    def mightySwing(myHero):
        return myHero.level + myHero.equipment.damage
    
    #Base class for all heroes
    def __init__(self, name:str="Hero", health:int=10, equipment:item=None, protection:item=None, special:classAction=classAction("Mighty Swing", "The hero a powerful swing!", mightySwing)):
        self.name = name
        self.health = health
        self.level = 1
        self.equipment = equipment
        self.protection = protection
        self.special = special
        self.experience = 0

    #Print the hero's name
    def __str__(self):
        return self.name
    
    #Check if the hero is alive
    def isAlive(self):
        if self.health > 0:
            return True
        else:
            return False
    
    #Get the damage of the hero's special ability
    def useSpecial(self):
        return self.special.useAction(self)
    
    #Take damage from an attacker
    def takeDamage(self, damage):
        self.health = self.health - damage
        print(self.name + " has " + str(self.health) + " health remaining.")

    #Get the hero's block
    def getBlock(self):
        if self.protection is None:
            return 0
        else:
            return self.protection.block

    def gainExperience(self, experience):
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

class rogue(hero):
    #Rouge special ability
    #Backstab
    def backstab(myHero):
        if myHero.level == 1:
            damage = randint(myHero.level, (myHero.level + 1))
        else:
            damage = randint(myHero.level, (myHero.level * myHero.level))
        return damage
    
    def __init__(self, name):
        health = randint(5, 10)
        dagger = weapon("Dagger", "A sharp dagger", 2)
        leather = armor("Leather", "A suit of leather armor", 1)
        special = classAction("Backstab", name + " strike from the shadows", rogue.backstab)
        super().__init__(name, health, dagger, leather, special)

class fighter(hero):
    #Fighter special abilility
    #Power Attack
    def powerAttack(myHero):
        damage = myHero.equipment.damage + randint(myHero.level, (myHero.level * 2))
        return damage

    def __init__(self, name):
        health = randint(10, 15)
        sword = weapon("Sword", "A sharp sword", 5)
        chainmail = armor("Chainmail", "A suit of chainmail armor", 3)
        special = classAction("Power Attack", name + " uses all of his strength!", fighter.powerAttack)
        super().__init__(name, health, sword, chainmail, special)

def makeHero() -> hero:
    theHero = None
    while theHero is None:
        print()
        print("1. Rogue")
        print("2. Fighter")
        print()
        choice = input("What type of hero would you like to be? ")
        if choice == "1":
            name = input("What is your name? ")
            theHero = rogue(name)
        elif choice == "2":
            name = input("What is your name? ")
            theHero = fighter(name)
        else:
            print("Invalid choice!")
            theHero = makeHero()
    theHero.printStats()
    return theHero 