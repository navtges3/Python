from battle_manager import *
from screen_manager import *
from button_manager import ButtonManager
from hero import *
from items import *
from constants import *
from quest import *
import fileIO
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
        self.monster = None
        self.current_quest = None
        self.running = False
        self.popup_running = False
        self.battle_manager = None

        
        # Initialize the mixer for music
        pygame.mixer.init()
        # Load and play background music
        pygame.mixer.music.load(fileIO.resource_path('music\\background_music.mp3'))  # Replace with your music file path
        pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # Play music in a loop

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((GameConstants.SCREEN_WIDTH, GameConstants.SCREEN_HEIGHT))
        pygame.display.set_caption('Village Defense')
        pygame.display.set_icon(pygame.image.load(fileIO.resource_path('icon.ico')))

        self.screen_manager = ScreenManager(self.screen, self.font)        # Load button sprite sheet
        button_sheet = pygame.image.load(fileIO.resource_path('images\\buttons\\button_sheet_0.png')).convert_alpha()
        self.button_manager = ButtonManager(self.font, button_sheet)
        
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
        if self.monster is not None:
            save_data.update({"monster": self.monster.to_dict(),})
        save_data.update({
            "game_volume": pygame.mixer.music.get_volume(),
            "current_quest": self.current_quest,  # Save the currently selected quest
        })

        # TODO save quests

        fileIO.save_game(save_data)

    def load_game(self) -> None:
        """Load the player's progress from the save file."""
        save_data = fileIO.load_game()
        if save_data is not None:
            # Load hero data
            if "hero" in save_data:
                self.hero = Hero(pygame.image.load(fileIO.resource_path(f"images/{save_data['hero']['class_name'].lower()}.png")).convert())
                self.hero.from_dict(save_data["hero"])
                self.hero.image = pygame.transform.scale(self.hero.image, (100, 100))
            else:
                print("No hero data found in save file.")
                return
            
            if "monster" in save_data:
                self.monster = Monster(save_data["monster"])
            else:
                self.monster = None

            pygame.mixer.music.set_volume(save_data.get("game_volume", 0.5))
            # Load current quest
            self.current_quest = save_data.get("current_quest", None)

            # Load game state
            self.game_state = GameState[save_data.get("game_state", "WELCOME")]

            # TODO load quests
        
    def show_esc_popup(self) -> None:
        """Show the escape popup menu."""
        self.popup_running = True
        exit_text = "Exit Game" if self.game_state == GameState.NEW_GAME else "Save and Exit"
        self.button_manager.get_button(GameState.PAUSE, "Exit").update_text(exit_text)

        while self.popup_running:
            pause_buttons = self.button_manager.get_buttons(GameState.PAUSE)
            self.screen_manager.draw_popup("Pause Menu", pause_buttons)
            self.events()
            self.update()
        
        if self.game_state == GameState.WELCOME and exit_text == "Save and Exit":
            self.save_game()

    def welcome_screen(self) -> None:
        """Welcome screen with options to start a new game or load an existing game."""
        self.running = True

        # Check for save file
        if fileIO.save_file_exists():
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

            # Draw all welcome screen buttons
            self.button_manager.draw_buttons(self.screen, GameState.WELCOME)

            self.events()
            self.update()

    def options_screen(self) -> None:
        """Options screen for adjusting game settings."""
        options_running = True
        music_volume = pygame.mixer.music.get_volume()
        
        while options_running:            # Draw the base popup
            options_buttons = self.button_manager.get_buttons(GameState.OPTIONS) 
            self.screen_manager.draw_popup("Options", options_buttons)
            
            # Draw volume slider
            volume_x = (GameConstants.SCREEN_WIDTH - GameConstants.POPUP_WIDTH) // 2 + 50
            volume_y = (GameConstants.SCREEN_HEIGHT - GameConstants.POPUP_HEIGHT) // 2 + 120
            
            # Draw volume label
            draw_text("Music Volume", self.font, Colors.BLACK, self.screen, volume_x, volume_y - 30)
            
            # Draw slider background
            pygame.draw.rect(self.screen, Colors.GRAY, (volume_x, volume_y, 300, 10))
            
            # Draw volume level
            pygame.draw.rect(self.screen, Colors.BLUE, (volume_x, volume_y, 300 * music_volume, 10))
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    options_running = False                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_button = self.button_manager.handle_click(GameState.OPTIONS, event.pos)
                    if clicked_button == "Back":
                        options_running = False
                elif event.type == pygame.MOUSEMOTION:
                    if event.buttons[0]:  # Left mouse button
                        mouse_x = event.pos[0]
                        if volume_x <= mouse_x <= volume_x + 300:
                            music_volume = (mouse_x - volume_x) / 300
                            pygame.mixer.music.set_volume(music_volume)
            
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

            # Enable/disable Create Hero button based on having both name and class
            create_hero_button = self.button_manager.get_button(GameState.NEW_GAME, "Create Hero")
            if hero_name and hero_class and create_hero_button.is_locked():
                create_hero_button.unlock()
            elif (not hero_name or not hero_class) and not create_hero_button.is_locked():
                create_hero_button.lock()

            self.button_manager.draw_buttons(self.screen, GameState.NEW_GAME)
            self.text_box.draw(self.screen)

            self.events()         
            self.update()

        if self.game_state == GameState.MAIN_GAME:
            self.hero = knight if hero_class == "Knight" else assassin
            # Use the text box's final text as the hero name
            self.hero.name = self.text_box.text

    def main_game(self) -> None:
        """Main game screen."""
        self.running = True
        while self.running:
            self.screen.fill(Colors.WHITE)            # Draw the hero
            self.hero.draw(self.screen, self.font, 0, GameConstants.SCREEN_HEIGHT // 2)

            # Draw Buttons
            self.button_manager.draw_buttons(self.screen, GameState.MAIN_GAME)

            self.events()
            self.update()

    def shop_screen(self) -> None:
        """Shop screen where the hero can buy items."""
        self.running = True
        
        while self.running:
            self.screen.fill(Colors.WHITE)
            
            # Draw shop buttons
            self.button_manager.draw_buttons(self.screen, GameState.SHOP)
            
            self.events()
            self.update()

    def quest_screen(self) -> None:

        self.running = True
        quest_selected = False
        while self.running:
            quest_button = self.button_manager.get_button(GameState.QUEST, "Quests")
            start_button = self.button_manager.get_button(GameState.QUEST, "Start")

            if quest_button.selected is not None and not quest_button.buttons[quest_button.selected].quest.is_complete():
                quest_selected = True
            else:
                quest_selected = False

            if quest_selected and start_button.is_locked():
                start_button.unlock()
            elif not quest_selected and not start_button.is_locked():
                start_button.lock()

            self.screen.fill(Colors.WHITE)
            
            # Draw all quest screen buttons
            self.button_manager.draw_buttons(self.screen, GameState.QUEST)
                
            self.events()
            self.update()

    def battle_screen(self) -> None:
        """Battle screen where the hero fights a monster."""
        self.running = True
        if self.battle_manager is None:
            self.battle_manager = BattleManager(self.hero, self.battle_log)
            quest_button = self.button_manager.get_button(GameState.QUEST, "Quests")
        if self.current_quest != quest_button.selected:
            self.current_quest = quest_button.selected
            self.monster = None

        if self.monster is None or not self.monster.is_alive():
            self.monster = quest_button.buttons[self.current_quest].quest.get_monster()
        
        tooltip = Tooltip(f"Attack {self.monster.name} with your {self.hero.weapon.name}!", self.font)

        while self.running:
            if self.battle_manager.state == BattleState.HOME:
                use_potion_button = self.button_manager.get_button(GameState.BATTLE, "Use Potion")
                if self.hero.has_potions() and use_potion_button.is_locked():
                    use_potion_button.unlock()
                elif not self.hero.has_potions() and not use_potion_button.is_locked():
                    use_potion_button.lock()
            elif self.battle_manager.state == BattleState.USE_ITEM:
                battle_buttons = self.button_manager.get_buttons(GameState.BATTLE)
                for button_name, button in battle_buttons.items():
                    if button_name == "Health Potion":
                        if self.hero.potion_bag["Health Potion"] > 0 and button.is_locked():
                            button.unlock()
                        elif self.hero.potion_bag["Health Potion"] == 0 and not button.is_locked():
                            button.lock()
                    elif button_name == "Damage Potion":
                        if self.hero.potion_bag["Damage Potion"] > 0 and button.is_locked():
                            button.unlock()
                        elif self.hero.potion_bag["Damage Potion"] == 0 and not button.is_locked():
                            button.lock()
                    elif button_name == "Block Potion":
                        if self.hero.potion_bag["Block Potion"] > 0 and button.is_locked():
                            button.unlock()
                        elif self.hero.potion_bag["Block Potion"] == 0 and not button.is_locked():
                            button.lock()
                            battle_buttons = self.button_manager.get_buttons(GameState.BATTLE)
            self.screen_manager.draw_battle_screen(self.hero, self.monster, self.battle_log, battle_buttons.values())
            
            if self.battle_manager.state == BattleState.HOME:
                mouse_pos = pygame.mouse.get_pos()
                attack_button = self.button_manager.get_button(GameState.BATTLE, "Attack")
                if attack_button and attack_button.rect.collidepoint(mouse_pos):
                    tooltip.draw(self.screen, mouse_pos[0] + 10, mouse_pos[1])

            self.events()
    
            if self.hero.is_alive() and not self.monster.is_alive() and self.battle_manager.state != BattleState.MONSTER_DEFEATED:
                print("Monster defeated!")
                self.battle_log.append(f"{self.monster.name} has been defeated!")
                self.battle_log.append(f"{self.hero.name} gains {self.monster.experience} experience and 10 gold.")
                self.hero.gain_experience(self.monster.experience)
                self.hero.add_gold(self.monster.gold)
                quest_button = self.button_manager.get_button(GameState.QUEST, "Quests")
                quest_button.buttons[self.current_quest].quest.slay_monster(self.monster)
                if quest_button.buttons[self.current_quest].quest.is_complete():
                    all_quests_complete = all(
                        quest_btn.quest.is_complete() for quest_btn in quest_button.buttons)
                    if all_quests_complete:
                        self.game_state = GameState.VICTORY
                        self.running = False
                    else:
                        self.draw_quest_complete(self.screen, self.buttons[GameState.QUEST]["Quests"].buttons[self.current_quest].quest)
                        self.game_state = GameState.QUEST
                        self.running = False
                else:
                    self.battle_manager.state = BattleState.MONSTER_DEFEATED
            elif not self.hero.is_alive():
                print("Hero defeated!")
                self.game_state = GameState.DEFEAT
                self.running = False
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

    def events(self) -> str:
        for event in pygame.event.get():
            if self.popup_running:
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.key_actions and event.key in self.key_actions:
                        if self.key_actions[event.key] == "escape" and self.game_state != GameState.WELCOME:
                            self.popup_running = False
                        else:
                            return self.key_actions[event.key]
                    elif event.unicode and len(event.unicode) == 1 and event.unicode.isprintable():
                        return event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_button = self.button_manager.handle_click(GameState.PAUSE, event.pos)
                    if clicked_button:
                        if clicked_button == "Resume":
                            self.popup_running = False
                        elif clicked_button == "Options":
                            self.options_screen()
                        elif clicked_button == "Exit":
                            self.game_state = GameState.WELCOME
                            self.popup_running = False
                            self.running = False
            else:
                if self.game_state == GameState.QUEST:
                    quest_button = self.button_manager.get_button(GameState.QUEST, "Quests")
                    quest_button.handle_event(event)

                # Handle text box input in NEW_GAME state
                if self.game_state == GameState.NEW_GAME:
                    self.text_box.handle_event(event)
                
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.key_actions and event.key in self.key_actions:
                        if self.key_actions[event.key] == "escape" and self.game_state != GameState.WELCOME:
                            self.show_esc_popup()
                        else:
                            return self.key_actions[event.key]
                    elif event.unicode and len(event.unicode) == 1 and event.unicode.isprintable():
                        return event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_button = self.button_manager.handle_click(self.game_state, event.pos)
                    if clicked_button:
                        self._handle_button_click(clicked_button)
                    elif self.game_state == GameState.NEW_GAME:
                        if self.text_box.rect.collidepoint(event.pos):
                            self.text_box.active = True
                        else:
                            self.text_box.active = False
                elif self.game_state == GameState.NEW_GAME and (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
                    self.text_box.handle_event(event)
                    if self.text_box.temp_text:
                        hero_name = self.text_box.temp_text
                elif self.game_state == GameState.NEW_GAME:
                    # Handle text box events
                    self.text_box.handle_event(event)
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
                self.options_screen()
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