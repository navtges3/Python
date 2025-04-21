from hero import Hero, class_action_dictionary
from items import equipment_dictionary, protection_dictionary
import json
import os
import sys


def resource_path(relative_path: str) -> str:
    """Get the absolute path to the resource, works for dev and PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def save_game(hero):
    """Save the hero's progress to a file."""
    try:
        with open("savefile.json", "w") as savefile:
            # Convert hero object to a dictionary and save it as JSON
            save_data = {"hero": hero.to_dict()}
            json.dump(save_data, savefile, indent=4)
        print("Game saved successfully!")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game() -> Hero:
    """Load the hero's progress from a file."""
    try:
        with open("savefile.json", "r") as savefile:
            # Load the hero data from the JSON file
            data = json.load(savefile)
            hero_data = data["hero"]
            # Recreate the hero object from the saved data
            hero = Hero(
                name=hero_data["name"],
                health=hero_data["health"],
                equipment=equipment_dictionary[hero_data["equipment"]],
                protection=protection_dictionary[hero_data["protection"]],
                special=class_action_dictionary[hero_data["special"]],
                gold=hero_data["gold"]
            )
            hero.level = hero_data["level"]
            hero.experience = hero_data["experience"]
            print("Game loaded successfully!")
            return hero
    except FileNotFoundError:
        print("No save file found. Starting a new game.")
        return None
    except Exception as e:
        print(f"Error loading game: {e}")
        return None