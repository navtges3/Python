from hero import Hero
import pygame
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

def save_game(save_data):
    """Save the hero's progress to a file."""
    try:
        with open("savefile.json", "w") as savefile:
            # Convert hero object to a dictionary and save it as JSON
            json.dump(save_data, savefile, indent=4)
        print("Game saved successfully!")
    except Exception as e:
        print(f"Error saving game: {e}")

def save_file_exists() -> bool:
    """Check if a save file exists.
    
    Returns:
        bool: True if save file exists, False otherwise
    """
    return os.path.exists("savefile.json")

def load_game() -> dict:
    """Load the hero's progress from a file."""
    try:
        with open("savefile.json", "r") as savefile:
            # Load the hero data from the JSON file
            data = json.load(savefile)
            return data
    except FileNotFoundError:
        print("No save file found. Starting a new game.")
        return None
    except Exception as e:
        print(f"Error loading game: {e}")
        return None