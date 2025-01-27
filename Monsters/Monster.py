class monster:
    
    def isAlive(self):
        if self.health > 0:
            return True
        else:
            return False

    def attack(self, target):
        print(self.name + " Attacks " + target.name + " dealing " + str(self.damage) + " damage.")
        target.takeDamage(self.damage)
        if target.isAlive() != True:
            print(self.name + " has slain " + target.name)

    def takeDamage(self, damage):
        self.health = self.health - damage
        print(self.name + " has " + str(self.health) + " remaining.")