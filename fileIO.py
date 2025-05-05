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
            if "hero" not in data:
                raise ValueError("No hero data found in save file.")
            else:
                if data["hero"]["class_name"] == "Knight":
                    hero_image = pygame.image.load(resource_path("images/knight.png")).convert()
                elif data["hero"]["class_name"] == "Assassin":
                    hero_image = pygame.image.load(resource_path("images/assassin.png")).convert()
                else:
                    hero_image = pygame.image.load(resource_path("images/knight.png")).convert()
                hero_image = pygame.transform.scale(hero_image, (100, 100))
                hero = Hero(hero_image)
                hero.from_dict(data["hero"])
                return hero
    except FileNotFoundError:
        print("No save file found. Starting a new game.")
        return None
    except Exception as e:
        print(f"Error loading game: {e}")
        return None