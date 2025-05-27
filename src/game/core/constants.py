from enum import Enum
from typing import Tuple, Final

class GameState(Enum):
    """Game states for managing different screens and transitions."""
    HOME = 1
    NEW_GAME = 2
    MAIN_GAME = 3
    QUEST = 4
    BATTLE = 5
    SHOP = 6
    VICTORY = 7
    DEFEAT = 8
    PAUSE = 9
    OPTIONS = 10
    EXIT = 11

class BattleActions(Enum):
    """Available actions during battle."""
    ATTACK = 0
    DEFEND = 1
    USE_POTION = 2

class Colors:
    """Color constants used throughout the game."""
    WHITE: Final[Tuple[int, int, int]] = (255, 255, 255)
    BLACK: Final[Tuple[int, int, int]] = (0, 0, 0)
    GRAY: Final[Tuple[int, int, int]] = (200, 200, 200)
    BLUE: Final[Tuple[int, int, int]] = (0, 0, 255)
    RED: Final[Tuple[int, int, int]] = (255, 0, 0)
    GREEN: Final[Tuple[int, int, int]] = (0, 255, 0)
    YELLOW: Final[Tuple[int, int, int]] = (255, 255, 0)
    LIGHT_GRAY: Final[Tuple[int, int, int]] = (211, 211, 211)
    LIGHT_BLUE: Final[Tuple[int, int, int]] = (173, 216, 230)
    LIGHT_RED: Final[Tuple[int, int, int]] = (255, 182, 193)
    LIGHT_YELLOW: Final[Tuple[int, int, int]] = (255, 255, 224)
    LIGHT_GREEN: Final[Tuple[int, int, int]] = (144, 238, 144)
    GOLD: Final[Tuple[int, int, int]] = (255, 215, 0)

class ShopConstants:
    """Constants for shop items and categories."""
    POTION_CARD_KEY: Final[str] = "Potion Card"
    WEAPON_CARD_KEY: Final[str] = "Weapon Card"
    ARMOR_CARD_KEY: Final[str] = "Armor Card"

class GameConstants:
    """Game-wide constants for screen dimensions and UI elements."""
    SCREEN_WIDTH: Final[int] = 800
    SCREEN_HEIGHT: Final[int] = 600
    POPUP_WIDTH: Final[int] = 400
    POPUP_HEIGHT: Final[int] = 300

    FPS: Final[int] = 60

    BUTTON_WIDTH: Final[int] = 200
    BUTTON_HEIGHT: Final[int] = 50

    BUTTON_IMAGE_PATH: Final[str] = "images\\buttons\\button.png"
    HOVER_IMAGE_PATH: Final[str] = "images\\buttons\\button_hover.png"

    # New Game Constants
    NEW_GAME_SPACING: Final[int] = SCREEN_HEIGHT // 30

    NEW_GAME_BUTTON_WIDTH: Final[int] = SCREEN_WIDTH // 8 * 3
    NEW_GAME_BUTTON_HEIGHT: Final[int] = SCREEN_HEIGHT // 12
    NEW_GAME_BUTTON_X: Final[int] = SCREEN_WIDTH // 2 - NEW_GAME_BUTTON_WIDTH // 2
    NEW_GAME_BUTTON_Y: Final[int] = SCREEN_HEIGHT // 2 - NEW_GAME_BUTTON_HEIGHT // 2
    NEW_GAME_BUTTON_INCREMENT: Final[int] = NEW_GAME_BUTTON_HEIGHT + NEW_GAME_SPACING

    # Battle Screen Constants
    BATTLE_SCREEN_SPACING: Final[int] = SCREEN_HEIGHT // 30

    BATTLE_SCREEN_BUTTON_BORDER_X: Final[int] = 0
    BATTLE_SCREEN_BUTTON_BORDER_Y: Final[int] = SCREEN_HEIGHT // 2
    BATTLE_SCREEN_BUTTON_BORDER_HEIGHT: Final[int] = SCREEN_HEIGHT // 2
    BATTLE_SCREEN_BUTTON_BORDER_WIDTH: Final[int] = SCREEN_WIDTH // 8 * 3

    BATTLE_SCREEN_BUTTON_X: Final[int] = BATTLE_SCREEN_BUTTON_BORDER_X + BATTLE_SCREEN_SPACING
    BATTLE_SCREEN_BUTTON_Y: Final[int] = BATTLE_SCREEN_BUTTON_BORDER_Y + BATTLE_SCREEN_SPACING
    BATTLE_SCREEN_BUTTON_HEIGHT: Final[int] = BATTLE_SCREEN_BUTTON_BORDER_HEIGHT // 6
    BATTLE_SCREEN_BUTTON_WIDTH: Final[int] = BATTLE_SCREEN_BUTTON_BORDER_WIDTH - BATTLE_SCREEN_SPACING * 2
    BATTLE_SCREEN_BUTTON_INCREMENT: Final[int] = BATTLE_SCREEN_BUTTON_HEIGHT + BATTLE_SCREEN_SPACING

    BATTLE_SCREEN_LOG_BORDER_X: Final[int] = BATTLE_SCREEN_BUTTON_BORDER_WIDTH
    BATTLE_SCREEN_LOG_BORDER_Y: Final[int] = BATTLE_SCREEN_BUTTON_BORDER_Y
    BATTLE_SCREEN_LOG_BORDER_WIDTH: Final[int] = SCREEN_WIDTH - BATTLE_SCREEN_BUTTON_BORDER_WIDTH
    BATTLE_SCREEN_LOG_BORDER_HEIGHT: Final[int] = BATTLE_SCREEN_BUTTON_BORDER_HEIGHT

    BATTLE_SCREEN_LOG_X: Final[int] = BATTLE_SCREEN_LOG_BORDER_X + BATTLE_SCREEN_SPACING
    BATTLE_SCREEN_LOG_Y: Final[int] = BATTLE_SCREEN_LOG_BORDER_Y + BATTLE_SCREEN_SPACING
    BATTLE_SCREEN_LOG_WIDTH: Final[int] = BATTLE_SCREEN_LOG_BORDER_WIDTH - BATTLE_SCREEN_SPACING * 2
    BATTLE_SCREEN_LOG_HEIGHT: Final[int] = BATTLE_SCREEN_LOG_BORDER_HEIGHT - BATTLE_SCREEN_SPACING * 2