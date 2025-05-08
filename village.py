from ui_helpers import *
from constants import *
from items import *
from hero import *
import random
import pygame

class Shop:
    def __init__(self, font):
        self.potion_key = random.choice(list(potion_dictionary.keys()))
        self.weapon_key = random.choice(list(weapon_dictionary.keys()))
        self.armor_key = random.choice(list(armor_dictionary.keys()))
        self.card_selected_key = Shop_Constants.POTION_CARD_KEY
        self.selected_price = potion_dictionary[self.potion_key].value
        self.cards = {
            Shop_Constants.POTION_CARD_KEY:  Button(Shop_Constants.POTION_CARD_KEY, (Game_Constants.SCREEN_WIDTH // 8, 25), (Game_Constants.SCREEN_WIDTH // 16 * 3, Game_Constants.SCREEN_HEIGHT // 3), font, Colors.BLACK, Colors.LIGHT_GRAY, Colors.GRAY),
            Shop_Constants.WEAPON_CARD_KEY:  Button(Shop_Constants.WEAPON_CARD_KEY, (Game_Constants.SCREEN_WIDTH // 32 * 13, 25), (Game_Constants.SCREEN_WIDTH // 16 * 3, Game_Constants.SCREEN_HEIGHT // 3), font, Colors.BLACK, Colors.LIGHT_RED, Colors.RED),
            Shop_Constants.ARMOR_CARD_KEY:   Button(Shop_Constants.ARMOR_CARD_KEY, (Game_Constants.SCREEN_WIDTH // 16 * 11, 25), (Game_Constants.SCREEN_WIDTH // 16 * 3, Game_Constants.SCREEN_HEIGHT // 3), font, Colors.BLACK, Colors.LIGHT_BLUE, Colors.BLUE),
        }

    def new_card(self, card_name: str) -> None:
        """Change the card in the shop."""
        if card_name == Shop_Constants.POTION_CARD_KEY:
            self.potion_key = random.choice(list(potion_dictionary.keys()))
            self.selected_price = potion_dictionary[self.potion_key].value
        elif card_name == Shop_Constants.WEAPON_CARD_KEY:
            self.weapon_key = random.choice(list(weapon_dictionary.keys()))
            self.selected_price = weapon_dictionary[self.weapon_key].value
        elif card_name == Shop_Constants.ARMOR_CARD_KEY:
            self.armor_key = random.choice(list(armor_dictionary.keys()))
            self.selected_price = armor_dictionary[self.armor_key].value
        self.card_selected_key = card_name

    def card_selected(self, card_name: str) -> None:
        """Stelect a card in the shop."""
        print(f"Selected card: {card_name}")
        if card_name == Shop_Constants.POTION_CARD_KEY:
            self.selected_price = potion_dictionary[self.potion_key].value
        elif card_name == Shop_Constants.WEAPON_CARD_KEY:
            self.selected_price = weapon_dictionary[self.weapon_key].value
        elif card_name == Shop_Constants.ARMOR_CARD_KEY:
            self.selected_price = armor_dictionary[self.armor_key].value
        self.card_selected_key = card_name

    def buy_item(self, hero:Hero) -> None:
        """Buy the selected item from the shop."""
        if self.card_selected_key == Shop_Constants.POTION_CARD_KEY:
            item = potion_dictionary[self.potion_key]
        elif self.card_selected_key == Shop_Constants.WEAPON_CARD_KEY:
            item = weapon_dictionary[self.weapon_key]
        elif self.card_selected_key == Shop_Constants.ARMOR_CARD_KEY:
            item = armor_dictionary[self.armor_key]

        if hero.spend_gold(self.selected_price):
            hero.add_item(item)
            self.new_card(self.card_selected_key)
        else:
            print("Not enough gold to buy the item.")

    def draw(self, surface):
        """Open the shop and display the items."""
        # Draw the shop background
        potion_border = Colors.LIGHT_GREEN if self.card_selected_key == Shop_Constants.POTION_CARD_KEY else Colors.BLACK
        weapon_border = Colors.LIGHT_GREEN if self.card_selected_key == Shop_Constants.WEAPON_CARD_KEY else Colors.BLACK
        armor_border = Colors.LIGHT_GREEN if self.card_selected_key == Shop_Constants.ARMOR_CARD_KEY else Colors.BLACK

        draw_item(potion_dictionary[self.potion_key], self.cards[Shop_Constants.POTION_CARD_KEY], surface, potion_border)
        draw_item(weapon_dictionary[self.weapon_key], self.cards[Shop_Constants.WEAPON_CARD_KEY], surface, weapon_border)
        draw_item(armor_dictionary[self.armor_key],   self.cards[Shop_Constants.ARMOR_CARD_KEY],  surface, armor_border)

class Village:
    
    def __init__(self, name:int, health:int, font):
        """Initialize the village with a name and health."""
        self.name = name
        self.health = health
        self.max_health = health
        self.level = 1
        self.font = font
        self.shop = Shop(self.font)
    
    def take_damage(self, damage:int) -> None:
        """Take damage from the village."""
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def draw(self, surface, x: int, y: int):
        """Draw the village and its health bar."""
        # Draw the village name
        draw_text(self.name, self.font, Colors.BLACK, surface, x, y)

        # Draw the health bar
        health_bar_width = 200
        health_bar_height = 20
        health_bar_x = x
        health_bar_y = y + 30
        draw_health_bar(surface, self.font, health_bar_x, health_bar_y, health_bar_width, health_bar_height, self.health, self.max_health)