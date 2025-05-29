from src.game.managers.battle_manager import BattleManager, TurnState, BattleState
from src.game.managers.screen_manager import ScreenManager
from src.game.managers.button_manager import ButtonManager
from src.game.managers.event_manager import EventManager
from src.game.entities.hero import Hero, Knight, Assassin
from src.game.entities.monster import Monster
from src.game.entities.items import *
from src.game.entities.village import Village
from src.game.core.constants import GameState, GameConstants, Colors
from src.game.entities.quest import Quest, QuestButton, quest_list
from src.game.utils.fileIO import save_file_exists, save_game, load_game, resource_path
from src.game.ui.button import Button
from src.game.ui.textbox import TextBox
from src.game.ui.tooltip import Tooltip
from src.game.ui.ui_helpers import *
import pygame
from typing import Dict, List, Optional, Any, Union, Tuple

class Game:
    """Class to manage different game screens and game state."""
    
    pygame.init()
    font: pygame.font.Font = pygame.font.Font(None, 24)
    key_actions: Dict[int, str] = {
        pygame.K_ESCAPE: "escape",
        pygame.K_BACKSPACE: "backspace",
        pygame.K_RETURN: "enter",
        pygame.K_DELETE: "delete",
        pygame.K_TAB: "tab",
    }
    instance = None  # Class variable to store the current game instance

    def __init__(self) -> None:
        """Initialize the game."""
        Game.instance = self  # Store instance for access from other classes
        self.game_state: GameState = GameState.HOME
        self.battle_log: List[str] = []
        self.hero: Optional[Hero] = None
        self.current_quest: Optional[Quest] = None
        self.running: bool = False
        self.popup_running: bool = False
        self.battle_manager: Optional[BattleManager] = None
        self.event_manager: EventManager = EventManager()
        self.village: Village = Village("Heroville", 100, self.font)  # Initialize village with 100 health
        
        # Initialize the mixer for music
        pygame.mixer.init()
        # Load and play background music
        pygame.mixer.music.load(resource_path('music\\background_music.mp3'))
        pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # Play music in a loop

        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.screen: pygame.Surface = pygame.display.set_mode((GameConstants.SCREEN_WIDTH, GameConstants.SCREEN_HEIGHT))
        pygame.display.set_caption('Village Defense')
        pygame.display.set_icon(pygame.image.load(resource_path('icon.ico')))

        self.screen_manager: ScreenManager = ScreenManager(self.screen, self.font)
        # Load button sprite sheet
        button_sheet: pygame.Surface = pygame.image.load(resource_path('images\\buttons\\button_sheet_0.png')).convert_alpha()
        quest_button_sheet: pygame.Surface = pygame.image.load(resource_path('images\\buttons\\quest_sheet.png')).convert_alpha()
        self.button_manager: ButtonManager = ButtonManager(self.font, button_sheet, quest_button_sheet)
        
        # Create text box above the middle of the screen
        text_box_width: int = 180  # Original 200 - 20 (10px on each side)
        text_box_y: int = GameConstants.SCREEN_HEIGHT // 2 - 100  # 100px above the middle
        self.text_box: TextBox = TextBox(
            rect=pygame.Rect(
                (GameConstants.SCREEN_WIDTH - text_box_width) // 2,  # Centered horizontally
                text_box_y,
                text_box_width,  # Width
                30   # Height
            ),
            font=self.font,
            placeholder="Enter Hero Name",
        )

    def update(self) -> None:
        """Update the game display."""
        self.clock.tick(GameConstants.FPS)
        pygame.display.update()

    def quit(self) -> None:
        """Quit the game."""
        Game.instance = None  # Clear the instance when quitting
        pygame.quit()

    def save_game(self) -> None:
        """Save the player's progress."""
        save_data: Dict[str, Any] = {}
        if self.hero is not None:
            save_data.update({"hero": self.hero.to_dict()})  # Save hero data
        if self.battle_manager and self.battle_manager.monster is not None:
            save_data.update({"monster": self.battle_manager.monster.to_dict()})
        save_data.update({
            "game_volume": pygame.mixer.music.get_volume(),
        })

        # Save quest lists
        available_quests: List[Dict[str, Any]] = []
        completed_quests: List[Dict[str, Any]] = []
        failed_quests: List[Dict[str, Any]] = []
        
        # Save available quests
        for button in self.button_manager.available_quests.buttons:
            quest_data = {
                "name": button.quest.name,
                "monsters_slain": button.quest.monsters_slain
            }
            available_quests.append(quest_data)
            
        # Save completed quests
        for button in self.button_manager.completed_quests.buttons:
            quest_data = {
                "name": button.quest.name,
                "monsters_slain": button.quest.monsters_slain
            }
            completed_quests.append(quest_data)

        # Save failed quests
        for button in self.button_manager.failed_quests.buttons:
            quest_data = {
                "name": button.quest.name,
                "monsters_slain": button.quest.monsters_slain
            }
            failed_quests.append(quest_data)

        save_data.update({
            "available_quests": available_quests,
            "completed_quests": completed_quests,
            "failed_quests": failed_quests
        })

        save_game(save_data)

    def load_game(self) -> None:
        """Load the player's progress from the save file."""
        save_data = load_game()
        if save_data is not None:
            # Load hero data
            if "hero" in save_data:
                self.hero = Hero(pygame.image.load(resource_path(f"images/{save_data['hero']['class_name'].lower()}.png")).convert())
                self.hero.from_dict(save_data["hero"])
                self.hero.image = pygame.transform.scale(self.hero.image, (100, 100))
            else:
                print("No hero data found in save file.")
                return
            
            # Initialize battle manager
            self.battle_manager = BattleManager(self.hero, self.battle_log)
            
            if "monster" in save_data:
                self.battle_manager.monster = Monster(save_data["monster"])

            pygame.mixer.music.set_volume(save_data.get("game_volume", 0.5))
            
            # Clear existing quest lists
            self.button_manager.available_quests.clear_buttons()
            self.button_manager.completed_quests.clear_buttons()
            
            # Load available quests
            if "available_quests" in save_data:
                for quest_data in save_data["available_quests"]:
                    # Find the quest in quest_list by name
                    for quest in quest_list:
                        if quest.name == quest_data["name"]:
                            # Create a new quest instance to avoid modifying the original
                            new_quest = Quest(
                                quest.name,
                                quest.description,
                                quest.monster_list.copy(),
                                quest.reward,
                                quest.penalty
                            )
                            # Update monsters slain
                            new_quest.monsters_slain = quest_data["monsters_slain"]
                            # Create new quest button
                            quest_button = QuestButton(
                                self.button_manager.quest_button_sheet,
                                0,  # x position will be set by ScrollableButtons
                                0,  # y position will be set by ScrollableButtons
                                700,  # width
                                100,  # height
                                1,  # scale
                                new_quest  # quest object
                            )
                            self.button_manager.available_quests.add_button(quest_button)
                            break
            
            # Load completed quests
            if "completed_quests" in save_data:
                for quest_data in save_data["completed_quests"]:
                    # Find the quest in quest_list by name
                    for quest in quest_list:
                        if quest.name == quest_data["name"]:
                            # Create a new quest instance to avoid modifying the original
                            new_quest = Quest(
                                quest.name,
                                quest.description,
                                quest.monster_list.copy(),
                                quest.reward,
                                quest.penalty
                            )
                            # Update monsters slain
                            new_quest.monsters_slain = quest_data["monsters_slain"]
                            # Create new quest button
                            quest_button = QuestButton(
                                self.button_manager.quest_button_sheet,
                                0,  # x position will be set by ScrollableButtons
                                0,  # y position will be set by ScrollableButtons
                                700,  # width
                                100,  # height
                                1,  # scale
                                new_quest  # quest object
                            )
                            self.button_manager.completed_quests.add_button(quest_button)
                            break

            # Load failed quests and lock them
            if "failed_quests" in save_data:
                for quest_data in save_data["failed_quests"]:
                    # Find the quest in quest_list by name
                    for quest in quest_list:
                        if quest.name == quest_data["name"]:
                            # Create a new quest instance to avoid modifying the original
                            new_quest = Quest(
                                quest.name,
                                quest.description,
                                quest.monster_list.copy(),
                                quest.reward,
                                quest.penalty
                            )
                            # Update monsters slain
                            new_quest.monsters_slain = quest_data["monsters_slain"]
                            # Create new quest button and lock it
                            quest_button: QuestButton = QuestButton(
                                self.button_manager.quest_button_sheet,
                                0,  # x position will be set by ScrollableButtons
                                0,  # y position will be set by ScrollableButtons
                                700,  # width
                                100,  # height
                                1,  # scale
                                new_quest  # quest object
                            )
                            quest_button.lock()
                            quest_button.failed = True
                            # Add to failed quests list
                            self.button_manager.failed_quests.add_button(quest_button)
                            break

    def show_esc_popup(self) -> None:
        """Display the escape popup menu."""
        self.popup_running = True
        exit_text: str = "Exit Game" if self.game_state == GameState.NEW_GAME else "Save and Exit"
        exit_button = self.button_manager.get_button(GameState.PAUSE, "Exit")
        if exit_button:
            exit_button.update_text(exit_text)

        while self.popup_running:
            # Draw the current game screen in the background
            self.screen.fill(Colors.WHITE)
            
            # Draw game state specific background
            if self.game_state == GameState.VILLAGE:
                if self.hero:
                    self.hero.draw(self.screen, self.font, 0, GameConstants.SCREEN_HEIGHT // 2)
                self.button_manager.draw_buttons(self.screen, GameState.VILLAGE)
            elif self.game_state == GameState.NEW_GAME:
                self.text_box.draw(self.screen)
                self.button_manager.draw_buttons(self.screen, GameState.NEW_GAME)
            elif self.game_state == GameState.QUEST:
                if self.button_manager.get_button(GameState.QUEST, "Available").is_toggled():
                    self.button_manager.available_quests.draw(self.screen)
                else:
                    self.button_manager.completed_quests.draw(self.screen)
                self.button_manager.draw_buttons(self.screen, GameState.QUEST)
            elif self.game_state == GameState.BATTLE:
                if self.hero:
                    self.hero.draw(self.screen, self.font, 0, 25)
                if self.battle_manager and self.battle_manager.monster:
                    self.battle_manager.monster.draw(self.screen, self.font, GameConstants.SCREEN_WIDTH // 2, 25)
                self.button_manager.draw_buttons(self.screen, GameState.BATTLE)
                self._draw_battle_log()
            elif self.game_state == GameState.SHOP:
                self.button_manager.draw_buttons(self.screen, GameState.SHOP)
            
            # Draw popup background
            popup_rect = pygame.Rect(
                (GameConstants.SCREEN_WIDTH - GameConstants.POPUP_WIDTH) // 2,
                (GameConstants.SCREEN_HEIGHT - GameConstants.POPUP_HEIGHT) // 2,
                GameConstants.POPUP_WIDTH,
                GameConstants.POPUP_HEIGHT
            )
            pygame.draw.rect(self.screen, Colors.WHITE, popup_rect)
            pygame.draw.rect(self.screen, Colors.BLACK, popup_rect, 2)
            
            # Draw popup title
            draw_text_centered("Menu", self.font, Colors.BLACK, self.screen,
                popup_rect.centerx, popup_rect.y + 20)
            
            # Draw popup buttons
            self.button_manager.draw_buttons(self.screen, GameState.PAUSE)
            
            # Handle events first
            for event in self.event_manager.process_events():
                # Check for quit
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    self.running = False
                    self.popup_running = False
                    break
                    
                # Check for popup close
                if self.event_manager.handle_popup_events(event):
                    self.popup_running = False
                    break
                
                # Handle keyboard input
                key_action = self.event_manager.handle_keyboard_event(event)
                if key_action == "escape":
                    self.popup_running = False
                    break
                
                # Handle button clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click only
                    mouse_pos = pygame.mouse.get_pos()
                    for button_name, button in self.button_manager.get_buttons(GameState.PAUSE).items():
                        if not button.is_locked() and button.rect.collidepoint(mouse_pos):
                            if button_name == "Resume":
                                self.popup_running = False
                            elif button_name == "Options":
                                self.show_options_popup()
                            elif button_name == "Exit":
                                if self.game_state != GameState.NEW_GAME:
                                    self.save_game()
                                self.game_state = GameState.HOME
                                self.running = False
                                self.popup_running = False
                            break
            
            self.update()

    def show_options_popup(self) -> None:
        """Display the options popup menu."""
        self.popup_running = True
        volume_x: int = (GameConstants.SCREEN_WIDTH - 300) // 2
        volume_y: int = (GameConstants.SCREEN_HEIGHT - GameConstants.POPUP_HEIGHT) // 2 + 100
        volume_rect = pygame.Rect(volume_x, volume_y, 300, 20)
        
        while self.popup_running:
            # Draw the current game screen in the background
            self.screen.fill(Colors.WHITE)
            
            # Draw popup background
            popup_rect = pygame.Rect(
                (GameConstants.SCREEN_WIDTH - GameConstants.POPUP_WIDTH) // 2,
                (GameConstants.SCREEN_HEIGHT - GameConstants.POPUP_HEIGHT) // 2,
                GameConstants.POPUP_WIDTH,
                GameConstants.POPUP_HEIGHT
            )
            pygame.draw.rect(self.screen, Colors.WHITE, popup_rect)
            pygame.draw.rect(self.screen, Colors.BLACK, popup_rect, 2)
            
            # Draw popup title
            draw_text_centered("Options", self.font, Colors.BLACK, self.screen,
                popup_rect.centerx, popup_rect.y + 20)
            
            # Draw volume slider
            pygame.draw.rect(self.screen, Colors.GRAY, volume_rect)
            volume_pos = volume_x + int(pygame.mixer.music.get_volume() * 300)
            pygame.draw.rect(self.screen, Colors.BLUE,
                pygame.Rect(volume_x, volume_y, volume_pos - volume_x, 20))
            
            # Draw volume text
            draw_text_centered("Volume", self.font, Colors.BLACK, self.screen,
                popup_rect.centerx, volume_y - 20)
            
            # Draw popup buttons
            self.button_manager.draw_buttons(self.screen, GameState.OPTIONS)
            
            # Handle events
            for event in self.event_manager.process_events():
                # Check for quit
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    self.running = False
                    self.popup_running = False
                    break
                    
                # Check for popup close
                if self.event_manager.handle_popup_events(event):
                    self.popup_running = False
                    break
                
                # Handle keyboard input
                key_action = self.event_manager.handle_keyboard_event(event)
                if key_action == "escape":
                    self.popup_running = False
                    break
                
                # Handle volume slider
                new_volume = self.event_manager.handle_volume_slider(event, volume_rect, volume_x)
                if new_volume is not None:
                    pygame.mixer.music.set_volume(new_volume)
                
                # Handle button clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click only
                    mouse_pos = pygame.mouse.get_pos()
                    for button_name, button in self.button_manager.get_buttons(GameState.OPTIONS).items():
                        if not button.is_locked() and button.rect.collidepoint(mouse_pos):
                            if button_name == "Back":
                                self.popup_running = False
                            break
            
            self.update()

    def home_screen(self) -> None:
        """Display and handle the home screen."""
        self.running = True
        while self.running:
            self.screen.fill(Colors.WHITE)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click only
                    # Get home screen buttons
                    home_buttons = self.button_manager.get_buttons(GameState.HOME)
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check each button
                    for button_name, button in home_buttons.items():
                        if not button.is_locked() and button.rect.collidepoint(mouse_pos):
                            if button_name == "New Game":
                                self.game_state = GameState.NEW_GAME
                                self.running = False
                            elif button_name == "Load Game":
                                self.load_game()
                                self.game_state = GameState.VILLAGE
                                self.running = False
                            elif button_name == "Options":
                                self.show_options_popup()
                            elif button_name == "Exit Game":
                                self.game_state = GameState.EXIT
                                self.running = False
                            break

            # Draw all home screen buttons
            self.button_manager.draw_buttons(self.screen, GameState.HOME)
            self.update()

    def new_game_screen(self) -> None:
        """New game screen for creating a hero."""
        hero_class: str = ''
        self.running = True
        self.text_box.text = ''  # Reset text box
        self.text_box.temp_text = ''  # Reset temporary text

        # Load character images
        knight_image = pygame.image.load(resource_path('images/knight.png')).convert()
        assassin_image = pygame.image.load(resource_path('images/assassin.png')).convert()
        
        # Scale images to be larger for display
        character_size = (200, 200)  # Larger size for display
        knight_image = pygame.transform.scale(knight_image, character_size)
        assassin_image = pygame.transform.scale(assassin_image, character_size)

        # Calculate positions for character images
        image_y = GameConstants.SCREEN_HEIGHT // 4  # Quarter down the screen
        knight_x = GameConstants.SCREEN_WIDTH // 4 - character_size[0] // 2  # Left quarter
        assassin_x = (GameConstants.SCREEN_WIDTH * 3) // 4 - character_size[0] // 2  # Right quarter

        while self.running:
            self.screen.fill(Colors.WHITE)
            
            # Draw character images
            self.screen.blit(knight_image, (knight_x, image_y))
            self.screen.blit(assassin_image, (assassin_x, image_y))
            
            if self.button_manager.get_button(GameState.NEW_GAME, 'Knight').is_toggled():
                hero_class = 'Knight'
                # Draw selection highlight for Knight
                pygame.draw.rect(self.screen, Colors.YELLOW, 
                                (knight_x - 5, image_y - 5, 
                                character_size[0] + 10, character_size[1] + 10), 
                                3)  # 3px wide border
            elif self.button_manager.get_button(GameState.NEW_GAME, 'Assassin').is_toggled():
                hero_class = 'Assassin'
                # Draw selection highlight for Assassin
                pygame.draw.rect(self.screen, Colors.YELLOW, 
                                (assassin_x - 5, image_y - 5, 
                                character_size[0] + 10, character_size[1] + 10), 
                                3)  # 3px wide border
            else:
                hero_class = ''

            # Draw class labels
            draw_text_centered("Knight", self.font, Colors.BLACK, self.screen,
                             knight_x + character_size[0] // 2, image_y + character_size[1] + 10)
            draw_text_centered("Assassin", self.font, Colors.BLACK, self.screen,
                             assassin_x + character_size[0] // 2, image_y + character_size[1] + 10)

            # Draw text box first
            self.text_box.draw(self.screen)

            # Display current text from text box and hero class below it
            hero_name = self.text_box.text  # Use text instead of temp_text
            name_y = self.text_box.rect.bottom + 20  # 20px below text box
            class_y = name_y + 40  # 40px below name text
            
            draw_text_centered(f"Hero Name: {hero_name}", self.font, Colors.BLACK, self.screen, 
                             GameConstants.SCREEN_WIDTH // 2, name_y)
            draw_text_centered(f"Hero Class: {hero_class}", self.font, Colors.BLACK, self.screen, 
                             GameConstants.SCREEN_WIDTH // 2, class_y)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle text box activation
                    if self.text_box.rect.collidepoint(event.pos):
                        self.text_box.active = True
                    else:
                        self.text_box.active = False
                        # When deactivating, update the permanent text with the temporary text
                        if self.text_box.temp_text:
                            self.text_box.text = self.text_box.temp_text
                        
                    # Handle button clicks
                    if event.button == 1 and self.event_manager.can_click_buttons():  # Left click only
                        new_game_buttons = self.button_manager.get_buttons(GameState.NEW_GAME)
                        mouse_pos = pygame.mouse.get_pos()
                        
                        for button_name, button in new_game_buttons.items():
                            if not button.is_locked() and button.rect.collidepoint(mouse_pos):
                                self.event_manager.reset_button_delay()
                                if button_name == "Knight":
                                    self.button_manager.get_button(GameState.NEW_GAME, "Knight").toggle()
                                    self.button_manager.get_button(GameState.NEW_GAME, "Assassin").reset_toggle()
                                elif button_name == "Assassin":
                                    self.button_manager.get_button(GameState.NEW_GAME, "Assassin").toggle()
                                    self.button_manager.get_button(GameState.NEW_GAME, "Knight").reset_toggle()
                                elif button_name == "Back":
                                    self.button_manager.get_button(GameState.NEW_GAME, "Knight").reset_toggle()
                                    self.button_manager.get_button(GameState.NEW_GAME, "Assassin").reset_toggle()
                                    self.game_state = GameState.HOME
                                    self.running = False
                                elif button_name == "Create Hero":
                                    self.game_state = GameState.VILLAGE
                                    self.running = False
                                break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.event_manager.can_click_buttons():
                        self.event_manager.reset_button_delay()
                        self.show_esc_popup()
                    else:
                        self.text_box.handle_event(event)

            # Enable/disable Create Hero button based on having both name and class
            create_hero_button = self.button_manager.get_button(GameState.NEW_GAME, "Create Hero")
            if hero_name and hero_class and create_hero_button.is_locked():
                create_hero_button.unlock()
            elif (not hero_name or not hero_class) and not create_hero_button.is_locked():
                create_hero_button.lock()

            # Draw buttons and text box
            self.button_manager.draw_buttons(self.screen, GameState.NEW_GAME)
            self.text_box.draw(self.screen)
            self.update()

        if self.game_state == GameState.VILLAGE:
            hero_name = self.text_box.text
            if hero_class == "Knight":
                self.hero = Knight(hero_name)  # Knight class handles image loading
            else:
                self.hero = Assassin(hero_name)  # Assassin class handles image loading

    def village_screen(self) -> None:
        """Main village screen where the player can see the village status and access other features."""
        self.running = True
        self.event_manager.reset_button_delay()  # Start delay timer
        
        while self.running:
            self.screen.fill(Colors.WHITE)
            
            # Draw the village and hero
            self.village.draw(self.screen, GameConstants.SCREEN_WIDTH // 4, 50)  # Draw village at top quarter
            if self.hero:
                self.hero.draw(self.screen, self.font, 0, GameConstants.SCREEN_HEIGHT // 2)

            # Handle events
            for event in self.event_manager.process_events():
                # Check for quit
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    self.running = False
                    break
                    
                # Handle keyboard events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.event_manager.can_click_buttons():
                            self.event_manager.reset_button_delay()
                            self.show_esc_popup()
                            # If we returned from popup and game state changed, exit this screen
                            if self.game_state != GameState.VILLAGE:
                                self.running = False
                                break
                
                # Handle button clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Get main game buttons
                    main_buttons = self.button_manager.get_buttons(GameState.VILLAGE)
                    
                    # Check each button
                    for button_name, button in main_buttons.items():
                        if self.event_manager.handle_button_click(event, button.rect, button.is_locked()):
                            if button_name == "Menu":
                                self.show_esc_popup()
                                # If we returned from popup and game state changed, exit this screen
                                if self.game_state != GameState.VILLAGE:
                                    self.running = False
                                    break
                            elif button_name == "Quest":
                                self.game_state = GameState.QUEST
                                self.running = False
                            elif button_name == "Shop":
                                self.game_state = GameState.SHOP
                                self.running = False
                            break

            # Draw Buttons
            self.button_manager.draw_buttons(self.screen, GameState.VILLAGE)
            self.update()

    def shop_screen(self) -> None:
        """Shop screen where the hero can buy items."""
        self.running = True
        
        # Calculate positions for item sections
        section_width = GameConstants.SCREEN_WIDTH // 3
        section_height = 150
        y_start = 100
        padding = 20

        # Calculate clickable areas for each section
        potion_rect = pygame.Rect(padding, y_start, section_width - padding * 2, section_height)
        weapon_rect = pygame.Rect(section_width + padding, y_start, section_width - padding * 2, section_height)
        armor_rect = pygame.Rect(section_width * 2 + padding, y_start, section_width - padding * 2, section_height)

        # Calculate buy button area
        buy_button_rect = pygame.Rect(
            GameConstants.SCREEN_WIDTH // 2 - 100,
            y_start + section_height + padding,
            200,
            40
        )
        
        while self.running:
            self.screen.fill(Colors.WHITE)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.event_manager.can_click_buttons():
                        self.event_manager.reset_button_delay()
                        self.show_esc_popup()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click only
                    if self.event_manager.can_click_buttons():
                        mouse_pos = pygame.mouse.get_pos()
                        
                        # Check for section clicks
                        if potion_rect.collidepoint(mouse_pos):
                            self.village.shop.card_selected(ShopConstants.POTION_CARD_KEY)
                        elif weapon_rect.collidepoint(mouse_pos):
                            self.village.shop.card_selected(ShopConstants.WEAPON_CARD_KEY)
                        elif armor_rect.collidepoint(mouse_pos):
                            self.village.shop.card_selected(ShopConstants.ARMOR_CARD_KEY)
                        # Check for buy button click
                        elif (buy_button_rect.collidepoint(mouse_pos) and 
                            self.village.shop.card_selected_key is not None and 
                            self.village.shop.can_buy_selected(self.hero)):
                            self.village.shop.buy_item(self.hero)
                        # Check for leave button click
                        elif self.button_manager.get_button(GameState.SHOP, "Leave").rect.collidepoint(mouse_pos):
                            self.game_state = GameState.VILLAGE
                            self.running = False
            
            # Draw shop interface
            self.village.shop.draw(self.screen, self.hero)
            
            # Draw leave button
            self.button_manager.draw_buttons(self.screen, GameState.SHOP)
            self.update()

    def quest_screen(self) -> None:
        """Quest screen where the player can select and start quests."""
        self.running = True
        showing_available: bool = True  # Track which quest list is being shown
        showing_completed: bool = False  # Track if showing completed quests
        showing_failed: bool = False  # Track if showing failed quests
        
        # Ensure Available tab is selected and others are reset when opening screen
        quest_buttons = self.button_manager.get_buttons(GameState.QUEST)
        available_button = quest_buttons.get("Available")
        complete_button = quest_buttons.get("Complete")
        failed_button = quest_buttons.get("Failed")
        if available_button:
            available_button.toggle()
        if complete_button:
            complete_button.reset_toggle()
        if failed_button:
            failed_button.reset_toggle()

        # Initialize battle manager if it doesn't exist
        if self.battle_manager is None and self.hero:
            self.battle_manager = BattleManager(self.hero, self.battle_log)
        
        while self.running:
            self.screen.fill(Colors.WHITE)
            
            # Get quest buttons
            quest_buttons = self.button_manager.get_buttons(GameState.QUEST)
            start_button = quest_buttons.get("Start")
            available_button = quest_buttons.get("Available")
            complete_button = quest_buttons.get("Complete")
            failed_button = quest_buttons.get("Failed")
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.event_manager.can_click_buttons():
                        self.event_manager.reset_button_delay()
                        self.show_esc_popup()
                        if self.game_state != GameState.QUEST:
                            self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle quest list scrolling and selection
                    if showing_available:
                        self.button_manager.available_quests.handle_event(event)
                    elif showing_completed:
                        self.button_manager.completed_quests.handle_event(event)
                    elif showing_failed:
                        self.button_manager.failed_quests.handle_event(event)
                        
                    # Handle button clicks
                    if event.button == 1 and self.event_manager.can_click_buttons():  # Left click only
                        mouse_pos = pygame.mouse.get_pos()
                        for button_name, button in quest_buttons.items():
                            if not button.is_locked() and button.rect.collidepoint(mouse_pos):
                                # Handle tab buttons
                                if button_name == "Available":
                                    showing_available = True
                                    showing_completed = False
                                    showing_failed = False
                                    available_button.toggle()
                                    complete_button.reset_toggle()
                                    failed_button.reset_toggle()
                                elif button_name == "Complete":
                                    showing_available = False
                                    showing_completed = True
                                    showing_failed = False
                                    available_button.reset_toggle()
                                    complete_button.toggle()
                                    failed_button.reset_toggle()
                                elif button_name == "Failed":
                                    showing_available = False
                                    showing_completed = False
                                    showing_failed = True
                                    available_button.reset_toggle()
                                    complete_button.reset_toggle()
                                    failed_button.toggle()
                                # Handle action buttons
                                elif button_name == "Start" and selected_quest:
                                    self.current_quest = selected_quest.quest
                                    # Always create a fresh battle manager for a new quest
                                    self.battle_manager = BattleManager(self.hero, self.battle_log)
                                    self.game_state = GameState.BATTLE
                                    self.running = False
                                elif button_name == "Back":
                                    print("Quest screen: Back button clicked") # DEBUG
                                    self.game_state = GameState.VILLAGE
                                    self.running = False
                                break
                elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
                    if showing_available:
                        self.button_manager.available_quests.handle_event(event)
                    elif showing_completed:
                        self.button_manager.completed_quests.handle_event(event)
                    elif showing_failed:
                        self.button_manager.failed_quests.handle_event(event)
                elif event.type == pygame.MOUSEWHEEL:
                    if showing_available:
                        self.button_manager.available_quests.handle_event(event)
                    elif showing_completed:
                        self.button_manager.completed_quests.handle_event(event)
                    elif showing_failed:
                        self.button_manager.failed_quests.handle_event(event)
            
            # Draw the appropriate quest list
            if showing_available:
                self.button_manager.available_quests.draw(self.screen)
                selected_quest = self.button_manager.available_quests.get_selected_button()
            elif showing_completed:
                self.button_manager.completed_quests.draw(self.screen)
                selected_quest = self.button_manager.completed_quests.get_selected_button()
            else:  # showing_failed
                self.button_manager.failed_quests.draw(self.screen)
                selected_quest = self.button_manager.failed_quests.get_selected_button()
            
            # Update Start button state based on selection
            if selected_quest and showing_available and start_button.is_locked():
                start_button.unlock()
            elif (not selected_quest or not showing_available) and not start_button.is_locked():
                start_button.lock()
                
            # Draw all quest screen buttons
            self.button_manager.draw_buttons(self.screen, GameState.QUEST)
            self.update()

    def _update_potion_button_state(self, button_name: str, potion_type: str) -> None:
        """Helper method to update potion button states.
        
        Args:
            button_name: The name of the button to update
            potion_type: The type of potion the button uses
        """
        button = self.button_manager.get_button(GameState.BATTLE, button_name)
        if button is None:
            return
            
        if self.hero and self.hero.potion_bag[potion_type] > 0 and button.is_locked():
            button.unlock()
        elif self.hero and self.hero.potion_bag[potion_type] == 0 and not button.is_locked():
            button.lock()

    def _handle_quest_completion(self) -> None:
        """Helper method to handle quest completion logic."""
        if self.current_quest is None:
            return
            
        # Find the quest button in available quests
        for button in self.button_manager.available_quests.buttons:
            if button.quest == self.current_quest:
                # Check if hero died or fled - quest failed
                if not self.hero.is_alive() or self.game_state == GameState.QUEST:
                    self.button_manager.move_failed_quest(button)
                else:
                    self.button_manager.move_completed_quest(button)
                break
        
        # Reset battle state and buttons
        self.battle_manager.state = BattleState.HOME
        self.battle_manager.turn = TurnState.HERO_TURN
        self._switch_battle_layout(False)
        
        # Check if all quests are complete or failed
        if len(self.button_manager.available_quests.buttons) == 0:
            # Check if any quests were completed successfully
            if len(self.button_manager.completed_quests.buttons) > 0:
                self.game_state = GameState.VICTORY
            else:
                self.game_state = GameState.DEFEAT
            self.running = False
        else:
            self.game_state = GameState.QUEST
            self.running = False

    def _switch_battle_layout(self, to_victory: bool) -> None:
        """Switch between combat and victory button layouts.
        
        Args:
            to_victory: True to switch to victory layout, False for combat layout
        """
        battle_buttons = self.button_manager.get_buttons(GameState.BATTLE)
        
        # Combat buttons
        combat_buttons: List[str] = ['Attack', 'Defend', 'Potion', 'Flee']
        # Victory buttons
        victory_buttons: List[str] = ['Continue', 'Retreat']
        
        # Show/hide appropriate buttons
        for name, button in battle_buttons.items():
            if name in combat_buttons:
                if to_victory:
                    button.hide()
                    button.lock()  # Lock combat buttons in victory state
                else:
                    button.show()
                    # During combat, availability depends on turn
                    if self.battle_manager and self.battle_manager.turn == TurnState.HERO_TURN:
                        button.unlock()
                    else:
                        button.lock()
            elif name in victory_buttons:
                if to_victory:
                    button.show()
                    button.unlock()
                else:
                    button.hide()
                    button.lock()  # Lock victory buttons in combat state

    def _handle_monster_defeat(self) -> None:
        """Handle monster defeat logic."""
        if not self.battle_manager or not self.current_quest:
            return
            
        # Switch to victory layout
        self._switch_battle_layout(True)
        
        # Update quest progress using the proper method
        if self.battle_manager.monster:
            self.current_quest.slay_monster(self.battle_manager.monster)
        
        # Check if quest is complete
        if self.current_quest.is_complete():
            self._handle_quest_completion()

    def _draw_battle_log(self) -> None:
        """Draw the battle log on the screen."""
        # Calculate battle log position
        button_width = GameConstants.BUTTON_WIDTH + 40  # Button width plus margins
        log_x = button_width  # Start after buttons
        log_y = GameConstants.SCREEN_HEIGHT // 2  # Align with buttons
        log_width = GameConstants.SCREEN_WIDTH - button_width - 20  # Remaining width minus margin
        log_height = GameConstants.SCREEN_HEIGHT - log_y - 20  # Remaining height minus margin
        
        # Draw battle log background
        log_rect = pygame.Rect(
            log_x,  # x position after buttons
            log_y,  # y position aligned with buttons
            log_width,  # width fills remaining space
            log_height  # height fills remaining space
        )
        pygame.draw.rect(self.screen, Colors.LIGHT_GRAY, log_rect)
        
        # Draw battle log entries
        y_offset = 0
        # Calculate how many lines will fit in the log rect height
        max_lines = (log_rect.height - 20) // self.font.get_linesize()
        for log_entry in self.battle_log[-max_lines:]:
            text_surface = self.font.render(log_entry, True, Colors.BLACK)
            self.screen.blit(text_surface, (log_rect.x + 10, log_rect.y + 10 + y_offset))
            y_offset += self.font.get_linesize()

    def _setup_new_monster(self, monster: Optional[Monster]) -> bool:
        """Set up a new monster for battle.
        
        Args:
            monster: The monster to set up, or None if no monster available
            
        Returns:
            bool: True if setup was successful, False if no monster available
        """
        if not monster or not self.battle_manager:
            return False
            
        self.battle_manager.monster = monster
        self._switch_battle_layout(False)  # Switch to combat layout
        self.battle_log.append(f"A {monster.name} appears!")
        
        return True

    def battle_screen(self) -> None:
        """Battle screen where the hero fights a monster."""
        self.running = True
        self.event_manager.reset_button_delay()
        tooltip: Optional[Tooltip] = None

        # Initialize battle manager if needed
        if self.battle_manager is None:
            self.battle_manager = BattleManager(self.hero, self.battle_log)

        # Reset battle buttons to initial state
        battle_buttons = self.button_manager.get_buttons(GameState.BATTLE)
        
        # Hide victory buttons
        for name in ['Continue', 'Retreat']:
            if name in battle_buttons:
                battle_buttons[name].hide()
                battle_buttons[name].lock()
        
        # Set up combat buttons
        combat_buttons = ['Attack', 'Defend', 'Flee']
        for name in combat_buttons:
            if name in battle_buttons:
                button = battle_buttons[name]
                button.show()
                if self.battle_manager.turn == TurnState.HERO_TURN:
                    button.unlock()
                else:
                    button.lock()

        # Handle potion buttons
        if 'Potion' in battle_buttons:
            potion = battle_buttons['Potion']
            if self.hero and self.hero.has_potions():
                potion.unlock()
            else:
                potion.lock()

        # Hide selection buttons
        for name in ['Health Potion', 'Damage Potion', 'Block Potion']:
            if name in battle_buttons:
                battle_buttons[name].hide()
                battle_buttons[name].lock()

        # Set up monster if needed
        if not self.battle_manager.monster or not self.battle_manager.monster.is_alive():
            if self.current_quest:
                new_monster = self.current_quest.get_monster()
                success = self._setup_new_monster(new_monster)
                if not success:
                    self.game_state = GameState.QUEST
                    self.running = False
                    return
            else:
                self.game_state = GameState.QUEST
                self.running = False
                return

        # Main battle loop
        while self.running:
            # Draw the battle screen first
            self.screen.fill(Colors.WHITE)

            # Draw combatants
            if self.hero:
                self.hero.draw(self.screen, self.font, 0, 25)
            if self.battle_manager and self.battle_manager.monster:
                self.battle_manager.monster.draw(self.screen, self.font, GameConstants.SCREEN_WIDTH // 2, 25)

            # Update battle state and handle victory/defeat
            battle_result = self.battle_manager.update_battle_state()
            
            if battle_result is False:  # Hero defeated
                if self.current_quest:
                    for button in self.button_manager.available_quests.buttons:
                        if button.quest == self.current_quest:
                            self.button_manager.move_failed_quest(button)
                            if self.village.health <= 0:
                                self.game_state = GameState.DEFEAT
                            break
                self.game_state = GameState.DEFEAT
                self.running = False
            elif battle_result is True:  # Monster defeated
                self._handle_monster_defeat()
                
            # Update button states
            self.battle_manager.update_button_states(self.button_manager)

            # Handle events
            for event in self.event_manager.process_events():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    self.running = False
                    break
                
                # Handle keyboard input
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.event_manager.can_click_buttons():
                        self.event_manager.reset_button_delay()
                        self.show_esc_popup()
                        if self.game_state != GameState.BATTLE:
                            self.running = False
                            break

                # Handle button clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.event_manager.can_click_buttons():
                        mouse_pos = pygame.mouse.get_pos()
                        for button_name, button in battle_buttons.items():
                            if self.event_manager.handle_button_click(event, button.rect, button.is_locked()):
                                if button_name == "Continue" and self.battle_manager.state == BattleState.MONSTER_DEFEATED:
                                    # Get next monster
                                    new_monster = self.current_quest.get_monster()
                                    success, new_tooltip = self._setup_new_monster(new_monster)
                                    if success:
                                        tooltip = new_tooltip
                                        self.battle_manager.state = BattleState.HOME
                                        self.battle_manager.turn = TurnState.HERO_TURN
                                        self._switch_battle_layout(False)
                                    else:
                                        self.game_state = GameState.QUEST
                                        self.running = False
                                    break

                                # Handle combat actions during hero's turn
                                if self.battle_manager.turn == TurnState.HERO_TURN:
                                    if button_name == "Attack":
                                        self.battle_manager.handle_attack(self.battle_manager.monster)
                                        self.event_manager.reset_button_delay()
                                    elif button_name == "Defend":
                                        self.battle_manager.handle_defend()
                                        self.event_manager.reset_button_delay()
                                    elif button_name == "Potion":
                                        self.battle_manager.handle_use_potion()
                                        self.event_manager.reset_button_delay()
                                    elif button_name == "Flee":
                                        if self.battle_manager.handle_flee():
                                            self.battle_log.append(f"{self.hero.name} flees from battle!")
                                            self._handle_quest_failure()
                                    elif button_name.startswith("Ability_"):
                                        ability_name = button_name.replace("Ability_", "")
                                        self.battle_manager.use_ability(ability_name)
                                        self.event_manager.reset_button_delay()
                                    elif button_name in ["Health Potion", "Damage Potion", "Block Potion"]:
                                        self.battle_manager.use_potion(button_name)
                                        self.event_manager.reset_button_delay()

                                # Handle retreat button
                                if button_name == "Retreat":
                                    self.battle_log.append(f"{self.hero.name} retreats to regroup!")
                                    self._handle_quest_failure()
                                break

            # Draw UI elements
            self._draw_battle_log()
            self.button_manager.draw_buttons(self.screen, GameState.BATTLE)

            # Draw turn indicator during combat
            if self.battle_manager.state != BattleState.MONSTER_DEFEATED:
                turn_text = "Monster's Turn" if self.battle_manager.turn == TurnState.MONSTER_TURN else "Your Turn"
                draw_text_centered(turn_text, self.font, Colors.BLACK, self.screen, 
                                GameConstants.SCREEN_WIDTH // 2, 10)

            # Draw tooltips
            mouse_pos = pygame.mouse.get_pos()

            if self.battle_manager.state == BattleState.USE_ITEM:
                for potion_name in ['Health Potion', 'Damage Potion', 'Block Potion']:
                    button = self.button_manager.get_button(GameState.BATTLE, potion_name)
                    if button and not button.is_locked() and button.rect.collidepoint(mouse_pos):
                        if potion_tooltip := self.battle_manager.get_potion_tooltip(potion_name):
                            potion_tooltip.draw(self.screen, mouse_pos[0] + 10, mouse_pos[1])

            if self.battle_manager.state == BattleState.USE_ABILITY:
                for button_name, button in battle_buttons.items():
                    if button_name.startswith("Ability_") and not button.is_locked() and button.rect.collidepoint(mouse_pos):
                        if ability_tooltip := self.battle_manager.get_ability_tooltip(button_name):
                            ability_tooltip.draw(self.screen, mouse_pos[0] + 10, mouse_pos[1])

            self.update()

    def victory_screen(self) -> None:
        """Display the victory screen when all quests are completed."""
        self.running = True
        while self.running:
            self.screen.fill(Colors.WHITE)
            draw_text_centered("Victory!", self.font, Colors.GOLD, self.screen, 
                GameConstants.SCREEN_WIDTH // 2, GameConstants.SCREEN_HEIGHT // 2 - 100)
            draw_text_centered(f"{self.hero.name if self.hero else 'Hero'} has saved the village!", self.font, Colors.BLACK, 
                self.screen, GameConstants.SCREEN_WIDTH // 2, GameConstants.SCREEN_HEIGHT // 2 - 50)
            draw_text_centered("Press ESC to return to the main menu", self.font, Colors.BLACK, 
                self.screen, GameConstants.SCREEN_WIDTH // 2, GameConstants.SCREEN_HEIGHT // 2 + 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.HOME
                        self.running = False
            self.update()

    def defeat_screen(self) -> None:
        """Display the defeat screen when hero dies or village falls."""
        self.running = True
        defeat_reason: str = "The village has fallen!"
        
        while self.running:
            self.screen.fill(Colors.WHITE)
            draw_text_centered(defeat_reason, self.font, Colors.RED, self.screen, 
                GameConstants.SCREEN_WIDTH // 2, GameConstants.SCREEN_HEIGHT // 2 - 100)
            draw_text_centered("Game Over", self.font, Colors.BLACK, self.screen, 
                GameConstants.SCREEN_WIDTH // 2, GameConstants.SCREEN_HEIGHT // 2 - 50)
            draw_text_centered("Press ESC to return to the main menu", self.font, Colors.BLACK, 
                self.screen, GameConstants.SCREEN_WIDTH // 2, GameConstants.SCREEN_HEIGHT // 2 + 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.HOME
                        self.running = False
            self.update()

    def _handle_popup_events(self, event: pygame.event.Event) -> Optional[str]:
        """Handle events when a popup is active.
        
        Args:
            event: The pygame event to handle
            
        Returns:
            The key action if a key was pressed, None if no relevant action was taken
        """
        if event.type == pygame.QUIT:
            self.game_state = GameState.EXIT
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if self.key_actions and event.key in self.key_actions:
                if self.key_actions[event.key] == "escape":
                    self.popup_running = False  # Resume game on escape
                else:
                    return self.key_actions[event.key]
            elif event.unicode and len(event.unicode) == 1 and event.unicode.isprintable():
                return event.unicode
        return None

    def _handle_keyboard_events(self, event: pygame.event.Event) -> Optional[str]:
        """Handle keyboard events.
        
        Args:
            event: The pygame event to handle
            
        Returns:
            The key action if a key was pressed, None if no relevant action was taken
        """
        if event.type == pygame.KEYDOWN:
            if self.key_actions and event.key in self.key_actions:
                if self.game_state != GameState.HOME:
                    if self.key_actions[event.key] == "escape":
                        self.show_esc_popup()
                    else:
                        return self.key_actions[event.key]
            elif event.unicode and len(event.unicode) == 1 and event.unicode.isprintable():
                return event.unicode
        return None

    def _handle_mouse_events(self, event: pygame.event.Event) -> None:
        """Handle mouse events.
        
        Args:
            event: The pygame event to handle
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.game_state == GameState.NEW_GAME:
                if self.text_box.rect.collidepoint(event.pos):
                    self.text_box.active = True
                else:
                    self.text_box.active = False

    def _update_buttons(self) -> None:
        """Update all buttons in the current game state."""
        buttons = self.button_manager.get_buttons(self.game_state)
        for button in buttons.values():
            button.draw(None)  # Update button state without drawing
            if button.was_clicked:
                for button_name, btn in buttons.items():
                    if btn == button:
                        self._handle_button_click(button_name)
                        break

    def events(self) -> Optional[str]:
        """Handle all game events.
        
        Returns:
            The key action if a key was pressed, None if no relevant action was taken
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.EXIT
                self.running = False
                return None

            if self.popup_running:
                result = self._handle_popup_events(event)
                if result:
                    return result
            else:
                # Handle text box input in NEW_GAME state
                if self.game_state == GameState.NEW_GAME:
                    self.text_box.handle_event(event)

                # Handle keyboard events
                result = self._handle_keyboard_events(event)
                if result:
                    return result

                # Handle mouse events
                self._handle_mouse_events(event)

            # Update button states
            self._update_buttons()

        return None

    def _handle_button_click(self, button_name: str) -> None:
        """Handle button clicks based on current game state and button name.
        
        Args:
            button_name: The name of the button that was clicked
        """
        if self.game_state == GameState.HOME:
            if button_name == "New Game":
                self.game_state = GameState.NEW_GAME
                self.running = False
            elif button_name == "Load Game":
                self.load_game()
                self.game_state = GameState.VILLAGE
                self.running = False
            elif button_name == "Options":
                self.show_options_popup()
            elif button_name == "Exit Game":
                self.game_state = GameState.EXIT
                self.running = False
                
        elif self.game_state == GameState.NEW_GAME:
            if button_name == "Knight":
                self.button_manager.get_button(GameState.NEW_GAME, "Knight").toggle()
                self.button_manager.get_button(GameState.NEW_GAME, "Assassin").reset_toggle()
            elif button_name == "Assassin":
                self.button_manager.get_button(GameState.NEW_GAME, "Assassin").toggle()
                self.button_manager.get_button(GameState.NEW_GAME, "Knight").reset_toggle()
            elif button_name == "Back":
                self.button_manager.get_button(GameState.NEW_GAME, "Knight").reset_toggle()
                self.button_manager.get_button(GameState.NEW_GAME, "Assassin").reset_toggle()
                self.game_state = GameState.HOME
                self.running = False
            elif button_name == "Create Hero":
                self.game_state = GameState.VILLAGE
                self.running = False
        
        elif self.game_state == GameState.VILLAGE:
            if button_name == "Menu":
                self.show_esc_popup()
            elif button_name == "Quest":
                self.game_state = GameState.QUEST
                self.running = False
            elif button_name == "Shop":
                self.game_state = GameState.SHOP
                self.running = False
                
        elif self.game_state == GameState.SHOP:
            if button_name == "Leave":
                self.game_state = GameState.VILLAGE
                self.running = False
                
        elif self.game_state == GameState.QUEST:
            if button_name == "Back":
                self.game_state = GameState.VILLAGE
                self.running = False
            elif button_name == "Start":
                self.game_state = GameState.BATTLE
                self.running = False        
        elif self.game_state == GameState.BATTLE:
            # Initialize battle manager if it doesn't exist
            if self.battle_manager is None and self.hero:
                self.battle_manager = BattleManager(self.hero, self.battle_log)
                
            # Only process battle actions during hero's turn if battle manager exists
            if self.battle_manager and self.battle_manager.turn == TurnState.HERO_TURN:
                if button_name == "Attack":
                    self.battle_manager.handle_attack(self.battle_manager.monster)
                elif button_name == "Defend":
                    self.battle_manager.handle_defend()
                elif button_name == "Potion":
                    self.battle_manager.handle_use_potion()
                elif button_name == "Flee":
                    if self.battle_manager.handle_flee():
                        self.battle_log.append(f"{self.hero.name} flees from battle!")
                        # Mark quest as failed when fleeing
                        if self.current_quest:
                            for button in self.button_manager.available_quests.buttons:
                                if button.quest == self.current_quest:
                                    self.button_manager.move_failed_quest(button)
                                    # Check if village is defeated after applying penalty
                                    if self.village.health <= 0:
                                        self.game_state = GameState.DEFEAT
                                        self.running = False
                                        break
                        self.game_state = GameState.QUEST
                        self.running = False
            
            # Handle Retreat button regardless of turn
            if button_name == "Retreat":
                self.battle_log.append(f"{self.hero.name} retreats to regroup!")
                # Mark quest as failed when retreating
                if self.current_quest:
                    for button in self.button_manager.available_quests.buttons:
                        if button.quest == self.current_quest:
                            self.button_manager.move_failed_quest(button)
                            # Check if village is defeated after applying penalty
                            if self.village.health <= 0:
                                self.game_state = GameState.DEFEAT
                                self.running = False
                                break
                    self.game_state = GameState.QUEST
                    self.running = False

    def _handle_quest_failure(self) -> None:
        """Helper method to handle quest failure logic."""
        if self.current_quest:
            for button in self.button_manager.available_quests.buttons:
                if button.quest == self.current_quest:
                    self.button_manager.move_failed_quest(button)
                    if self.village.health <= 0:
                        self.game_state = GameState.DEFEAT
                        self.running = False
                        return
            self.game_state = GameState.QUEST
            self.running = False