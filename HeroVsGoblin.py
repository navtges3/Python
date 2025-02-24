from Heroes.HeroBase import heroBase as hero
from Monsters.Goblin import goblin
from Monsters.Orc import orc
from Monsters.Ogre import ogre

print("Welcome to Hero vs Goblin!")
print("You are a hero, and you have to fight a goblin!")
print("The battle is on!")
print("What is your hero's name?")
name = input()

myHero = hero(name, 20, 5)
myMonster = goblin()

while myHero.isAlive():
    myHero.attack(myMonster)
    if myMonster.isAlive():
        myMonster.attack(myHero)
        if myHero.isAlive() == True:
            print("Do you wish to continue the battle? (y/n)")
            stay = input()
            if len(stay) == 0:
                stay = "y"
            if stay[0] == "n":
                break
        else:
            break
    else:
        print("Do you wish to stay and fight another goblin? (y/n)")
        stay = input()
        if len(stay) == 0:
            stay = "y"
        if stay[0] == "n":
            break
        else:
            if myHero.monstersSlain % 5 == 0:
                myHero.levelUp()
            if myHero.monstersSlain > 10 and myHero.monstersSlain < 20:
                myMonster = orc()
            elif myHero.monstersSlain > 20:
                myMonster = ogre()
            else:
                myMonster = goblin()
    
if myHero.isAlive():
    if myHero.monstersSlain > 0:
        print(str(myHero) + "retired victorious from the battle after slaying " + str(myHero.monstersSlain) + " monster!")
    else:
        print(str(myHero) + " escaped before being defeated by " + str(myMonster) + "!")
else:
    print(str(myHero) + " was defeated in battle by " + str(myMonster) + " after slaying " + str(myHero.monstersSlain) + " monsters!")

print("The battle is over!")
myHero.printStats()
print("Press Enter to exit.")
input()