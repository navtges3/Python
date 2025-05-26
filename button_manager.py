from typing import Dict, Optional
import pygame
from button import Button, TextButton
from spritesheet import SpriteSheet
from constants import GameState, GameConstants, Colors

class ButtonManager:
    """Manages button creation and organization for different game states."""
    
    def __init__(self, font: pygame.font.Font, button_sheet: pygame.Surface):
        self.font = font
        # Split the 600x250 button sheet into 5 rows of 600x50
        self.button_sheet_gray      = SpriteSheet(button_sheet.subsurface((0, 0, 600, 50)))
        self.button_sheet_red       = SpriteSheet(button_sheet.subsurface((0, 50, 600, 50)))
        self.button_sheet_green     = SpriteSheet(button_sheet.subsurface((0, 100, 600, 50)))
        self.button_sheet_blue      = SpriteSheet(button_sheet.subsurface((0, 150, 600, 50)))
        self.button_sheet_yellow    = SpriteSheet(button_sheet.subsurface((0, 200, 600, 50)))
        self.buttons: Dict[GameState, Dict[str, Button]] = self._initialize_buttons()

    def _initialize_buttons(self) -> Dict[GameState, Dict[str, Button]]:
        """Initialize all game buttons organized by game state."""
        return {
            GameState.WELCOME:      self._create_welcome_buttons(),
            GameState.NEW_GAME:     self._create_new_game_buttons(),
            GameState.MAIN_GAME:    self._create_main_game_buttons(),
            GameState.QUEST:        self._create_quest_buttons(),
            GameState.BATTLE:       self._create_battle_buttons(),
            GameState.SHOP:         self._create_shop_buttons(),
            GameState.PAUSE:        self._create_pause_buttons(),
            GameState.OPTIONS:      self._create_options_buttons(),
        }

    def _create_welcome_buttons(self) -> Dict[str, Button]:
        """Create welcome screen buttons."""
        return {
            'New Game': TextButton(
                self.button_sheet_blue,
                GameConstants.SCREEN_WIDTH // 2 - 100,
                GameConstants.SCREEN_HEIGHT // 2 - 20,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'New Game',
                self.font,
                Colors.BLACK
            ),
            'Load Game': TextButton(
                self.button_sheet_green,
                GameConstants.SCREEN_WIDTH // 2 - 100,
                GameConstants.SCREEN_HEIGHT // 2 + 40,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Load Game',
                self.font,
                Colors.BLACK
            ),
            'Options': TextButton(
                self.button_sheet_yellow,
                GameConstants.SCREEN_WIDTH // 2 - 100,
                GameConstants.SCREEN_HEIGHT // 2 + 100,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Options',
                self.font,
                Colors.BLACK
            ),
            'Exit Game': TextButton(
                self.button_sheet_red,
                GameConstants.SCREEN_WIDTH // 2 - 100,
                GameConstants.SCREEN_HEIGHT // 2 + 160,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Exit Game',
                self.font,
                Colors.BLACK
            )
        }
    
    def _create_new_game_buttons(self) -> Dict[str, Button]:
        return {
            'Back': TextButton(
                self.button_sheet_red,
                20,
                80,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Back',
                self.font
            ),
            'Create Hero': TextButton(
                self.button_sheet_green,
                320,
                80,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Create Hero',
                self.font,
            ),
            'Knight': Button(
                self.button_sheet_yellow,
                20,
                20,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
            ),
            'Assassin': Button(
                self.button_sheet_blue,
                320,
                20,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
            ),
        }
    
    def _create_main_game_buttons(self) -> Dict[str, Button]:
        return {
            'Menu': TextButton(
                self.button_sheet_red,
                0,
                GameConstants.SCREEN_HEIGHT - GameConstants.SCREEN_HEIGHT // 12,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Menu',
                self.font,
            ),
            'Quest': TextButton(
                self.button_sheet_blue,
                GameConstants.SCREEN_WIDTH // 3,
                GameConstants.SCREEN_HEIGHT - GameConstants.SCREEN_HEIGHT // 12,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Quest',
                self.font,
            ),
            'Shop': TextButton(
                self.button_sheet_yellow,
                GameConstants.SCREEN_WIDTH // 3 * 2,
                GameConstants.SCREEN_HEIGHT - GameConstants.SCREEN_HEIGHT // 12,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Shop',
                self.font,
            ),
        }
    
    def _create_quest_buttons(self) -> Dict[str, Button]:
        return {
            'Back': TextButton(
                self.button_sheet_red,
                GameConstants.SCREEN_WIDTH // 3,
                GameConstants.SCREEN_HEIGHT - GameConstants.SCREEN_HEIGHT // 12,
                GameConstants.SCREEN_WIDTH // 3,
                GameConstants.SCREEN_HEIGHT // 12, 1,
                'Back',
                self.font,
            ),
            'Start': TextButton(
                self.button_sheet_green,
                GameConstants.SCREEN_WIDTH // 3 * 2,
                GameConstants.SCREEN_HEIGHT - GameConstants.SCREEN_HEIGHT // 12,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Start Quest',
                self.font,
            ),
            'Available': TextButton(
                self.button_sheet_yellow,
                GameConstants.SCREEN_WIDTH // 3,
                10,
                GameConstants.SCREEN_WIDTH // 3,
                GameConstants.SCREEN_HEIGHT // 12, 1,
                'Available',
                self.font,
            ),
            'Complete': TextButton(
                self.button_sheet_green,
                GameConstants.SCREEN_WIDTH // 3 * 2,
                10,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Complete',
                self.font,
            ),
        }
    
    def _create_battle_buttons(self) -> Dict[str, Button]:
        return
    
    def _create_shop_buttons(self) -> Dict[str, Button]:
        return {
            'Purchase': TextButton(
                self.button_sheet_green,
                GameConstants.SCREEN_WIDTH // 2 + 15,
                GameConstants.SCREEN_HEIGHT // 2 + 20,
                GameConstants.BUTTON_WIDTH,
                GameConstants.BUTTON_HEIGHT,
                1,
                'Purchase',
                self.font,
            ),
            'Leave': TextButton(
                self.button_sheet_red,
                GameConstants.SCREEN_WIDTH // 2 + 15,
                GameConstants.SCREEN_HEIGHT // 2 + 75,
                GameConstants.BUTTON_WIDTH,
                GameConstants.BUTTON_HEIGHT,
                1,
                'Leave',
                self.font,
            ),
        }
    
    def _create_pause_buttons(self) -> Dict[str, Button]:
        popup_x = (GameConstants.SCREEN_WIDTH - GameConstants.POPUP_WIDTH) // 2 + GameConstants.BUTTON_WIDTH // 2
        popup_y = (GameConstants.SCREEN_HEIGHT - GameConstants.POPUP_HEIGHT) // 2 + GameConstants.BUTTON_HEIGHT
        return {
            'Resume': TextButton(
                self.button_sheet_green,
                popup_x ,
                popup_y,
                GameConstants.BUTTON_WIDTH,
                GameConstants.BUTTON_HEIGHT,
                1,
                'Resume',
                self.font,
            ),
            'Options': TextButton(
                self.button_sheet_yellow,
                popup_x,
                popup_y + 70,
                GameConstants.BUTTON_WIDTH,
                GameConstants.BUTTON_HEIGHT,
                1,
                'Options',
                self.font,
            ),
            'Exit': TextButton(
                self.button_sheet_red,
                popup_x,
                popup_y + 140,
                GameConstants.BUTTON_WIDTH,
                GameConstants.BUTTON_HEIGHT,
                1,
                'Exit',
                self.font,
            ),
        }
    
    def _create_options_buttons(self) -> Dict[str, Button]:
        popup_x = (GameConstants.SCREEN_WIDTH - GameConstants.POPUP_WIDTH) // 2 + GameConstants.BUTTON_WIDTH // 2
        popup_y = (GameConstants.SCREEN_HEIGHT - GameConstants.POPUP_HEIGHT) // 2 + GameConstants.BUTTON_HEIGHT
        return {
            'Exit': TextButton(
                self.button_sheet_red,
                popup_x,
                popup_y + 140,
                GameConstants.BUTTON_WIDTH,
                GameConstants.BUTTON_HEIGHT,
                1,
                'Exit',
                self.font,
            ),
        }

    def get_buttons(self, state: GameState) -> Dict[str, Button]:
        """Get all buttons for a specific game state."""
        return self.buttons.get(state, {})

    def get_button(self, state: GameState, button_name: str) -> Optional[Button]:
        """Get a specific button by state and name."""
        return self.buttons.get(state, {}).get(button_name)

    def draw_buttons(self, surface: pygame.Surface, state: GameState) -> None:
        """Draw all buttons for a specific game state."""
        for button in self.buttons[state].values():
            button.draw(surface)

    def handle_click(self, state: GameState, pos: tuple) -> Optional[str]:
        """Handle click events and return clicked button name if any."""
        for button_name, button in self.buttons[state].items():
            if button.rect.collidepoint(pos) and not button.is_locked():
                if button.was_clicked:
                    return button_name
        return None