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

damage_functions = {
    "Mighty Swing": mightySwing,
    "Power Attack": powerAttack,
    "Backstab": backstab
}

descriptions = {
    "Mighty Swing": "A powerful swing!",
    "Power Attack": "A strong attack!",
    "Backstab": "A sneaky attack!"
}

class ClassAction:
    
    def __init__(self, name:str):
        self.name = name
        self.description = descriptions[name]
        self.damage_func = damage_functions[name]
    
    def __str__(self):
        return self.name
    
    def useAction(self, myHero):
        print(myHero.name + " uses " + self.name + "!")
        print(self.description)
        damage = self.damage_func(myHero)
        print(myHero.name + " does " + str(damage) + " damage!")
        return damage