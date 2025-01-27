import random
from Heroes.HeroBase import heroBase

class fighter(heroBase):
    healthLow = 10
    healthHigh = 20
    damageLow = 2
    damageHigh = 5
    def __init__(self):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        super().__init__("Fighter", health, damage)