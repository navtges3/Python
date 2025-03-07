from hero import hero, makeHero
from monster import monster, goblin, orc, ogre, getMonster
import items

def welcome() -> None:
    print("Welcome to Hero vs Goblin!")

def battle(myHero, myMonster) -> None:
    while myMonster.isAlive() and myHero.isAlive():
        print()
        print("1. Fight")
        print("2. Defend")
        print("3. Run")
        print()
        choice = input("What would you like to do? ")
        if choice == "1":
            #Hero attacks first
            myMonster.takeDamage(myHero.getDamage())
            #If the monster is still alive, it attacks back
            if myMonster.isAlive():
                myHero.takeDamage(myMonster.getDamage())
        elif choice == "2":
            print("You defend!")
            damage = myMonster.getDamage() - myHero.getBlock()
            if damage < 0:
                damage = 0
            myHero.takeDamage(damage)
        elif choice == "3":
            print("You run away!")
            break
        else:
            print("Invalid choice!")

def retire() -> bool:
    print()
    print("1. Fight another monster")
    print("2. Retire")
    print()
    choice = input("What would you like to do? ")
    if choice == "2":
        return True
    else:
        return False

def main() -> None:
    welcome()
    myHero = makeHero()
    continueFight = True
    while myHero.isAlive() and continueFight:
        #Create a random monster
        myMonster = getMonster(myHero.level)
        
        #Battle the monster
        battle(myHero, myMonster)
        if myHero.isAlive():
            if myMonster.isAlive():
                print("You ran away from the " + str(myMonster) + "!")
            else:
                print("You defeated the " + str(myMonster) + "!")
                myHero.gainExperience(myMonster.experience)
        else:
            print("You were defeated by the " + str(myMonster) + "!")
        
        #Ask if the hero wants to continue
        if retire():
            continueFight = False
    
    print("Game Over!")
    myHero.printStats()
    input("Press Enter to close the program.")

if __name__ == "__main__":
    main()