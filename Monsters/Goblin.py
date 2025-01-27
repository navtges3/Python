import Monster

class goblin(Monster.monster):
    def __init__(self, health, damage):
        self.name = "Goblin"
        self.health = health
        self.damage = damage

    def isAlive(self):
        return super().isAlive()
        
    def attack(self, target):
        super().attack(target)
    
    def takeDamage(self, damage):
        super().takeDamage(damage)