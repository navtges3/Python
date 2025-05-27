from src.game.ui.ui_helpers import *
from src.game.core.constants import *
from src.game.entities.items import *
from src.game.entities.hero import *
import random
import pygame
from typing import Dict, Optional, Union

# Type aliases
CardDict = Dict[str, Button]
ItemDict = Dict[str, Union[Item, Weapon, Armor]]

class Shop:
    """A class representing a shop where heroes can buy items."""

    def __init__(self, font: pygame.font.Font) -> None:
        """
        Initialize the shop with random items.

        Args:
            font: Font to use for text rendering
        """
        self.potion_key: str = random.choice(list(potion_dictionary.keys()))
        self.weapon_key: str = random.choice(list(weapon_dictionary.keys()))
        self.armor_key: str = random.choice(list(armor_dictionary.keys()))
        self.card_selected_key: Optional[str] = ShopConstants.POTION_CARD_KEY
        self.selected_price: int = potion_dictionary[self.potion_key].value
        self.cards: CardDict = {
            ShopConstants.POTION_CARD_KEY: Button(
                ShopConstants.POTION_CARD_KEY, 
                (GameConstants.SCREEN_WIDTH // 8, 25), 
                (GameConstants.SCREEN_WIDTH // 16 * 3, GameConstants.SCREEN_HEIGHT // 3), 
                font, Colors.BLACK
            ),
            ShopConstants.WEAPON_CARD_KEY: Button(
                ShopConstants.WEAPON_CARD_KEY, 
                (GameConstants.SCREEN_WIDTH // 32 * 13, 25), 
                (GameConstants.SCREEN_WIDTH // 16 * 3, GameConstants.SCREEN_HEIGHT // 3), 
                font, Colors.BLACK, Colors.RED
            ),
            ShopConstants.ARMOR_CARD_KEY: Button(
                ShopConstants.ARMOR_CARD_KEY, 
                (GameConstants.SCREEN_WIDTH // 16 * 11, 25), 
                (GameConstants.SCREEN_WIDTH // 16 * 3, GameConstants.SCREEN_HEIGHT // 3), 
                font, Colors.BLACK, Colors.BLUE
            ),
        }

    def new_card(self, card_name: str) -> None:
        """
        Change the card in the shop.

        Args:
            card_name: Name of the card type to change
        """
        if card_name == ShopConstants.POTION_CARD_KEY:
            self.potion_key = random.choice(list(potion_dictionary.keys()))
            self.selected_price = potion_dictionary[self.potion_key].value
        elif card_name == ShopConstants.WEAPON_CARD_KEY:
            self.weapon_key = random.choice(list(weapon_dictionary.keys()))
            self.selected_price = weapon_dictionary[self.weapon_key].value
        elif card_name == ShopConstants.ARMOR_CARD_KEY:
            self.armor_key = random.choice(list(armor_dictionary.keys()))
            self.selected_price = armor_dictionary[self.armor_key].value
        self.card_selected_key = card_name

    def card_selected(self, card_name: str) -> None:
        """
        Select a card in the shop.

        Args:
            card_name: Name of the card to select
        """
        print(f"Selected card: {card_name}")
        if card_name == ShopConstants.POTION_CARD_KEY:
            self.selected_price = potion_dictionary[self.potion_key].value
        elif card_name == ShopConstants.WEAPON_CARD_KEY:
            self.selected_price = weapon_dictionary[self.weapon_key].value
        elif card_name == ShopConstants.ARMOR_CARD_KEY:
            self.selected_price = armor_dictionary[self.armor_key].value
        self.card_selected_key = card_name

    def can_buy_selected(self, hero: Hero) -> bool:
        """
        Check if the hero can afford the selected item.

        Args:
            hero: The hero attempting to buy

        Returns:
            True if the hero has enough gold, False otherwise
        """
        if self.card_selected_key is None:
            return False
        else:
            if self.card_selected_key == ShopConstants.POTION_CARD_KEY:
                item = potion_dictionary[self.potion_key]
            elif self.card_selected_key == ShopConstants.WEAPON_CARD_KEY:
                item = weapon_dictionary[self.weapon_key]
            elif self.card_selected_key == ShopConstants.ARMOR_CARD_KEY:
                item = armor_dictionary[self.armor_key]
            return hero.gold >= item.value

    def buy_item(self, hero: Hero) -> None:
        """
        Buy the selected item from the shop.

        Args:
            hero: The hero making the purchase
        """
        if self.card_selected_key == ShopConstants.POTION_CARD_KEY:
            item = potion_dictionary[self.potion_key]
        elif self.card_selected_key == ShopConstants.WEAPON_CARD_KEY:
            item = weapon_dictionary[self.weapon_key]
        elif self.card_selected_key == ShopConstants.ARMOR_CARD_KEY:
            item = armor_dictionary[self.armor_key]

        if hero.spend_gold(self.selected_price):
            hero.add_item(item)
            self.new_card(self.card_selected_key)
        else:
            print("Not enough gold to buy the item.")

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the shop and its items.

        Args:
            surface: Pygame surface to draw on
        """
        # Draw the shop background
        potion_border = Colors.LIGHT_GREEN if self.card_selected_key == ShopConstants.POTION_CARD_KEY else Colors.BLACK
        weapon_border = Colors.LIGHT_GREEN if self.card_selected_key == ShopConstants.WEAPON_CARD_KEY else Colors.BLACK
        armor_border = Colors.LIGHT_GREEN if self.card_selected_key == ShopConstants.ARMOR_CARD_KEY else Colors.BLACK

        draw_item(potion_dictionary[self.potion_key], self.cards[ShopConstants.POTION_CARD_KEY], surface, potion_border)
        draw_item(weapon_dictionary[self.weapon_key], self.cards[ShopConstants.WEAPON_CARD_KEY], surface, weapon_border)
        draw_item(armor_dictionary[self.armor_key], self.cards[ShopConstants.ARMOR_CARD_KEY], surface, armor_border)

class Village:
    """A class representing a village that can be damaged and has a shop."""
    
    def __init__(self, name: str, health: int, font: pygame.font.Font) -> None:
        """
        Initialize the village with a name and health.

        Args:
            name: Name of the village
            health: Starting health of the village
            font: Font to use for text rendering
        """
        self.name: str = name
        self.health: int = health
        self.max_health: int = health
        self.level: int = 1
        self.font: pygame.font.Font = font
        self.shop: Shop = Shop(self.font)
    
    def take_damage(self, damage: int) -> None:
        """
        Take damage and reduce village health.

        Args:
            damage: Amount of damage to take
        """
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def draw(self, surface: pygame.Surface, x: int, y: int) -> None:
        """
        Draw the village and its health bar.

        Args:
            surface: Pygame surface to draw on
            x: X coordinate to draw at
            y: Y coordinate to draw at
        """
        # Draw the village name
        draw_text(self.name, self.font, Colors.BLACK, surface, x, y)

        # Draw the health bar
        health_bar_width = 200
        health_bar_height = 20
        health_bar_x = x
        health_bar_y = y + 30
        draw_health_bar(surface, self.font, health_bar_x, health_bar_y, 
                        health_bar_width, health_bar_height, 
                        self.health, self.max_health)