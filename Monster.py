from items import Item, lootDictionary
import random

class Monster:

    #Base class for all monsters
    def __init__(self, name:str, health:int, damage:int, loot:Item=None):
        self.name = name
        self.health = health
        self.damage = damage
        self.experience = (health + damage) // 2
        self.loot = loot
        print("A new monster appears!")
        self.printStats()
        
    def __str__(self):
        return self.name
    
    def isAlive(self) -> bool:
        if self.health > 0:
            return True
        else:
            return False

    #Get the monster's damage
    def getDamage(self) -> int:
        return self.damage
    
    #Take damage from an attacker
    def takeDamage(self, damage:int):
        self.health = self.health - damage
        if self.health < 0:
            self.health = 0
        print(self.name + " has " + str(self.health) + " health remaining.")

    def drop_loot(self) -> Item:
        return self.loot

    #Print the monster's stats
    def printStats(self):
        print(self.name + " has " + str(self.health) + " health and " + str(self.damage) + " damage and " + str(self.experience) + " experience.")

class Goblin(Monster):
    healthLow = 5
    healthHigh = 10
    damageLow = 1
    damageHigh = 3
    def __init__(self):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        loot = lootDictionary["Gold"]
        super().__init__("Goblin", health, damage, loot)

class Orc(Monster):
    healthLow = 10
    healthHigh = 17
    damageLow = 2
    damageHigh = 5
    experience = 2
    def __init__(self):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        loot = lootDictionary["Gem"]
        super().__init__("Orc", health, damage, loot)

class Ogre(Monster):
    healthLow = 17
    healthHigh = 25
    damageLow = 4
    damageHigh = 8
    experience = 3
    def __init__(self):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        loot = lootDictionary["Potion"]
        super().__init__("Ogre", health, damage, loot)

def getMonster(level:int) -> Monster:
    if level < 3:
        return Goblin()
    elif level < 6:
        return Orc()
    else:
        return Ogre()