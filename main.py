from hero import Hero, makeHero
from monster import Monster, Goblin, Orc, Ogre, getMonster
from items import equipmentDictionary, protectionDictionary, lootDictionary
from actions import classActionDictionary
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
                equipment=equipmentDictionary[data["equipment"]],
                protection=protectionDictionary[data["protection"]],
                special=classActionDictionary[data["special"]]
            )
            hero.level = data["level"]
            hero.experience = data["experience"]
            # Load inventory items
            for item_name in data["inventory"]:
                hero.inventory.add_item(lootDictionary[item_name])
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

def battle(hero, myMonster) -> None:
    while myMonster.isAlive() and hero.isAlive():
        print()
        print("1. Defend with your " + str(hero.protection))
        print("2. Use your " + str(hero.equipment))
        print("3. Use your " + str(hero.special))
        print("4. Run away")
        print("5. View Inventory")
        print()
        choice = input("What would you like to do? ")
        if choice == "1":
            print("You defend!")
            damage = myMonster.getDamage() - hero.getBlock()
            if damage < 0:
                damage = 0
            hero.takeDamage(damage)
        elif choice == "2":
            # Hero attacks first
            myMonster.takeDamage(hero.equipment.damage)
            # If the monster is still alive, it attacks back
            if myMonster.isAlive():
                hero.takeDamage(myMonster.getDamage())
        elif choice == "3":
            print("You use your special ability!")
            myMonster.takeDamage(hero.useSpecial())
            if myMonster.isAlive():
                hero.takeDamage(myMonster.getDamage())
        elif choice == "4":
            print("You run away!")
            break
        elif choice == "5":
            hero.inventory.show_inventory()
        else:
            print("Invalid choice!")

def shop(hero: Hero):
    """Allow the hero to buy items from the shop."""
    print("\nWelcome to the shop!")
    print("You have " + str(hero.gold) + " gold.")
    print("1. Buy Weapons")
    print("2. Buy Armor")
    print("3. Buy Items")
    print("4. Exit Shop")
    
    choice = input("What would you like to do? ")
    if choice == "1":
        print("\nWeapons for sale:")
        for name, weapon in equipmentDictionary.items():
            print(f"{name}: {weapon.description} (Damage: {weapon.damage}) - {weapon.value} gold")
        weapon_choice = input("Which weapon would you like to buy? ")
        if weapon_choice in equipmentDictionary:
            if hero.spend_gold(equipmentDictionary[weapon_choice].value):
                hero.inventory.add_item(equipmentDictionary[weapon_choice])
        else:
            print("Invalid choice!")
    elif choice == "2":
        print("\nArmor for sale:")
        for name, armor in protectionDictionary.items():
            print(f"{name}: {armor.description} (Block: {armor.block}) - {armor.value} gold")
        armor_choice = input("Which armor would you like to buy? ")
        if armor_choice in protectionDictionary:
            if hero.spend_gold(protectionDictionary[armor_choice].value):
                hero.inventory.add_item(protectionDictionary[armor_choice])
        else:
            print("Invalid choice!")
    elif choice == "3":
        print("\nItems for sale:")
        for name, item in lootDictionary.items():
            print(f"{name}: {item.description} - {item.value} gold")
        item_choice = input("Which item would you like to buy? ")
        if item_choice in lootDictionary:
            if hero.spend_gold(lootDictionary[item_choice].value):
                hero.inventory.add_item(lootDictionary[item_choice])
        else:
            print("Invalid choice!")
    elif choice == "4":
        print("Thank you for visiting the shop!")
    else:
        print("Invalid choice!")    

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
                print(f"You defeated the {myMonster.name}!")
                loot = myMonster.drop_loot()  # Assume monsters have a drop_loot method
                if loot:
                    print(f"You found {loot}!")
                    myHero.inventory.add_item(loot)
        else:
            print(str(myHero) + " was defeated by the " + str(myMonster) + "!")
        
        #Ask if the hero wants to continue
        if myHero.isAlive():
            print()
            print("1. Fight another monster")
            print("2. Shop")
            print("3. Retire")
            print()
            choice = input("What would you like to do? ")
            if choice == "2":
                shop(myHero)
            elif choice == "3":
                continueFight = False
            else:
                continueFight = True
    
    myHero.printStats()
    print("1. Save and exit")
    print("2. Exit without saving")
    choice = input("What would you like to do? ")
    if choice == "1":
        save_game(myHero)

if __name__ == "__main__":
    main()