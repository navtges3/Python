from random import randint
from items import Item, Armor, Weapon, weapon_dictionary, armor_dictionary

class Hero:
    """Base class for all heroes in the game."""

    def __init__(self, name:str="Hero", health:int=10, equipment:Weapon=None, protection:Armor=None, gold:int=50):
        """Initialize the hero with a name, health, equipment, protection, and gold."""
        self.alive = True
        self.image = "knight_image.jpg"
        self.name = name
        self.health = health
        self.max_health = health
        self.equipment = equipment
        self.protection = protection
        self.level = 1
        self.experience = 0
        self.gold = gold
        self.potion_bag = {
            "Health Potion": 2,
            "Damage Potion": 1,
            "Block Potion": 1,
        }
        self.potion_damage = 0
        self.potion_block = 0

    #Print the hero's name
    def __str__(self):
        """Returns the name of the hero."""
        return self.name
    
    def to_dict(self):
        """Convert the hero object to a dictionary for saving."""
        return {
            "name": self.name,
            "health": self.health,
            "level": self.level,
            "experience": self.experience,
            "gold": self.gold,
            "equipment": str(self.equipment),
            "protection": str(self.protection),
            "potion_bag": self.potion_bag,
        }
    
    def from_dict(self, data):
        """Load the hero object from a dictionary."""
        self.name = data["name"]
        self.health = data["health"]
        self.level = data["level"]
        self.experience = data["experience"]
        self.gold = data["gold"]
        self.equipment = weapon_dictionary[data["equipment"]]
        self.protection = armor_dictionary[data["protection"]]
        self.potion_bag = data["potion_bag"]
    
    def has_potions(self) -> bool:
        return any(amount > 0 for amount in self.potion_bag.values())
    
    def add_potion(self, potion_name:str, amount:int):
        """Add a potion to the hero's inventory."""
        if potion_name in self.potion_bag:
            self.potion_bag[potion_name] += amount
        else:
            self.potion_bag[potion_name] = amount
        print(f"{amount} {potion_name}(s) added to your inventory!")

    def use_potion(self, potion_name:str):
        """Use a potion from the hero's inventory."""
        if potion_name in self.potion_bag and self.potion_bag[potion_name] > 0:
            if potion_name == "Health Potion":
                self.health += 5
                if self.health > self.max_health:
                    self.health = self.max_health
                print(f"{self.name} used a Health Potion! Health is now {self.health}.")
            elif potion_name == "Damage Potion":
                damage = 2
                print(f"{self.name} used a Damage Potion! Damage increased by {damage}.")
            elif potion_name == "Block Potion":
                block = 2
                print(f"{self.name} used a Block Potion! Block increased by {block}.")
            self.potion_bag[potion_name] -= 1
        else:
            print(f"You don't have any {potion_name}(s) left!")
    
    def take_damage(self, damage:int):
        """Reduces the hero's health by the damage taken."""
        if self.potion_block > 0:
            damage = damage - self.potion_block
            if damage < 0:
                damage = 0
            self.potion_block = 0
        if self.protection is not None and self.protection.active > 0:
            if self.protection.dodge > 0:
                dodge_roll = randint(1, 100)
                if dodge_roll <= self.protection.dodge:
                    print(f"{self.name} dodged the attack!")
                    damage = 0
            if self.protection.block > 0:
                damage = damage - self.protection.block
                if damage < 0:
                    damage = 0
                print(f"{self.name} blocked {self.protection.block} damage!")
            self.protection.active -= 1
            if self.protection.active <= 0:
                print(f"{self.name}'s {self.protection.name} has expired!")
        
        self.health = self.health - damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
            print(f"{self.name} has died!")
        else:
            print(f"{self.name} has taken {damage} damage!")

    def get_block(self):
        """Returns the block value of the hero's protection."""
        if self.protection is None:
            return 0
        else:
            return self.protection.block

    def add_gold(self, amount):
        """Add gold to the hero's inventory."""
        self.gold += amount
        print(f"You gained {amount} gold! Total gold: {self.gold}")

    def spend_gold(self, amount) -> bool:
        """Spend gold from the hero's inventory."""
        if self.gold >= amount:
            self.gold -= amount
            print(f"You spent {amount} gold. Remaining gold: {self.gold}")
            return True
        else:
            print("Not enough gold!")
            return False

    def gain_experience(self, experience:int):
        """Gain experience points."""
        self.experience += experience
        if self.experience >= (10 * self.level):
            self.experience = 0
            self.level_up()

    def level_up(self):
        """Level up the hero."""
        self.health += 5
        if self.health > self.max_health:
            self.max_health = self.health
        self.level += 1
        print(self.name + " has leveled up!")
        self.print_stats()
        print()
    
    def print_stats(self):
        """Prints the hero's stats."""
        print()
        print(f"{self.name} has {self.health} health.")
        print(f"{self.name} is level {self.level} with {self.experience} experience.")

        if self.equipment is not None:
            print(f"{self.name} is wielding a {self.equipment}.")
        else:
            print(f"{self.name} is not wielding any equipment.")

        if self.protection is not None:
            print(f"{self.name} is wearing {self.protection}.")
        else:
            print(f"{self.name} is not wearing any protection.")
        print()

class Rogue(Hero):
    """A class representing a Rogue hero."""

    def __init__(self, name:str):
        """Initialize the Rogue with random health and a dagger."""
        health = randint(5, 10)
        dagger = weapon_dictionary["Daggers"]
        leather = armor_dictionary["Leather Armor"]
        super().__init__(name, health, dagger, leather)

class Fighter(Hero):
    """A class representing a Fighter hero."""

    def __init__(self, name:str):
        """Initialize the Fighter with random health and a greatsword."""
        health = randint(10, 15)
        sword = weapon_dictionary["Greatsword"]
        chainmail = armor_dictionary["Chainmail"]
        super().__init__(name, health, sword, chainmail)

def make_hero(hero_name:str, hero_class:str) -> Hero:
    """Create a hero based on the given name and class."""
    the_hero = None
    if hero_class == "Rogue":
        the_hero = Rogue(hero_name)
    elif hero_class == "Fighter":
        the_hero = Fighter(hero_name)
    else:
        the_hero = Hero(hero_name)
    return the_hero 
