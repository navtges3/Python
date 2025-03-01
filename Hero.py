from random import randint

class hero:
    
    #Base class for all heroes
    def __init__(self, name, health, weapon, armor):
        self.name = name
        self.health = health
        self.monstersSlain = 0
        self.level = 1
        self.weapon = weapon
        self.armor = armor

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
    def getDamage(self):
        if self.weapon is None:
            damage = self.level
        elif self.level > randint(1, 10):
            print("Critical Hit!")
            damage = self.weapon.damage * 2
        else:
            damage = self.weapon.damage
        return damage
    
    #Take damage from an attacker
    def takeDamage(self, damage):
        if self.armor is not None and self.armor.block > randint(1, 10):
            print("Block!")
            damage = damage / 2
        else:
            damage = damage
        self.health = self.health - damage
        print(self.name + " has " + str(self.health) + " health remaining.")

    #Level up the hero
    #Increase health and damage
    def levelUp(self):
        self.health += 5
        self.level += 1
        print(self.name + " has leveled up!")
        self.printStats()
    
    #Print the hero's stats
    def printStats(self):
        print(self.name + " has " + str(self.health) + " health.")
        print(self.name + " is level " + str(self.level) + ".")
        print(self.name + " has slain " + str(self.monstersSlain) + " monsters.")
        if self.weapon is not None:
            print(self.name + " is wielding a " + str(self.weapon) + ".")
        else:
            print(self.name + " is not wielding any weapon.")
        if self.armor is not None:
            print(self.name + " is wearing " + str(self.armor) + ".")
        else:
            print(self.name + " is not wearing any armor.")