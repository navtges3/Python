from random import randint
from items import weapon, armor

class hero:
    
    #Base class for all heroes
    def __init__(self, name, health, weapon, armor, special="Special Attack"):
        self.name = name
        self.health = health
        self.level = 1
        self.weapon = weapon
        self.armor = armor
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
    
    #Get the hero's damage        
    def getSpecial(self):
        print(self.name + " makes a mighty swing!")
        damage = self.level + self.weapon.damage
        print(self.name + " does " + str(damage) + " damage!")
        return damage
    
    #Take damage from an attacker
    def takeDamage(self, damage):
        self.health = self.health - damage
        print(self.name + " has " + str(self.health) + " health remaining.")

    #Get the hero's block
    def getBlock(self):
        if self.armor is None:
            return 0
        else:
            return self.armor.block

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

        if self.weapon is not None:
            print(self.name + " is wielding a " + str(self.weapon) + ".")
        else:
            print(self.name + " is not wielding any weapon.")

        if self.armor is not None:
            print(self.name + " is wearing " + str(self.armor) + ".")
        else:
            print(self.name + " is not wearing any armor.")
        print()

class rogue(hero):
    def __init__(self, name):
        health = randint(5, 10)
        dagger = weapon("Dagger", "A sharp dagger", 2)
        leather = armor("Leather", "A suit of leather armor", 1)
        special = "Backstab"
        super().__init__(name, health, dagger, leather, special)

    def getSpecial(self):
        print(self.name + " strikes from the shadows!")
        if self.level == 1:
            damage = randint(self.level, (self.level + 1))
        else:
            damage = randint(self.level, (self.level * 2))
        print(self.name + " does " + str(damage) + " damage!")
        return damage

class fighter(hero):
    def __init__(self, name):
        health = randint(10, 15)
        sword = weapon("Sword", "A sharp sword", 5)
        chainmail = armor("Chainmail", "A suit of chainmail armor", 3)
        special = "Power Attack"
        super().__init__(name, health, sword, chainmail, special)
    
    def getSpecial(self):
        print(self.name + " uses all of his strength!")
        if self.level == 1:
            damage =  randint(self.level, (self.level + 1))
        else:
            damage = randint(self.level, (self.level * 2))
        print(self.name + " does " + str(damage) + " damage!")
        return damage

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