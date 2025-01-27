import random
from Monsters.MonsterBase import monsterBase

class ogre(monsterBase):
    healthLow = 17
    healthHigh = 25
    damageLow = 4
    damageHigh = 8
    def __init__(self):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        super().__init__("Ogre", health, damage)