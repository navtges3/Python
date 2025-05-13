from random import randint
from items import Item, Armor, Weapon, weapon_dictionary, armor_dictionary
from ui_helpers import *

class Hero:
    """Base class for all heroes in the game."""

    def __init__(self, image, name:str="Hero", health:int=10, weapon:Weapon=None, armor:Armor=None, gold:int=50, border_color:Colors=Colors.BLUE, class_name:str="Hero"):
        """Initialize the hero with a name, health, weapon, armor, and gold."""
        self.alive = True
        self.name = name
        self.health = health
        self.max_health = health
        self.weapon = weapon
        self.armor = armor
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
        self.border_color = border_color
        self.image = image
        self.class_name = class_name


    #Print the hero's name
    def __str__(self):
        """Returns the name of the hero."""
        return self.name
    
    def to_dict(self):
        """Convert the hero object to a dictionary for saving."""
        return {
            "name": self.name,
            "class_name": self.class_name,
            "max_health": self.max_health,
            "health": self.health,
            "level": self.level,
            "experience": self.experience,
            "gold": self.gold,
            "weapon": {
                "name": str(self.weapon),
                "level": self.weapon.level,
                },
            "armor": str(self.armor),
            "potion_bag": self.potion_bag,
        }
    
    def from_dict(self, data):
        """Load the hero object from a dictionary."""
        self.name = data["name"]
        self.class_name = data["class_name"]
        self.max_health = data["max_health"]
        self.health = data["health"]
        self.level = data["level"]
        self.experience = data["experience"]
        self.gold = data["gold"]
        self.weapon = weapon_dictionary[data["weapon"]["level"]][data["weapon"]["name"]]
        self.armor = armor_dictionary[data["armor"]]
        self.potion_bag = data["potion_bag"]
    
    def draw(self, surface, font, x:int=0, y:int=0) -> None:
        # Border
        hero_border = pygame.Rect(x, y, Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT // 2 - 50)

        # Hero Name
        draw_text(self.name, font, Colors.BLACK, surface, hero_border.x + 20, hero_border.y + 10)

        # Hero Image
        surface.blit(self.image, (hero_border.x + 10, hero_border.y + font.get_linesize() + 10))

        # Health Bar
        health_bar_width = 90
        health_bar_height = font.get_linesize() + 4
        health_bar_x = hero_border.x + 15
        health_bar_y = hero_border.y + font.get_linesize() + self.image.get_height() + 15
        draw_health_bar(surface, font, health_bar_x, health_bar_y, health_bar_width, health_bar_height, self.health, self.max_health)

        # Hero Stats
        hero_text = f"Level: {self.level}\nExp: {self.experience}\nGold: {self.gold}"
        draw_multiple_lines(hero_text, font, Colors.BLACK, surface, hero_border.x + self.image.get_width() + 10, hero_border.y + font.get_linesize() + 20)

        potion_text = f"-Health Potion: {self.potion_bag['Health Potion']}\n-Damage Potion: {self.potion_bag['Damage Potion']}\n-Block Potion: {self.potion_bag['Block Potion']}"
        draw_multiple_lines(potion_text, font, Colors.BLACK, surface, hero_border.x + 10, hero_border.y + font.get_linesize() * 2 + self.image.get_height() + 25)

        # Draw the hero's weapon and armor
        # Weapon
        if self.weapon is not None:
            weapon_border = pygame.Rect(hero_border.x + hero_border.width // 2, hero_border.y, hero_border.width // 2, hero_border.height // 3)
            draw_text_centered(self.weapon.name, font, Colors.BLACK, surface, weapon_border.x + weapon_border.width // 2, weapon_border.y + font.get_linesize() // 2 + 10)
            draw_multiple_lines(f"Damage {self.weapon.damage}", font, Colors.BLACK, surface, weapon_border.x + 10, weapon_border.y + font.get_linesize() + 25)
            pygame.draw.rect(surface, Colors.LIGHT_RED, weapon_border, width=3, border_radius=10)
        # Armor
        if self.armor is not None:
            armor_border = pygame.Rect(hero_border.x + hero_border.width // 2 , hero_border.y + hero_border.height // 3, hero_border.width // 2, hero_border.height // 3 * 2)
            draw_text_centered(self.armor.name, font, Colors.BLACK, surface, armor_border.x + armor_border.width // 2, armor_border.y + font.get_linesize() // 2 + 10)
            armor_text = f"Block: {self.armor.block}\nDodge: {self.armor.dodge}\nDuration: {self.armor.duration} turns"
            draw_multiple_lines(armor_text, font, Colors.BLACK, surface, armor_border.x + 10, armor_border.y + font.get_linesize() + 25)
            pygame.draw.rect(surface, Colors.LIGHT_BLUE, armor_border, width=3, border_radius=10)
        
        pygame.draw.rect(surface, Colors.BLUE, hero_border, width=5, border_radius=10)

    def add_item(self, item:Item):
        """Add an item to the hero's inventory."""
        if isinstance(item, Weapon):
            self.weapon = item
            print(f"{self.name} equipped a {item.name}!")
        elif isinstance(item, Armor):
            self.armor = item
            print(f"{self.name} equipped a {item.name}!")
        elif isinstance(item, Item):
            self.add_potion(item.name, 1)

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
                self.potion_damage = 3
                print(f"{self.name} used a Damage Potion! Damage increased by {self.potion_damage}.")
            elif potion_name == "Block Potion":
                self.potion_block = 2
                print(f"{self.name} used a Block Potion! Block increased by {self.potion_block}.")
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

        if self.armor.is_active():
            if self.armor.dodge > 0:
                dodge_roll = randint(1, 100)
                if dodge_roll <= self.armor.dodge:
                    print(f"{self.name} dodged the attack!")
                    damage = 0
            if self.armor.block > 0 and damage > 0:
                damage = damage - self.armor.block
                if damage < 0:
                    damage = 0
                print(f"{self.name} blocked {self.armor.block} damage!")
        
        self.health = self.health - damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
            print(f"{self.name} has died!")
        else:
            print(f"{self.name} has taken {damage} damage!")

        self.armor.update()

    def get_block(self):
        """Returns the block value of the hero's armor."""
        if self.armor is None:
            return 0
        else:
            return self.armor.block

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

        if self.weapon is not None:
            print(f"{self.name} is wielding a {self.weapon}.")
        else:
            print(f"{self.name} is not wielding any weapon.")

        if self.armor is not None:
            print(f"{self.name} is wearing {self.armor}.")
        else:
            print(f"{self.name} is not wearing any armor.")
        print()

class Assassin(Hero):
    """A class representing a Assassin hero."""

    def __init__(self, image, name:str):
        """Initialize the Assassin with random health and a dagger."""
        health = randint(5, 10)
        dagger = weapon_dictionary[1]["Iron Knife"]
        leather = armor_dictionary["Leather Armor"]
        super().__init__(image, name, health, dagger, leather, border_color=Colors.GREEN, class_name="Assassin")

class Knight(Hero):
    """A class representing a Knight hero."""

    def __init__(self, image, name:str):
        """Initialize the Knight with random health and a greatsword."""
        health = randint(10, 15)
        sword = weapon_dictionary[1]["Rusty Sword"]
        chainmail = armor_dictionary["Chainmail"]
        super().__init__(image, name, health, sword, chainmail, border_color=Colors.RED, class_name="Knight")

def make_hero(hero_name:str, hero_class:str, image) -> Hero:
    """Create a hero based on the given name and class."""
    the_hero = None
    if hero_class == "Assassin":
        the_hero = Assassin(image, hero_name)
    elif hero_class == "Knight":
        the_hero = Knight(image, hero_name)
    else:
        the_hero = Hero(image, hero_name)
    return the_hero 
