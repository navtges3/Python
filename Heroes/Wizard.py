import random
from Heroes.HeroBase import heroBase

class wizard(heroBase):
    healthLow = 5
    healthHigh = 10
    damageLow = 3
    damageHigh = 6
    def __init__(self):
        health = random.randrange(self.healthLow, self.healthHigh)
        damage = random.randrange(self.damageLow, self.damageHigh)
        super().__init__("Wizard", health, damage)
        self.mana = 10
        self.maxMana = 10