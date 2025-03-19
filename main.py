from hero import Hero, makeHero
from monster import Monster, Goblin, Orc, Ogre, getMonster
from items import equipment, protection
from actions import ClassAction
import json

def save_game(hero):
    """Save the hero's progress to a file."""
    try:
        with open("savefile.json", "w") as savefile:
            # Convert hero object to a dictionary and save it as JSON
            json.dump(hero.to_dict(), savefile, indent=4)
        print("Game saved successfully!")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game():
    """Load the hero's progress from a file."""
    try:
        with open("savefile.json", "r") as savefile:
            # Load the hero data from the JSON file
            data = json.load(savefile)
            # Recreate the hero object from the saved data
            hero = Hero(
                name=data["name"],
                health=data["health"],
                equipment=equipment[data["equipment"]],
                protection=protection[data["protection"]],
                special=ClassAction(data["special"])
            )
            hero.level = data["level"]
            hero.experience = data["experience"]
            print("Game loaded successfully!")
            return hero
    except FileNotFoundError:
        print("No save file found. Starting a new game.")
        return None
    except Exception as e:
        print(f"Error loading game: {e}")
        return None
    
def welcome() -> None:
    print("Welcome to Hero vs Goblin!")

def battle(myHero, myMonster) -> None:
    while myMonster.isAlive() and myHero.isAlive():
        print()
        print("1. Use your " + str(myHero.equipment))
        print("2. Defend with your " + str(myHero.protection))
        print("3. Use your " + str(myHero.special))
        print("4. Run away")
        print()
        choice = input("What would you like to do? ")
        if choice == "1":
            #Hero attacks first
            myMonster.takeDamage(myHero.equipment.damage)
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
            print("You use your special ability!")
            myMonster.takeDamage(myHero.useSpecial())
            if myMonster.isAlive():
                myHero.takeDamage(myMonster.getDamage())
        elif choice == "4":
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
    print("1. Start a new game")
    print("2. Load a saved game")
    choice = input("What would you like to do? ")
    if choice == "2":
        myHero = load_game()
    else:
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
            print(str(myHero) + " was defeated by the " + str(myMonster) + "!")
        
        #Ask if the hero wants to continue
        if myHero.isAlive():
            continueFight = not retire()
    
    myHero.printStats()
    print("1. Save and exit")
    print("2. Exit without saving")
    choice = input("What would you like to do? ")
    if choice == "1":
        save_game(myHero)

if __name__ == "__main__":
    main()