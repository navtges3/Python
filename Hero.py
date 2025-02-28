class hero:
    
    #Base class for all heroes
    def __init__(self, name, health, strength, weapon):
        self.name = name
        self.health = health
        self.strength = strength
        self.monstersSlain = 0
        self.level = 1
        self.weapon = weapon

    #Print the hero's name
    def __str__(self):
        return self.name
    
    #Check if the hero is alive
    def isAlive(self):
        if self.health > 0:
            return True
        else:
            return False
    
    #Attack the target
    def attack(self, target):
        damage = self.strength + self.weapon.damage
        print(self.name + " Attacks " + target.name + " dealing " + str(damage) + " damage.")
        target.takeDamage(damage)
        if not target.isAlive():
            self.monstersSlain += 1
            print(self.name + " has slain " + str(target) + "!")
            
    #Take damage from an attacker
    def takeDamage(self, damage):
        self.health = self.health - damage
        print(self.name + " has " + str(self.health) + " health remaining.")

    #Level up the hero
    #Increase health and damage
    def levelUp(self):
        self.health += 5
        self.strength += 2
        self.level += 1
        print(self.name + " has leveled up!")
        self.printStats()
    
    #Print the hero's stats
    def printStats(self):
        print(self.name + " has " + str(self.health) + " health.")
        print(self.name + " is level " + str(self.level) + ".")
        print(self.name + " is wielding a " + str(self.weapon) + ".")
        print(self.name + " has slain " + str(self.monstersSlain) + " monsters.")