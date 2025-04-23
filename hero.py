from random import randint
from items import Item, Armor, Weapon, equipment_dictionary, armor_dictionary

def mighty_swing(myHero) -> int:
        return myHero.level + myHero.equipment.damage
    
def power_attack(myHero) -> int:
    damage = myHero.equipment.damage + randint(myHero.level, (myHero.level * 2))
    return damage

def backstab(myHero) -> int:
    if myHero.level == 1:
        damage = randint(myHero.level, (myHero.level + 1))
    else:
        damage = randint(myHero.level, (myHero.level * myHero.level))
    return damage

class ClassAction:
    """A class representing a special action or ability that a hero can perform."""
    
    def __init__(self, name:str, description:str, damage_func, cooldown:int=5):
        """Initialize the class action with a name, description, damage function, and cooldown."""
        self.active = 0
        self.name = name
        self.description = description
        self.damage_func = damage_func
        self.cooldown = cooldown
    
    def __str__(self):
        """Returns the name of the class action."""
        return self.name
    
    def use_action(self, myHero):
        """Use the class action and return the damage dealt."""
        print(f"{myHero.name} uses {self.name}!")
        damage = self.damage_func(myHero)
        print(f"{myHero.name} does {damage} damage!")
        return damage
    
class_action_dictionary = {"Mighty Swing": ClassAction("Mighty Swing", "A powerful swing!", mighty_swing),
                        "Power Attack": ClassAction("Power Attack", "A strong attack!", power_attack, 5),
                        "Backstab": ClassAction("Backstab", "A sneaky attack!", backstab, 3)}

class Hero:
    """Base class for all heroes in the game."""

    def __init__(self, name:str="Hero", health:int=10, equipment:Weapon=None, protection:Armor=None, special:ClassAction=class_action_dictionary["Mighty Swing"], gold:int=50):
        """Initialize the hero with a name, health, equipment, protection, special ability, and gold."""
        self.alive = True
        self.image = "knight_image.jpg"
        self.name = name
        self.health = health
        self.max_health = health
        self.equipment = equipment
        self.special = special
        self.protection = protection
        self.level = 1
        self.experience = 0
        self.gold = gold
        
        

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
            "special": str(self.special),  # Convert special to a string
            "equipment": str(self.equipment),  # Convert equipment to a string
            "protection": str(self.protection),  # Convert protection to a string
        }
    
    #Get the damage of the hero's special ability
    def use_special(self):
        """Use the hero's special ability and return the damage dealt."""
        return self.special.use_action(self)
    
    #Take damage from an attacker
    def take_damage(self, damage:int):
        """Reduces the hero's health by the damage taken."""

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
        
        if self.special is not None and self.special.active > 0:
            self.special.active -= 1
            if self.special.active <= 0:
                print(f"{self.name}'s {self.special.name} is ready to use!")
        
        self.health = self.health - damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
            print(f"{self.name} has died!")
        else:
            print(f"{self.name} has taken {damage} damage!")

    #Get the hero's block
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

    #Level up the hero
    #Increase health and damage
    def level_up(self):
        """Level up the hero."""
        self.health += 5
        if self.health > self.max_health:
            self.max_health = self.health
        self.level += 1
        print(self.name + " has leveled up!")
        self.print_stats()
        print()
    
    #Print the hero's stats
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
        dagger = equipment_dictionary["Daggers"]
        leather = armor_dictionary["Leather Armor"]
        special = class_action_dictionary["Backstab"]
        super().__init__(name, health, dagger, leather, special)

class Fighter(Hero):
    """A class representing a Fighter hero."""

    def __init__(self, name:str):
        """Initialize the Fighter with random health and a greatsword."""
        health = randint(10, 15)
        sword = equipment_dictionary["Greatsword"]
        chainmail = armor_dictionary["Chainmail"]
        special = class_action_dictionary["Power Attack"]
        super().__init__(name, health, sword, chainmail, special)

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
