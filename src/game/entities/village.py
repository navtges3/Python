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
        self.card_selected_key: Optional[str] = None
        self.selected_price: int = 0
        self.font: pygame.font.Font = font

    def new_card(self, card_name: str) -> None:
        """
        Change the item in the shop.

        Args:
            card_name: Name of the item type to change
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
        Select an item in the shop.

        Args:
            card_name: Name of the item type to select
        """
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

    def draw(self, surface: pygame.Surface, hero: Hero) -> None:
        """
        Draw the shop and its items.

        Args:
            surface: Pygame surface to draw on
            hero: The hero who is shopping
        """
        # Draw shop title
        draw_text_centered("Shop", self.font, Colors.BLACK, surface, 
                          GameConstants.SCREEN_WIDTH // 2, 20)

        # Draw hero's gold
        draw_text_centered(f"Gold: {hero.gold}", self.font, Colors.GOLD, surface,
                          GameConstants.SCREEN_WIDTH // 2, 50)

        # Calculate positions for item sections
        section_width = GameConstants.SCREEN_WIDTH // 3
        section_height = 150
        y_start = 100
        padding = 20

        # Draw Potions Section
        potion_x = padding
        self._draw_item_section(surface, potion_x, y_start, section_width - padding * 2, section_height,
                                "Potions", potion_dictionary[self.potion_key],
                                ShopConstants.POTION_CARD_KEY, hero)

        # Draw Weapons Section
        weapon_x = section_width + padding
        self._draw_item_section(surface, weapon_x, y_start, section_width - padding * 2, section_height,
                                "Weapons", weapon_dictionary[self.weapon_key],
                                ShopConstants.WEAPON_CARD_KEY, hero)

        # Draw Armor Section
        armor_x = section_width * 2 + padding
        self._draw_item_section(surface, armor_x, y_start, section_width - padding * 2, section_height,
                                "Armor", armor_dictionary[self.armor_key],
                                ShopConstants.ARMOR_CARD_KEY, hero)

        # Draw Buy Button if item is selected
        if self.card_selected_key is not None:
            buy_button_rect = pygame.Rect(
                GameConstants.SCREEN_WIDTH // 2 - 100,
                y_start + section_height + padding,
                200,
                40
            )
            can_buy = self.can_buy_selected(hero)
            button_color = Colors.GREEN if can_buy else Colors.GRAY
            pygame.draw.rect(surface, button_color, buy_button_rect, border_radius=5)
            draw_text_centered("Buy", self.font, Colors.WHITE, surface,
                                buy_button_rect.centerx, buy_button_rect.centery)

    def _draw_item_section(self, surface: pygame.Surface, x: int, y: int, width: int, height: int,
                            title: str, item: Union[Item, Weapon, Armor], card_key: str, hero: Hero) -> None:
        """
        Draw a section for an item type in the shop.

        Args:
            surface: Pygame surface to draw on
            x: X coordinate of the section
            y: Y coordinate of the section
            width: Width of the section
            height: Height of the section
            title: Title of the section
            item: Item to display
            card_key: Key identifying this item type
            hero: The hero who is shopping
        """
        # Draw section background
        rect = pygame.Rect(x, y, width, height)
        is_selected = self.card_selected_key == card_key
        border_color = Colors.LIGHT_GREEN if is_selected else Colors.BLACK
        pygame.draw.rect(surface, Colors.WHITE, rect)
        pygame.draw.rect(surface, border_color, rect, 2, border_radius=5)

        # Draw section title
        draw_text_centered(title, self.font, Colors.BLACK, surface,
                            rect.centerx, rect.y + 20)

        # Draw item name
        draw_text_centered(item.name, self.font, Colors.BLACK, surface,
                            rect.centerx, rect.y + 50)

        # Draw item price
        draw_text_centered(f"Price: {item.value} gold", self.font,
                            Colors.GOLD if hero.gold >= item.value else Colors.RED,
                            surface, rect.centerx, rect.y + 80)

        # Draw item description (wrapped)
        draw_wrapped_text(item.description, self.font, Colors.BLACK, surface,
                            rect.x + 10, rect.y + 110, width - 20)

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