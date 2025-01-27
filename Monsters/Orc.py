import random
from Monsters.MonsterBase import monsterBase

class orc(monsterBase):
    healthLow = 10
    healthHigh = 17
    damageLow = 2
    damageHigh = 5
    def __init__(self):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        super().__init__("Orc", health, damage)