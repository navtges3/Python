from Heroes.HeroBase import heroBase as hero
from Monsters.Goblin import goblin
from Monsters.Orc import orc
from Monsters.Ogre import ogre
from Util.IOHelper import getInput

print("Welcome to Hero vs Goblin!")
print("You are a hero, and you have to fight a goblin!")
print("The battle is on!")
print("What is your hero's name?")
name = input()

myHero = hero(name, 20, 5)
myMonster = goblin()

defaultInput = "A"
inputPrompt = "Do you wish to (A)ttack or (F)lee?"
action = getInput(defaultInput, inputPrompt)
while myHero.isAlive() and action[0].lower() == "a":
    myHero.attack(myMonster)
    #If the monster is still alive, have it attack the hero
    if myMonster.isAlive():
        myMonster.attack(myHero)
        #Exit loop if hero is dead
        if myHero.isAlive() == False:
            break
        defaultInput = "A"
        inputPrompt = "The monster still lives! Do you wish to (A)ttack or (F)lee?"
    #If the monster is dead, level up the hero and get a new monster
    else:
        if myHero.monstersSlain % 5 == 0:
            myHero.levelUp()
        if myHero.monstersSlain > 10 and myHero.monstersSlain < 20:
            myMonster = orc()
        elif myHero.monstersSlain > 20:
            myMonster = ogre()
        else:
            myMonster = goblin()
        defaultInput = "A"
        inputPrompt = "Do you wish to (A)ttack another monster or (F)lee?"
    #Get the next action from the user
    action = getInput(defaultInput, inputPrompt)
    
if myHero.isAlive():
    if myHero.monstersSlain > 0:
        print(str(myHero) + " retired victorious from the battle after slaying " + str(myHero.monstersSlain) + " monster!")
    else:
        print(str(myHero) + " escaped before being defeated by " + str(myMonster) + "!")
else:
    print(str(myHero) + " was defeated in battle by " + str(myMonster) + " after slaying " + str(myHero.monstersSlain) + " monsters!")

print("The battle is over!")
myHero.printStats()
print("Press Enter to exit.")
input()