from random import randint
from items import Item, equipmentDictionary, protectionDictionary
from actions import ClassAction, classActionDictionary
from inventory import Inventory

class Hero:
    #Base class for all heroes
    def __init__(self, name:str="Hero", health:int=10, equipment:Item=None, protection:Item=None, special:ClassAction=classActionDictionary["Mighty Swing"]):
        self.name = name
        self.health = health
        self.alive = True
        self.equipment = equipment
        self.protection = protection
        self.special = special
        self.level = 1
        self.experience = 0
        self.gold = 50
        self.inventory = Inventory()
        

    #Print the hero's name
    def __str__(self):
        return self.name
    
    def to_dict(self):
        """Convert the hero object to a dictionary for saving."""
        return {
            "name": self.name,
            "health": self.health,
            "level": self.level,
            "experience": self.experience,
            "special": str(self.special),  # Convert special to a string
            "equipment": str(self.equipment),  # Convert equipment to a string
            "protection": str(self.protection),  # Convert protection to a string
            "inventory": [str(item) for item in self.inventory.items],  # Save inventory items as strings
        }
    
    #Get the damage of the hero's special ability
    def use_special(self):
        return self.special.use_action(self)
    
    #Take damage from an attacker
    def take_damage(self, damage:int):
        self.health = self.health - damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
            print(self.name + " has died!")
        else:
            print(self.name + " has taken " + str(damage) + " damage!")

    #Get the hero's block
    def get_block(self):
        if self.protection is None:
            return 0
        else:
            return self.protection.block

    def add_gold(self, amount):
        self.gold += amount
        print(f"You gained {amount} gold! Total gold: {self.gold}")

    def spend_gold(self, amount) -> bool:
        if self.gold >= amount:
            self.gold -= amount
            print(f"You spent {amount} gold. Remaining gold: {self.gold}")
            return True
        else:
            print("Not enough gold!")
            return False

    def gain_experience(self, experience:int):
        self.experience += experience
        if self.experience >= (10 * self.level):
            self.experience = 0
            self.level_up()

    #Level up the hero
    #Increase health and damage
    def level_up(self):
        self.health += 5
        self.level += 1
        print(self.name + " has leveled up!")
        self.print_stats()
        print()
    
    #Print the hero's stats
    def print_stats(self):
        print()
        print(self.name + " has " + str(self.health) + " health.")
        print(self.name + " is level " + str(self.level) + " with " + str(self.experience) + " experience.")

        if self.equipment is not None:
            print(self.name + " is wielding a " + str(self.equipment) + ".")
        else:
            print(self.name + " is not wielding any equipment.")

        if self.protection is not None:
            print(self.name + " is wearing " + str(self.protection) + ".")
        else:
            print(self.name + " is not wearing any protection.")
        print()

class Rogue(Hero):
    def __init__(self, name:str):
        health = randint(5, 10)
        dagger = equipmentDictionary["Dagger"]
        leather = protectionDictionary["Leather"]
        special = classActionDictionary["Backstab"]
        super().__init__(name, health, dagger, leather, special)

class Fighter(Hero):
    def __init__(self, name:str):
        health = randint(10, 15)
        sword = equipmentDictionary["Sword"]
        chainmail = protectionDictionary["Chainmail"]
        special = classActionDictionary["Power Attack"]
        super().__init__(name, health, sword, chainmail, special)

def make_hero(hero_name:str, hero_class:str) -> Hero:
    the_hero = None
    if hero_class == "Rogue":
        the_hero = Rogue(hero_name)
    elif hero_class == "Fighter":
        the_hero = Fighter(hero_name)
    else:
        the_hero = Hero(hero_name)
    return the_hero 
