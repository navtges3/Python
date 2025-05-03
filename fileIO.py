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
        # Load idle animation frames
            idle_frames = [
                pygame.image.load(resource_path("images/knight/knight1.jpg")).convert(),
                pygame.image.load(resource_path("images/knight/knight2.jpg")).convert(),
                pygame.image.load(resource_path("images/knight/knight3.jpg")).convert(),
                pygame.image.load(resource_path("images/knight/knight4.jpg")).convert(),
                pygame.image.load(resource_path("images/knight/knight5.jpg")).convert(),
            ]

            # Scale the frames to the desired size
            idle_frames = [pygame.transform.scale(frame, (100, 100)) for frame in idle_frames]
            hero = Hero(idle_frames)
            hero.from_dict(data["hero"])
            return hero
    except FileNotFoundError:
        print("No save file found. Starting a new game.")
        return None
    except Exception as e:
        print(f"Error loading game: {e}")
        return None