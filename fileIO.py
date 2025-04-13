from hero import Hero, class_action_dictionary
from items import equipmentDictionary, protectionDictionary, lootDictionary
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

def load_game() -> Hero:
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
                special=class_action_dictionary[data["special"]],
                gold=data["gold"]
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