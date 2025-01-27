class heroBase:
    
    #Base class for all heroes
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage
        self.monstersSlain = 0

    def __str__(self):
        return self.name
    
    def isAlive(self):
        if self.health > 0:
            return True
        else:
            return False
    
    #Attack the target
    def attack(self, target):
        print(self.name + " Attacks " + target.name + " dealing " + str(self.damage) + " damage.")
        target.takeDamage(self.damage)
        if not target.isAlive():
            self.monstersSlain += 1
            print(self.name + " has slain " + str(target) + "!")
            
    #Take damage from an attacker
    def takeDamage(self, damage):
        self.health = self.health - damage
        print(self.name + " has " + str(self.health) + " health remaining.")  