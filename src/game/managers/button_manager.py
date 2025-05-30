from typing import Dict, Optional
import pygame
from src.game.ui.button import Button, TextButton
from src.game.ui.spritesheet import SpriteSheet
from src.game.core.constants import GameState, GameConstants, Colors
from src.game.ui.scrollable import ScrollableButtons
from src.game.entities.quest import QuestButton, quest_list

class ButtonManager:
    """Manages button creation and organization for different game states."""
    
    def __init__(self, font: pygame.font.Font, button_sheet: pygame.Surface, quest_button_sheet: pygame.Surface):
        self.font = font
        # Split the 800x250 button sheet into 5 rows of 800x50
        self.button_sheet_gray      = SpriteSheet(button_sheet.subsurface((0, 0, 800, 50)))
        self.button_sheet_red       = SpriteSheet(button_sheet.subsurface((0, 50, 800, 50)))
        self.button_sheet_green     = SpriteSheet(button_sheet.subsurface((0, 100, 800, 50)))
        self.button_sheet_blue      = SpriteSheet(button_sheet.subsurface((0, 150, 800, 50)))
        self.button_sheet_yellow    = SpriteSheet(button_sheet.subsurface((0, 200, 800, 50)))
        self.buttons: Dict[GameState, Dict[str, Button]] = self._initialize_buttons()

        self.quest_button_sheet = SpriteSheet(quest_button_sheet)
        
        # Initialize quest containers
        self.available_quests = ScrollableButtons(
            10, 70,  # x, y
            GameConstants.SCREEN_WIDTH - 20,  # width
            GameConstants.SCREEN_HEIGHT - 200,  # height
            100,  # button_height
            20  # button_spacing
        )
        
        self.completed_quests = ScrollableButtons(
            10, 70,  # x, y
            GameConstants.SCREEN_WIDTH - 20,  # width
            GameConstants.SCREEN_HEIGHT - 200,  # height
            100,  # button_height
            20  # button_spacing
        )

        self.failed_quests = ScrollableButtons(
            10, 70,  # x, y
            GameConstants.SCREEN_WIDTH - 20,  # width
            GameConstants.SCREEN_HEIGHT - 200,  # height
            100,  # button_height
            20  # button_spacing
        )
        
        # Initialize available quests
        for quest in quest_list:
            quest_button = QuestButton(
                self.quest_button_sheet,  # Use yellow button sheet for quests
                0,  # x position will be set by ScrollableButtons
                0,  # y position will be set by ScrollableButtons
                700,  # width
                100,  # height
                1,  # scale
                quest  # quest object
            )
            self.available_quests.add_button(quest_button)

        self.hero_ability_buttons = ScrollableButtons(
            GameConstants.BUTTON_WIDTH + 40,
            GameConstants.SCREEN_HEIGHT // 2,
            GameConstants.BUTTON_WIDTH + 15,
            GameConstants.SCREEN_HEIGHT // 2,
            GameConstants.BUTTON_HEIGHT,
        )

    def _initialize_buttons(self) -> Dict[GameState, Dict[str, Button]]:
        """Initialize all game buttons organized by game state."""
        return {
            GameState.HOME:         self._create_home_buttons(),
            GameState.NEW_GAME:     self._create_new_game_buttons(),
            GameState.VILLAGE:      self._create_main_game_buttons(),
            GameState.QUEST:        self._create_quest_buttons(),
            GameState.BATTLE:       self._create_battle_buttons(),
            GameState.SHOP:         self._create_shop_buttons(),
            GameState.PAUSE:        self._create_pause_buttons(),
            GameState.OPTIONS:      self._create_options_buttons(),
        }

    def _create_home_buttons(self) -> Dict[str, Button]:
        """Create home screen buttons."""
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
        # Calculate positions relative to screen height
        action_row_y = GameConstants.SCREEN_HEIGHT // 2 + 100  # Action buttons below middle
        
        left_col_x = GameConstants.SCREEN_WIDTH // 4 - GameConstants.BUTTON_WIDTH // 2  # Left quarter of screen
        right_col_x = (GameConstants.SCREEN_WIDTH * 3) // 4 - GameConstants.BUTTON_WIDTH // 2  # Right quarter of screen
        
        # Calculate positions for character buttons to match image positions
        image_y = GameConstants.SCREEN_HEIGHT // 4  # Quarter down the screen
        character_size = (200, 200)  # Same size as character images
        
        buttons = {
            'Back': TextButton(
                self.button_sheet_red,
                left_col_x,
                action_row_y,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Back',
                self.font
            ),
            'Create Hero': TextButton(
                self.button_sheet_green,
                right_col_x,
                action_row_y,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Create Hero',
                self.font,
            ),
            'Knight': Button(
                self.button_sheet_yellow,
                GameConstants.SCREEN_WIDTH // 4 - character_size[0] // 2,  # Match image x position
                image_y,  # Match image y position
                character_size[0],  # Match image width
                character_size[1],  # Match image height
                1,
            ),
            'Assassin': Button(
                self.button_sheet_blue,
                (GameConstants.SCREEN_WIDTH * 3) // 4 - character_size[0] // 2,  # Match image x position
                image_y,  # Match image y position
                character_size[0],  # Match image width
                character_size[1],  # Match image height
                1,
            ),
        }
        
        # Hide the character selection buttons (they'll be invisible but still clickable)
        buttons['Knight'].hide()
        buttons['Assassin'].hide()
        
        return buttons
    
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
        """Create quest screen buttons.
        
        Returns:
            Dictionary mapping button names to Button objects
        """
        print("Creating quest screen buttons") # DEBUG
        return {
            'Back': TextButton(
                self.button_sheet_red,
                0,
                GameConstants.SCREEN_HEIGHT - GameConstants.SCREEN_HEIGHT // 12,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Back',
                self.font,
            ),
            'Start': TextButton(
                self.button_sheet_green,
                GameConstants.SCREEN_WIDTH - GameConstants.BUTTON_WIDTH,
                GameConstants.SCREEN_HEIGHT - GameConstants.SCREEN_HEIGHT // 12,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Start',
                self.font,
            ),
            'Available': TextButton(
                self.button_sheet_blue,
                10,
                10,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Available',
                self.font,
            ),
            'Complete': TextButton(
                self.button_sheet_yellow,
                GameConstants.BUTTON_WIDTH + 20,
                10,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Complete',
                self.font,
            ),
            'Failed': TextButton(
                self.button_sheet_red,
                GameConstants.BUTTON_WIDTH * 2 + 30,
                10,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Failed',
                self.font,
            ),
        }
    
    def _create_battle_buttons(self) -> Dict[str, Button]:
        """Create battle screen buttons.
        
        Returns:
            Dictionary mapping button names to Button objects
        """
        # Calculate button positions
        button_x = 20  # Left margin for first column
        button_y_start = GameConstants.SCREEN_HEIGHT // 2  # Start at middle of screen
        button_spacing = GameConstants.BUTTON_HEIGHT + 10  # Vertical spacing between buttons
        
        # Calculate second column position for potion buttons
        potion_x = button_x + GameConstants.BUTTON_WIDTH + 20  # Right of first column with margin
        
        # Create buttons dictionary
        buttons: Dict[str, Button] = {
            'Ability': TextButton(
                self.button_sheet_red,
                button_x,
                button_y_start,  # First row
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Ability',
                self.font,
            ),
            'Potion': TextButton(
                self.button_sheet_blue,
                button_x,
                button_y_start + button_spacing,  # Second row
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Potions',
                self.font,
            ),
            'Rest': TextButton(
                self.button_sheet_green,
                button_x,
                button_y_start + button_spacing * 2,  # Third row
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Rest',
                self.font,
            ),
            'Flee': TextButton(
                self.button_sheet_yellow,
                button_x,
                button_y_start + button_spacing * 3,  # Fourth row
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Flee',
                self.font,
            ),
            'Continue': TextButton(
                self.button_sheet_green,
                button_x,
                button_y_start + button_spacing * 2,  # Same row as Potion
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Continue',
                self.font,
            ),
            'Retreat': TextButton(
                self.button_sheet_red,
                button_x,
                button_y_start + button_spacing * 3,  # Same row as Flee
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Retreat',
                self.font,
            ),
            'Health Potion': TextButton(
                self.button_sheet_green,
                potion_x,
                button_y_start,  # First row
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Health Potion',
                self.font,
            ),
            'Damage Potion': TextButton(
                self.button_sheet_red,
                potion_x,
                button_y_start + button_spacing,  # Second row
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Damage Potion',
                self.font,
            ),
            'Block Potion': TextButton(
                self.button_sheet_blue,
                potion_x,
                button_y_start + button_spacing * 2,  # Third row
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Block Potion',
                self.font,
            ),
        }

        # Hide victory buttons and potion buttons initially
        buttons['Continue'].hide()
        buttons['Retreat'].hide()
        buttons['Health Potion'].hide()
        buttons['Damage Potion'].hide()
        buttons['Block Potion'].hide()
        
        return buttons
    
    def _create_shop_buttons(self) -> Dict[str, Button]:
        """Create shop screen buttons.
        
        Returns:
            Dictionary mapping button names to Button objects
        """
        return {
            'Leave': TextButton(
                self.button_sheet_red,
                0,
                GameConstants.SCREEN_HEIGHT - GameConstants.SCREEN_HEIGHT // 12,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Leave',
                self.font,
            ),
        }
    
    def _create_pause_buttons(self) -> Dict[str, Button]:
        """Create pause menu buttons.
        
        Returns:
            Dictionary mapping button names to Button objects
        """
        # Calculate button positions
        button_y = (GameConstants.SCREEN_HEIGHT - GameConstants.POPUP_HEIGHT) // 2 + 50
        button_spacing = 50
        
        return {
            'Resume': TextButton(
                self.button_sheet_green,
                (GameConstants.SCREEN_WIDTH - GameConstants.BUTTON_WIDTH) // 2,
                button_y,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Resume',
                self.font,
            ),
            'Options': TextButton(
                self.button_sheet_blue,
                (GameConstants.SCREEN_WIDTH - GameConstants.BUTTON_WIDTH) // 2,
                button_y + button_spacing,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Options',
                self.font,
            ),
            'Exit': TextButton(
                self.button_sheet_red,
                (GameConstants.SCREEN_WIDTH - GameConstants.BUTTON_WIDTH) // 2,
                button_y + button_spacing * 2,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Exit',
                self.font,
            ),
        }
    
    def _create_options_buttons(self) -> Dict[str, Button]:
        """Create options menu buttons.
        
        Returns:
            Dictionary mapping button names to Button objects
        """
        return {
            'Back': TextButton(
                self.button_sheet_red,
                (GameConstants.SCREEN_WIDTH - GameConstants.BUTTON_WIDTH) // 2,
                (GameConstants.SCREEN_HEIGHT + GameConstants.POPUP_HEIGHT) // 2 - 60,
                GameConstants.BUTTON_WIDTH, 
                GameConstants.BUTTON_HEIGHT,
                1,
                'Back',
                self.font,
            ),
        }

    def get_buttons(self, state: GameState) -> Dict[str, Button]:
        """Get all buttons for a given game state.
        
        Args:
            state: The game state to get buttons for
            
        Returns:
            Dictionary mapping button names to Button objects
        """
        return self.buttons[state]

    def get_button(self, state: GameState, button_name: str) -> Optional[Button]:
        """Get a specific button by name from a game state.
        
        Args:
            state: The game state containing the button
            button_name: The name of the button to get
            
        Returns:
            The requested Button object, or None if not found
        """
        return self.buttons[state].get(button_name)

    def draw_buttons(self, surface: pygame.Surface, state: GameState) -> None:
        """Draw all buttons for a given game state.
        
        Args:
            surface: The surface to draw the buttons on
            state: The game state whose buttons to draw
        """
        for button in self.buttons[state].values():
            button.draw(surface)

    def handle_click(self, state: GameState, pos: tuple[int, int]) -> Optional[str]:
        """Handle a click event for buttons in a game state.
        
        Args:
            state: The game state whose buttons to check
            pos: The (x, y) position of the click
            
        Returns:
            The name of the clicked button, or None if no button was clicked
        """
        for name, button in self.buttons[state].items():
            if not button.is_locked() and button.rect.collidepoint(pos):
                print(f"Button clicked: {name}")  # DEBUG
                return name
        return None

    def show_button(self, state: GameState, button_name: str) -> None:
        """Show a specific button.
        
        Args:
            state: The game state containing the button
            button_name: The name of the button to show
        """
        if button := self.buttons[state].get(button_name):
            button.show()

    def hide_button(self, state: GameState, button_name: str) -> None:
        """Hide a specific button.
        
        Args:
            state: The game state containing the button
            button_name: The name of the button to hide
        """
        if button := self.buttons[state].get(button_name):
            button.hide()

    def show_all_buttons(self, state: GameState) -> None:
        """Show all buttons in a game state.
        
        Args:
            state: The game state whose buttons to show
        """
        for button in self.buttons[state].values():
            button.show()

    def hide_all_buttons(self, state: GameState) -> None:
        """Hide all buttons in a game state.
        
        Args:
            state: The game state whose buttons to hide
        """
        for button in self.buttons[state].values():
            button.hide()

    def move_completed_quest(self, quest_button: QuestButton) -> None:
        """Move a quest button from available to completed quests.
        
        Args:
            quest_button: The quest button to move
        """
        # Remove from available quests
        self.available_quests.remove_button(quest_button)
        # Add to completed quests
        self.completed_quests.add_button(quest_button)

    def move_failed_quest(self, quest_button: QuestButton) -> None:
        """Move a quest button from available to failed quests and apply penalty.
        
        Args:
            quest_button: The quest button to move
        """
        # Remove from available quests
        self.available_quests.remove_button(quest_button)
        # Mark the quest as failed
        quest_button.mark_as_failed()
        # Add to failed quests
        self.failed_quests.add_button(quest_button)
        
        # Apply the quest penalty
        penalty_target, penalty_value = quest_button.quest.penalty
        if penalty_target == "village":
            from src.game.core.game import Game  # Import here to avoid circular import
            if hasattr(Game, 'instance') and Game.instance and Game.instance.village:
                Game.instance.village.health += penalty_value  # Penalty value is negative
                Game.instance.battle_log.append(f"Village suffers {abs(penalty_value)} damage from quest failure!")

    def add_hero_ability_button(self, button: Button) -> None:
        """Add a hero ability button to the scrollable area.
        
        Args:
            button: The Button instance to add
        """
        self.hero_ability_buttons.append(button)

    def clear_hero_ability_buttons(self) -> None:
        """Clear all hero ability buttons from the scrollable area.
        """
        self.hero_ability_buttons.clear()