import random

class monster:

    #Base class for all monsters
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage
        print("A new monster appears!")
        self.printStats()
        
    def __str__(self):
        return self.name
    
    def isAlive(self):
        if self.health > 0:
            return True
        else:
            return False

    #Get the monster's damage
    def getDamage(self):
        return self.damage
    
    #Take damage from an attacker
    def takeDamage(self, damage):
        self.health = self.health - damage
        if self.health < 0:
            self.health = 0
        print(self.name + " has " + str(self.health) + " health remaining.")

    #Print the monster's stats
    def printStats(self):
        print(self.name + " has " + str(self.health) + " health and " + str(self.damage) + " damage.")

class goblin(monster):
    healthLow = 5
    healthHigh = 10
    damageLow = 1
    damageHigh = 3
    def __init__(self):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        super().__init__("Goblin", health, damage)

class orc(monster):
    healthLow = 10
    healthHigh = 17
    damageLow = 2
    damageHigh = 5
    def __init__(self):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        super().__init__("Orc", health, damage)

class ogre(monster):
    healthLow = 17
    healthHigh = 25
    damageLow = 4
    damageHigh = 8
    def __init__(self):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        super().__init__("Ogre", health, damage)