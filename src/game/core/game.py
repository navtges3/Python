from src.game.managers.battle_manager import *
from src.game.managers.screen_manager import *
from src.game.managers.button_manager import ButtonManager
from src.game.managers.event_manager import EventManager
from src.game.entities.hero import *
from src.game.entities.items import *
from src.game.core.constants import *
from src.game.entities.quest import *
from src.game.utils.fileIO import save_file_exists, save_game, load_game, resource_path
import pygame

class Game:
    pygame.init()

    font = pygame.font.Font(None, 24)
    
    key_actions = {
        pygame.K_ESCAPE: "escape",
        pygame.K_BACKSPACE: "backspace",
        pygame.K_RETURN: "enter",
        pygame.K_DELETE: "delete",
        pygame.K_TAB: "tab",
    }

    """Class to manage different game screens."""
    def __init__(self) -> None:
        self.game_state = GameState.WELCOME
        self.battle_log = []
        self.hero = None
        self.current_quest = None
        self.running = False
        self.popup_running = False
        self.battle_manager = None
        self.event_manager = EventManager()  # Initialize the event manager
        
        # Initialize the mixer for music
        pygame.mixer.init()
        # Load and play background music
        pygame.mixer.music.load(resource_path('music\\background_music.mp3'))
        pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # Play music in a loop

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((GameConstants.SCREEN_WIDTH, GameConstants.SCREEN_HEIGHT))
        pygame.display.set_caption('Village Defense')
        pygame.display.set_icon(pygame.image.load(resource_path('icon.ico')))

        self.screen_manager = ScreenManager(self.screen, self.font)
        # Load button sprite sheet
        button_sheet = pygame.image.load(resource_path('images\\buttons\\button_sheet_0.png')).convert_alpha()
        quest_button_sheet = pygame.image.load(resource_path('images\\buttons\\quest_sheet.png')).convert_alpha()
        self.button_manager = ButtonManager(self.font, button_sheet, quest_button_sheet)
        
        self.text_box = TextBox(
            rect=pygame.Rect(100, 150, 200, 30),
            font=self.font,
            placeholder="Enter Hero Name",
        )

    def update(self) -> None:
        self.clock.tick(GameConstants.FPS)
        pygame.display.update()

    def quit(self) -> None:
        """Quit the game."""
        pygame.quit()

    def save_game(self) -> None:
        """Save the player's progress."""
        save_data = {}
        if self.hero is not None:
            save_data.update({"hero": self.hero.to_dict(),})  # Save hero data
        if self.battle_manager and self.battle_manager.monster is not None:
            save_data.update({"monster": self.battle_manager.monster.to_dict(),})
        save_data.update({
            "game_volume": pygame.mixer.music.get_volume(),
        })

        # Save quest lists
        available_quests = []
        completed_quests = []
        
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
            
        save_data.update({
            "available_quests": available_quests,
            "completed_quests": completed_quests
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

    def show_esc_popup(self) -> None:
        """Show the escape popup menu."""
        self.popup_running = True
        exit_text = "Exit Game" if self.game_state == GameState.NEW_GAME else "Save and Exit"
        self.button_manager.get_button(GameState.PAUSE, "Exit").update_text(exit_text)

        while self.popup_running:
            # Draw the current game screen in the background
            if self.game_state == GameState.MAIN_GAME:
                self.screen.fill(Colors.WHITE)
                self.hero.draw(self.screen, self.font, 0, GameConstants.SCREEN_HEIGHT // 2)
                self.button_manager.draw_buttons(self.screen, GameState.MAIN_GAME)
            
            # Handle events first
            for event in self.event_manager.process_events():
                # Check for quit
                self.game_state, self.running = self.event_manager.handle_quit_event(event, self.game_state)
                if not self.running:
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
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Get pause buttons
                    pause_buttons = self.button_manager.get_buttons(GameState.PAUSE)
                    
                    # Check each button
                    for button_name, button in pause_buttons.items():
                        if self.event_manager.handle_button_click(event, button.rect, button.is_locked()):
                            if button_name == "Resume":
                                self.popup_running = False
                                break
                            elif button_name == "Options":
                                self.show_options_popup()
                                break
                            elif button_name == "Exit":
                                if self.game_state != GameState.NEW_GAME:
                                    self.save_game()  # Save the game if we're not in new game state
                                self.game_state = GameState.WELCOME
                                self.popup_running = False
                                self.running = False
                                break
            
            # Update and draw popup buttons (without processing clicks)
            pause_buttons = self.button_manager.get_buttons(GameState.PAUSE)
            for button in pause_buttons.values():
                button.draw(None)  # Just update visual state
            
            # Draw the popup and its buttons
            self.screen_manager.draw_popup("Pause Menu", pause_buttons)
            
            # Update display
            self.update()

    def show_options_popup(self) -> None:
        """Show the options popup menu."""
        options_running = True
        self.button_manager.get_button(GameState.OPTIONS, "Back").update_text("Back")
        music_volume = pygame.mixer.music.get_volume()
        dragging_volume = False

        # Create volume slider rect
        volume_x = (GameConstants.SCREEN_WIDTH - GameConstants.POPUP_WIDTH) // 2 + 50
        volume_y = (GameConstants.SCREEN_HEIGHT - GameConstants.POPUP_HEIGHT) // 2 + 120
        volume_rect = pygame.Rect(volume_x, volume_y, 300, 10)

        options_buttons = self.button_manager.get_buttons(GameState.OPTIONS) 
        while options_running:
            # Draw the current game screen in the background
            if self.game_state == GameState.MAIN_GAME:
                self.screen.fill(Colors.WHITE)
                self.hero.draw(self.screen, self.font, 0, GameConstants.SCREEN_HEIGHT // 2)
                self.button_manager.draw_buttons(self.screen, GameState.MAIN_GAME)
            
            # Handle events
            for event in self.event_manager.process_events():
                # Check for quit
                self.game_state, self.running = self.event_manager.handle_quit_event(event, self.game_state)
                if not self.running:
                    options_running = False
                    break
                
                # Check for popup close
                if self.event_manager.handle_popup_events(event):
                    options_running = False
                    break
                    
                # Handle volume slider
                if dragging_volume:
                    new_volume = self.event_manager.handle_volume_slider(event, volume_rect, volume_x)
                    if new_volume is not None:
                        music_volume = new_volume
                        pygame.mixer.music.set_volume(music_volume)
                    if event.type == pygame.MOUSEBUTTONUP:
                        dragging_volume = False
                else:
                    # Handle button clicks and volume slider activation
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Check if clicked on volume bar
                        if volume_rect.collidepoint(event.pos):
                            dragging_volume = True
                            new_volume = self.event_manager.handle_volume_slider(event, volume_rect, volume_x)
                            if new_volume is not None:
                                music_volume = new_volume
                                pygame.mixer.music.set_volume(music_volume)
                        else:
                            # Check buttons
                            for button_name, button in options_buttons.items():
                                if self.event_manager.handle_button_click(event, button.rect, button.is_locked()):
                                    if button_name == "Back":
                                        options_running = False
                                    break
            
            # Update and draw buttons
            for button in options_buttons.values():
                button.draw(None)  # Update button states
            
            # Draw the popup and its buttons
            self.screen_manager.draw_popup("Options", options_buttons)
            
            # Draw volume label
            draw_text("Music Volume", self.font, Colors.BLACK, self.screen, volume_x, volume_y - 30)
            # Draw slider background
            pygame.draw.rect(self.screen, Colors.GRAY, volume_rect)
            # Draw volume level
            pygame.draw.rect(self.screen, Colors.BLUE, (volume_x, volume_y, 300 * music_volume, 10))
            
            self.update()

    def welcome_screen(self) -> None:
        """Welcome screen with options to start a new game or load an existing game."""
        self.running = True

        # Check for save file
        if save_file_exists():
            self.button_manager.get_button(GameState.WELCOME, "Load Game").unlock()
        else:
            self.button_manager.get_button(GameState.WELCOME, "Load Game").lock()
            
        while self.running:
            self.screen.fill(Colors.WHITE)

            # Draw welcome text
            draw_text_centered(
                "Welcome to Village Defense!", 
                self.font, 
                Colors.BLACK, 
                self.screen, 
                GameConstants.SCREEN_WIDTH // 2, 
                GameConstants.SCREEN_HEIGHT // 2 - 100
            )

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click only
                    # Get welcome buttons
                    welcome_buttons = self.button_manager.get_buttons(GameState.WELCOME)
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check each button
                    for button_name, button in welcome_buttons.items():
                        if not button.is_locked() and button.rect.collidepoint(mouse_pos):
                            if button_name == "New Game":
                                self.game_state = GameState.NEW_GAME
                                self.running = False
                            elif button_name == "Load Game":
                                self.load_game()
                                self.game_state = GameState.MAIN_GAME
                                self.running = False
                            elif button_name == "Options":
                                self.show_options_popup()
                            elif button_name == "Exit Game":
                                self.game_state = GameState.EXIT
                                self.running = False
                            break

            # Draw all welcome screen buttons
            self.button_manager.draw_buttons(self.screen, GameState.WELCOME)
            self.update()

    def new_game_screen(self) -> None:
        """New game screen for creating a hero."""
        hero_class = ''
        self.running = True
        self.text_box.text = ''  # Reset text box
        self.text_box.temp_text = ''  # Reset temporary text

        knight = make_hero('Knight', 'Knight')
        assassin = make_hero('Assassin', 'Assassin')

        while self.running:
            self.screen.fill(Colors.WHITE)
            
            if self.button_manager.get_button(GameState.NEW_GAME, 'Knight').is_toggled():
                hero_class = 'Knight'
            elif self.button_manager.get_button(GameState.NEW_GAME, 'Assassin').is_toggled():
                hero_class = 'Assassin'
            else:
                hero_class = ''

            # Display current text from text box
            hero_name = self.text_box.temp_text if self.text_box.active else self.text_box.text
            draw_text(f"Hero Name: {hero_name}", self.font, Colors.BLACK, self.screen, 
                     GameConstants.SCREEN_WIDTH // 2 - self.font.size("Hero Name: ")[0], 
                     GameConstants.SCREEN_HEIGHT // 2 + self.font.get_linesize())
            draw_text(f"Hero Class: {hero_class}", self.font, Colors.BLACK, self.screen, 
                     GameConstants.SCREEN_WIDTH // 2 - self.font.size("Hero Class: ")[0], 
                     GameConstants.SCREEN_HEIGHT // 2 + self.font.get_linesize() * 2.5)

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
                                    self.game_state = GameState.WELCOME
                                    self.running = False
                                elif button_name == "Create Hero":
                                    self.game_state = GameState.MAIN_GAME
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

        if self.game_state == GameState.MAIN_GAME:
            self.hero = knight if hero_class == "Knight" else assassin
            self.hero.name = self.text_box.text

    def main_game(self) -> None:
        """Main game screen."""
        self.running = True
        self.event_manager.reset_button_delay()  # Start delay timer
        
        while self.running:
            self.screen.fill(Colors.WHITE)
            
            # Draw the hero
            self.hero.draw(self.screen, self.font, 0, GameConstants.SCREEN_HEIGHT // 2)

            # Handle events
            for event in self.event_manager.process_events():
                # Check for quit
                self.game_state, self.running = self.event_manager.handle_quit_event(event, self.game_state)
                if not self.running:
                    break
                    
                # Handle keyboard events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.event_manager.can_click_buttons():
                            self.event_manager.reset_button_delay()
                            self.show_esc_popup()
                
                # Handle button clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Get main game buttons
                    main_buttons = self.button_manager.get_buttons(GameState.MAIN_GAME)
                    
                    # Check each button
                    for button_name, button in main_buttons.items():
                        if self.event_manager.handle_button_click(event, button.rect, button.is_locked()):
                            if button_name == "Menu":
                                self.show_esc_popup()
                            elif button_name == "Quest":
                                self.game_state = GameState.QUEST
                                self.running = False
                            elif button_name == "Shop":
                                self.game_state = GameState.SHOP
                                self.running = False
                            break

            # Draw Buttons
            self.button_manager.draw_buttons(self.screen, GameState.MAIN_GAME)
            self.update()

    def shop_screen(self) -> None:
        """Shop screen where the hero can buy items."""
        self.running = True
        
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
                        shop_buttons = self.button_manager.get_buttons(GameState.SHOP)
                        mouse_pos = pygame.mouse.get_pos()
                        
                        for button_name, button in shop_buttons.items():
                            if not button.is_locked() and button.rect.collidepoint(mouse_pos):
                                self.event_manager.reset_button_delay()
                                if button_name == "Leave":
                                    self.game_state = GameState.MAIN_GAME
                                    self.running = False
                                break
            
            # Draw shop buttons
            self.button_manager.draw_buttons(self.screen, GameState.SHOP)
            self.update()

    def quest_screen(self) -> None:
        """Quest screen where the player can select and start quests."""
        self.running = True
        showing_available = True  # Track which quest list is being shown
        
        while self.running:
            self.screen.fill(Colors.WHITE)
            
            # Get quest buttons
            quest_buttons = self.button_manager.get_buttons(GameState.QUEST)
            start_button = quest_buttons.get("Start")
            available_button = quest_buttons.get("Available")
            complete_button = quest_buttons.get("Complete")
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.event_manager.can_click_buttons():
                        self.event_manager.reset_button_delay()
                        self.show_esc_popup()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle quest list scrolling and selection
                    if showing_available:
                        self.button_manager.available_quests.handle_event(event)
                    else:
                        self.button_manager.completed_quests.handle_event(event)
                        
                    # Handle button clicks
                    if event.button == 1 and self.event_manager.can_click_buttons():  # Left click only
                        mouse_pos = pygame.mouse.get_pos()
                        for button_name, button in quest_buttons.items():
                            if not button.is_locked() and button.rect.collidepoint(mouse_pos):
                                self.event_manager.reset_button_delay()
                                if button_name == "Available":
                                    showing_available = True
                                    available_button.toggle()
                                    complete_button.reset_toggle()
                                elif button_name == "Complete":
                                    showing_available = False
                                    complete_button.toggle()
                                    available_button.reset_toggle()
                                elif button_name == "Back":
                                    self.game_state = GameState.MAIN_GAME
                                    self.running = False
                                elif button_name == "Start" and selected_quest:
                                    self.current_quest = selected_quest.quest
                                    self.game_state = GameState.BATTLE
                                    self.running = False
                                break
                elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
                    if showing_available:
                        self.button_manager.available_quests.handle_event(event)
                    else:
                        self.button_manager.completed_quests.handle_event(event)
                elif event.type == pygame.MOUSEWHEEL:
                    if showing_available:
                        self.button_manager.available_quests.handle_event(event)
                    else:
                        self.button_manager.completed_quests.handle_event(event)
            
            # Draw the appropriate quest list
            if showing_available:
                self.button_manager.available_quests.draw(self.screen)
                selected_quest = self.button_manager.available_quests.get_selected_button()
            else:
                self.button_manager.completed_quests.draw(self.screen)
                selected_quest = self.button_manager.completed_quests.get_selected_button()
            
            # Update Start button state based on selection
            if selected_quest and showing_available and start_button.is_locked():
                start_button.unlock()
            elif (not selected_quest or not showing_available) and not start_button.is_locked():
                start_button.lock()
                
            # Draw all quest screen buttons
            self.button_manager.draw_buttons(self.screen, GameState.QUEST)
            self.update()

    def _update_potion_button_state(self, button_name: str, potion_type: str) -> None:
        """Helper method to update potion button states."""
        button = self.button_manager.get_button(GameState.BATTLE, button_name)
        if self.hero.potion_bag[potion_type] > 0 and button.is_locked():
            button.unlock()
        elif self.hero.potion_bag[potion_type] == 0 and not button.is_locked():
            button.lock()

    def _handle_quest_completion(self) -> None:
        """Helper method to handle quest completion logic."""
        # Find the quest button in available quests
        for button in self.button_manager.available_quests.buttons:
            if button.quest == self.current_quest:
                self.button_manager.move_completed_quest(button)
                break
        
        # Check if all quests are complete
        if len(self.button_manager.available_quests.buttons) == 0:
            self.game_state = GameState.VICTORY
            self.running = False
        else:
            self.game_state = GameState.QUEST
            self.running = False

    def _switch_battle_layout(self, to_victory: bool) -> None:
        """Switch between combat and victory button layouts."""
        battle_buttons = self.button_manager.get_buttons(GameState.BATTLE)
        
        # Combat buttons
        combat_buttons = ['Attack', 'Defend', 'Use Potion', 'Flee']
        # Victory buttons
        victory_buttons = ['Continue', 'Retreat']
        
        # Lock/unlock appropriate buttons
        for name, button in battle_buttons.items():
            if name in combat_buttons:
                if to_victory:
                    button.lock()
                else:
                    # During combat, availability depends on turn
                    if self.battle_manager.turn == TurnState.HERO_TURN:
                        button.unlock()
                    else:
                        button.lock()
            elif name in victory_buttons:
                if to_victory:
                    button.unlock()
                else:
                    button.lock()

    def _handle_monster_defeat(self) -> None:
        """Helper method to handle monster defeat logic."""
        print("Monster defeated!")
        self.battle_log.append(f"{self.battle_manager.monster.name} has been defeated!")
        self.battle_log.append(f"{self.hero.name} gains {self.battle_manager.monster.experience} experience and {self.battle_manager.monster.gold} gold.")
        self.hero.gain_experience(self.battle_manager.monster.experience)
        self.hero.add_gold(self.battle_manager.monster.gold)
        self.current_quest.slay_monster(self.battle_manager.monster)
        
        # Switch to victory layout
        self._switch_battle_layout(True)
        
        # Check if quest is complete
        if self.current_quest.is_complete():
            self.battle_log.append("Quest complete!")
            self._handle_quest_completion()
        else:
            self.battle_manager.state = BattleState.MONSTER_DEFEATED

    def _draw_battle_log(self) -> None:
        """Helper method to draw the battle log."""
        # Draw border for battle log
        log_border = pygame.Rect(
            GameConstants.BATTLE_SCREEN_LOG_BORDER_X,  # Start after buttons
            GameConstants.BATTLE_SCREEN_LOG_BORDER_Y,  # Same height as buttons
            GameConstants.BATTLE_SCREEN_LOG_BORDER_WIDTH - 10,  # Rest of screen width minus margin
            GameConstants.BATTLE_SCREEN_LOG_BORDER_HEIGHT - 10  # Same height as button area minus margin
        )
        pygame.draw.rect(self.screen, Colors.BLACK, log_border, width=2, border_radius=10)

        # Draw battle log title
        draw_text_centered("Battle Log", self.font, Colors.BLACK, self.screen,
                        log_border.centerx, log_border.y + 20)

        # Draw the most recent battle log entries
        log_x = log_border.x + 20
        log_y = log_border.y + 50
        max_width = log_border.width - 40

        # Show the last 8 log entries
        for log_entry in self.battle_log[-8:]:
            draw_wrapped_text(log_entry, self.font, Colors.BLACK, self.screen, log_x, log_y, max_width)
            log_y += self.font.get_linesize() * 2  # Double space between entries

    def battle_screen(self) -> None:
        """Battle screen where the hero fights a monster."""
        self.running = True
        self.event_manager.reset_button_delay()  # Start delay timer
        
        if self.battle_manager is None:
            self.battle_manager = BattleManager(self.hero, self.battle_log)
        
        # Spawn a new monster if there's no monster or if the current monster is dead
        if self.battle_manager.monster is None or not self.battle_manager.monster.is_alive():
            new_monster = self.current_quest.get_monster()
            if new_monster:
                self.battle_manager.start_battle(new_monster)
            else:
                # No more monsters in the quest, return to quest screen
                self.game_state = GameState.QUEST
                self.running = False
                return
        
        tooltip = Tooltip(f"Attack {self.battle_manager.monster.name} with your {self.hero.weapon.name}!", self.font)

        while self.running:
            # Draw the battle screen first
            self.screen.fill(Colors.WHITE)
            self.hero.draw(self.screen, self.font, 0, 25)
            if self.battle_manager.monster:
                self.battle_manager.monster.draw(self.screen, self.font, GameConstants.SCREEN_WIDTH // 2, 25)
            
            # Update battle state and check for victory/defeat
            battle_result = self.battle_manager.update_battle_state()
            if battle_result is False:  # Hero defeated
                print("Hero defeated!")
                self.game_state = GameState.DEFEAT
                self.running = False
            elif battle_result is True:  # Monster defeated
                self._handle_monster_defeat()
            
            # Update button states after state changes
            self.battle_manager.update_button_states(self.button_manager)
            
            # Handle events before drawing buttons
            for event in self.event_manager.process_events():
                # Check for quit
                self.game_state, self.running = self.event_manager.handle_quit_event(event, self.game_state)
                if not self.running:
                    break
                    
                # Handle keyboard events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.event_manager.can_click_buttons():
                            self.event_manager.reset_button_delay()
                            self.show_esc_popup()
                
                # Handle button clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Get all battle buttons
                    battle_buttons = self.button_manager.get_buttons(GameState.BATTLE)
                    
                    # Check each button
                    for button_name, button in battle_buttons.items():
                        if self.event_manager.handle_button_click(event, button.rect, button.is_locked()):
                            if button_name == "Continue" and self.battle_manager.state == BattleState.MONSTER_DEFEATED:
                                # Get next monster when Continue is pressed
                                new_monster = self.current_quest.get_monster()
                                if new_monster:
                                    self.battle_manager.start_battle(new_monster)
                                    tooltip = Tooltip(f"Attack {self.battle_manager.monster.name} with your {self.hero.weapon.name}!", self.font)
                                else:
                                    # No more monsters in quest, return to quest screen
                                    self.game_state = GameState.QUEST
                                    self.running = False
                                break
                            else:
                                self._handle_button_click(button_name)
                            break
            
            # Draw battle buttons
            self.button_manager.draw_buttons(self.screen, GameState.BATTLE)
            
            # Draw battle log
            self._draw_battle_log()
            
            # Draw turn indicator only during combat
            if self.battle_manager.state != BattleState.MONSTER_DEFEATED:
                turn_text = "Monster's Turn" if self.battle_manager.turn == TurnState.MONSTER_TURN else "Your Turn"
                draw_text_centered(turn_text, self.font, Colors.BLACK, self.screen, 
                                GameConstants.SCREEN_WIDTH // 2, 10)
            
            # Draw tooltip if hovering over attack button
            if self.battle_manager.state == BattleState.HOME and self.battle_manager.turn == TurnState.HERO_TURN:
                mouse_pos = pygame.mouse.get_pos()
                attack_button = self.button_manager.get_button(GameState.BATTLE, "Attack")
                if attack_button and not attack_button.is_locked() and attack_button.rect.collidepoint(mouse_pos):
                    tooltip.draw(self.screen, mouse_pos[0] + 10, mouse_pos[1])

            self.update()

    def victory_screen(self) -> None:
        """Victory screen shown when all quests are completed."""
        self.running = True
        while self.running:
            self.screen.fill(Colors.WHITE)
            draw_text_centered("Victory!", self.font, Colors.GOLD, self.screen, 
                GameConstants.SCREEN_WIDTH // 2, GameConstants.SCREEN_HEIGHT // 2 - 100)
            draw_text_centered(f"{self.hero.name} has saved the village!", self.font, Colors.BLACK, 
                self.screen, GameConstants.SCREEN_WIDTH // 2, GameConstants.SCREEN_HEIGHT // 2 - 50)
            draw_text_centered("Press ESC to return to the main menu", self.font, Colors.BLACK, 
                self.screen, GameConstants.SCREEN_WIDTH // 2, GameConstants.SCREEN_HEIGHT // 2 + 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.WELCOME
                        self.running = False
            self.update()

    def defeat_screen(self) -> None:
        """Defeat screen shown when hero or village health reaches 0."""
        self.running = True
        defeat_reason = "The village has fallen!"
        
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
                        self.game_state = GameState.WELCOME
                        self.running = False
            self.update()

    def _handle_popup_events(self, event) -> str:
        """Handle events when a popup is active."""
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

    def _handle_keyboard_events(self, event) -> str:
        """Handle keyboard events."""
        if event.type == pygame.KEYDOWN:
            if self.key_actions and event.key in self.key_actions:
                if self.game_state != GameState.WELCOME:
                    if self.key_actions[event.key] == "escape":
                        self.show_esc_popup()
                    else:
                        return self.key_actions[event.key]
            elif event.unicode and len(event.unicode) == 1 and event.unicode.isprintable():
                return event.unicode
        return None

    def _handle_mouse_events(self, event) -> None:
        """Handle mouse events."""
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

    def events(self) -> str:
        """Handle all game events."""
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
        """Handle button clicks based on current game state and button name."""
        if self.game_state == GameState.WELCOME:
            if button_name == "New Game":
                self.game_state = GameState.NEW_GAME
                self.running = False
            elif button_name == "Load Game":
                self.load_game()
                self.game_state = GameState.MAIN_GAME
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
                self.game_state = GameState.WELCOME
                self.running = False
            elif button_name == "Create Hero":
                self.game_state = GameState.MAIN_GAME
                self.running = False
        
        elif self.game_state == GameState.MAIN_GAME:
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
                self.game_state = GameState.MAIN_GAME
                self.running = False
                
        elif self.game_state == GameState.QUEST:
            if button_name == "Back":
                self.game_state = GameState.MAIN_GAME
                self.running = False
            elif button_name == "Start":
                self.game_state = GameState.BATTLE
                self.running = False

        elif self.game_state == GameState.BATTLE:
            # Only process battle actions during hero's turn
            if self.battle_manager.turn == TurnState.HERO_TURN:
                if button_name == "Attack":
                    self.battle_manager.handle_attack(self.battle_manager.monster)
                elif button_name == "Defend":
                    self.battle_manager.handle_defend()
                elif button_name == "Use Potion":
                    self.battle_manager.handle_use_potion()
                elif button_name == "Flee":
                    if self.battle_manager.handle_flee():
                        self.battle_log.append(f"{self.hero.name} flees from battle!")
                        self.game_state = GameState.QUEST
                        self.running = False
            
            # Handle Retreat button regardless of turn
            if button_name == "Retreat":
                self.battle_log.append(f"{self.hero.name} retreats to regroup!")
                self.game_state = GameState.QUEST
                self.running = False