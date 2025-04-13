import random

#Base class for all monsters
class Monster:
    def __init__(self, name:str, health:int, damage:int, image:str="goblin_image.jpg"):
        self.name = name
        self.health = health
        self.alive = True
        self.damage = damage
        self.experience = (health + damage) // 2
        self.image = image
        print("A new monster appears!")
        self.print_stats()
        
    def __str__(self):
        return self.name

    def get_damage(self) -> int:
        return self.damage
    
    def take_damage(self, damage:int):
        self.health = self.health - damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
        print(f"{self.name} has {self.health} health remaining.")

    def print_stats(self):
        print(f"{self.name} has {self.health} health and {self.damage} damage and {self.experience} experience.")

class Goblin(Monster):
    healthLow = 5
    healthHigh = 10
    damageLow = 1
    damageHigh = 3
    def __init__(self, name:str="Goblin"):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        super().__init__(name, health, damage, image="goblin_image.jpg")

class Orc(Monster):
    healthLow = 10
    healthHigh = 17
    damageLow = 2
    damageHigh = 5
    experience = 2
    def __init__(self, name:str="Orc"):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        super().__init__(name, health, damage, image="orc_image.jpg")

class Ogre(Monster):
    healthLow = 17
    healthHigh = 25
    damageLow = 4
    damageHigh = 8
    experience = 3
    def __init__(self, name:str="Ogre"):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        super().__init__(name, health, damage, image="ogre_image.jpg")

def get_monster(level:int) -> Monster:
    if level < 3:
        return Goblin()
    elif level < 6:
        return Orc()
    else:
        return Ogre()