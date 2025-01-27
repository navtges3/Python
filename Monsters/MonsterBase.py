class monsterBase:

    #Base class for all monsters
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage
        print("A new monster appears!")
        self.printStats()
        
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
        if target.isAlive() != True:
            print(self.name + " has slain " + str(target) + "!")

    #Take damage from an attacker
    def takeDamage(self, damage):
        self.health = self.health - damage
        if self.health < 0:
            self.health = 0
        print(self.name + " has " + str(self.health) + " health remaining.")

    #Print the monster's stats
    def printStats(self):
        print(self.name + " has " + str(self.health) + " health and " + str(self.damage) + " damage.")