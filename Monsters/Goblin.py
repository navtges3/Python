import random
from Monsters.MonsterBase import monsterBase

class goblin(monsterBase):
    healthLow = 5
    healthHigh = 10
    damageLow = 1
    damageHigh = 3
    def __init__(self):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        super().__init__("Goblin", health, damage)