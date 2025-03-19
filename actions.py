from random import randint

def mightySwing(myHero) -> int:
        return myHero.level + myHero.equipment.damage
    
def powerAttack(myHero) -> int:
    damage = myHero.equipment.damage + randint(myHero.level, (myHero.level * 2))
    return damage

def backstab(myHero) -> int:
    if myHero.level == 1:
        damage = randint(myHero.level, (myHero.level + 1))
    else:
        damage = randint(myHero.level, (myHero.level * myHero.level))
    return damage

class ClassAction:
    
    def __init__(self, name:str, description:str, damage_func):
        self.name = name
        self.description = description
        self.damage_func = damage_func
    
    def __str__(self):
        return self.name
    
    def useAction(self, myHero):
        print(myHero.name + " uses " + self.name + "!")
        print(self.description)
        damage = self.damage_func(myHero)
        print(myHero.name + " does " + str(damage) + " damage!")
        return damage
    
classActionDictionary = {"Mighty Swing": ClassAction("Mighty Swing", "A powerful swing!", mightySwing),
                        "Power Attack": ClassAction("Power Attack", "A strong attack!", powerAttack),
                        "Backstab": ClassAction("Backstab", "A sneaky attack!", backstab)}