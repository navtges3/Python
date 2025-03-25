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
        self.print_stats()
        
    def __str__(self):
        return self.name
    
    def is_alive(self) -> bool:
        return self.health > 0

    #Get the monster's damage
    def get_damage(self) -> int:
        return self.damage
    
    #Take damage from an attacker
    def take_damage(self, damage:int):
        self.health = self.health - damage
        if self.health < 0:
            self.health = 0
        print(self.name + " has " + str(self.health) + " health remaining.")

    def drop_loot(self) -> Item:
        return self.loot

    #Print the monster's stats
    def print_stats(self):
        print(self.name + " has " + str(self.health) + " health and " + str(self.damage) + " damage and " + str(self.experience) + " experience.")

class Goblin(Monster):
    healthLow = 5
    healthHigh = 10
    damageLow = 1
    damageHigh = 3
    def __init__(self, name:str="Goblin"):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        loot = lootDictionary["Gold"]
        super().__init__(name, health, damage, loot)

class Orc(Monster):
    healthLow = 10
    healthHigh = 17
    damageLow = 2
    damageHigh = 5
    experience = 2
    def __init__(self, name:str="Orc"):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        loot = lootDictionary["Gem"]
        super().__init__(name, health, damage, loot)

class Ogre(Monster):
    healthLow = 17
    healthHigh = 25
    damageLow = 4
    damageHigh = 8
    experience = 3
    def __init__(self, name:str="Ogre"):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        loot = lootDictionary["Potion"]
        super().__init__(name, health, damage, loot)

def get_monster(level:int) -> Monster:
    if level < 3:
        return Goblin()
    elif level < 6:
        return Orc()
    else:
        return Ogre()

def generate_wave(wave_number:int):
    goblins = []
    for i in range(wave_number):
        goblin = Goblin(f"Goblin {i + wave_number}")
        goblins.append(goblin)
    return goblins