import random
from hero import *
from items import *
from constants import *
from ui_helpers import *
from village import *
from quest import *
import fileIO
import pygame

def draw_hero_preview(surface:pygame.surface.Surface, font:pygame.font.Font, hero:Hero, button:Button) -> None:
    """Draw the hero preview on the screen."""
    # Border 
    hero_border = button.rect.copy()

    # Weapon
    if hero.weapon is not None:
        weapon_border = pygame.Rect(hero_border.x + hero_border.width // 2, hero_border.y + 50, hero_border.width // 2, hero_border.height // 3)
        draw_text_centered(hero.weapon.name, font, Colors.BLACK, surface, weapon_border.x + weapon_border.width // 2, weapon_border.y + font.get_linesize() // 2 + 10)
        draw_multiple_lines(f"Damage {hero.weapon.damage}", font, Colors.BLACK, surface, weapon_border.x + 10, weapon_border.y + font.get_linesize() + 25)
        pygame.draw.rect(surface, Colors.LIGHT_RED, weapon_border, width=3, border_radius=10)
    # Armor
    if hero.armor is not None:
        armor_border = pygame.Rect(hero_border.x + hero_border.width // 2 , hero_border.y + hero_border.height // 3 + 50, hero_border.width // 2, hero_border.height // 3 * 2 - 50)
        draw_text_centered(hero.armor.name, font, Colors.BLACK, surface, armor_border.x + armor_border.width // 2, armor_border.y + font.get_linesize() // 2 + 10)
        armor_text = f"Block: {hero.armor.block}\nBlock Chance: {hero.armor.block_chance:.0%}\nDodge: {hero.armor.dodge_chance:.0%}"
        draw_multiple_lines(armor_text, font, Colors.BLACK, surface, armor_border.x + 10, armor_border.y + font.get_linesize() + 25)
        pygame.draw.rect(surface, Colors.LIGHT_BLUE, armor_border, width=3, border_radius=10)

    # Name
    draw_text_centered(hero.name, font, Colors.BLACK, surface, hero_border.x + hero_border.width // 2, hero_border.y + font.get_linesize() // 2 + 10)

    # Image
    surface.blit(hero.image, (hero_border.x + 10, hero_border.y + font.get_linesize() + 10))
    if button.is_selected():
        pygame.draw.rect(surface, hero.border_color, hero_border, width=5, border_radius=10)
    else:
        pygame.draw.rect(surface, Colors.GRAY, hero_border, width=5, border_radius=10)


class Game:
    pygame.init()

    font = pygame.font.Font(None, 24)
    
    buttons = {
        Game_State.WELCOME : {
            "New Game":     Button("New Game", (Game_Constants.SCREEN_WIDTH // 2 - 100, Game_Constants.SCREEN_HEIGHT // 2 - 20), (200, 50), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
            "Load Game":    Button("Load Game", (Game_Constants.SCREEN_WIDTH // 2 - 100, Game_Constants.SCREEN_HEIGHT // 2 + 40), (200, 50), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
            "Options":      Button("Options", (Game_Constants.SCREEN_WIDTH // 2 - 100, Game_Constants.SCREEN_HEIGHT // 2 + 100), (200, 50), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
            "Exit Game":    Button("Exit Game", (Game_Constants.SCREEN_WIDTH // 2 - 100, Game_Constants.SCREEN_HEIGHT // 2 + 160), (200, 50), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
        },
        Game_State.NEW_GAME : {
            "Knight":       Button("Knight", (10, 10), (Game_Constants.SCREEN_WIDTH // 2 - 20, Game_Constants.SCREEN_HEIGHT // 2 - 20), font, Colors.BLACK),
            "Assassin":     Button("Assassin", (Game_Constants.SCREEN_WIDTH // 2 + 10, 10), (Game_Constants.SCREEN_WIDTH // 2 - 20, Game_Constants.SCREEN_HEIGHT // 2 - 20), font, Colors.BLACK),
            "Back":         Button("Back", (Game_Constants.SCREEN_WIDTH // 2 - 210, Game_Constants.SCREEN_HEIGHT // 4 * 3), (200, 50), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
            "Create Hero":  Button("Create Hero", (Game_Constants.SCREEN_WIDTH // 2 + 10, Game_Constants.SCREEN_HEIGHT // 4 * 3), (200, 50), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
        },
        Game_State.MAIN_GAME : {
            "Menu":         Button("Menu", (0, Game_Constants.SCREEN_HEIGHT - Game_Constants.SCREEN_HEIGHT // 12), (Game_Constants.SCREEN_WIDTH // 3, Game_Constants.SCREEN_HEIGHT // 12), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
            "Quest":        Button("Quest", (Game_Constants.SCREEN_WIDTH // 3, Game_Constants.SCREEN_HEIGHT - Game_Constants.SCREEN_HEIGHT // 12), (Game_Constants.SCREEN_WIDTH // 3, Game_Constants.SCREEN_HEIGHT // 12), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
            "Shop":         Button("Shop", (Game_Constants.SCREEN_WIDTH // 3 * 2, Game_Constants.SCREEN_HEIGHT - Game_Constants.SCREEN_HEIGHT // 12), (Game_Constants.SCREEN_WIDTH // 3, Game_Constants.SCREEN_HEIGHT // 12), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
        },
        Game_State.QUEST : {
            "Quests":       ScrollableArea(20, 20, Game_Constants.SCREEN_WIDTH - 100, Game_Constants.SCREEN_HEIGHT - 100, 100, font, Colors.BLACK),
            "Start":        Button("Start Quest",  (Game_Constants.SCREEN_WIDTH - Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH - 20, Game_Constants.SCREEN_HEIGHT - Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT - 20), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
            "Back":         Button("Back",         (20, Game_Constants.SCREEN_HEIGHT - Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT - 20), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
        },
        Game_State.BATTLE : {
            Battle_State.HOME:{
                "Attack":       Button("Attack",        (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 0), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
                "Use Potion":   Button("Use Potion",    (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 1), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
                "Defend":       Button("Defend",        (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 2), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
                "Flee":         Button("Flee",          (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 3), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
            },
            Battle_State.USE_ITEM:{
                "Health Potion": Button("Health Potion",    (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 0), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
                "Damage Potion": Button("Damage Potion",    (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 1), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
                "Block Potion":  Button("Block Potion",     (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 2), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
                "Back":          Button("Back",             (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 3), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
            },
            Battle_State.MONSTER_DEFEATED:{
                "Continue Fighting":    Button("Continue Fighting", (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 0), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
                "Retreat":              Button("Retreat",           (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 1), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
            },
        },
        Game_State.SHOP : {
            "Purchase":     Button("Purchase", (Game_Constants.SCREEN_WIDTH // 2 + 15, Game_Constants.SCREEN_HEIGHT // 2 + 20), (250, 50), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
            "Leave":        Button("Leave", (Game_Constants.SCREEN_WIDTH // 2 + 15, Game_Constants.SCREEN_HEIGHT // 2 + 75), (250, 50), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
        },
        Game_State.PAUSE : {
            "Resume":   Button("Resume", ((Game_Constants.SCREEN_WIDTH - Game_Constants.POPUP_WIDTH) // 2 + 50, (Game_Constants.SCREEN_HEIGHT - Game_Constants.POPUP_HEIGHT) // 2 + 50), (300, 50), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
            "Options":  Button("Options", ((Game_Constants.SCREEN_WIDTH - Game_Constants.POPUP_WIDTH) // 2 + 50, (Game_Constants.SCREEN_HEIGHT - Game_Constants.POPUP_HEIGHT) // 2 + 120), (300, 50), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
            "Exit":     Button("Exit", ((Game_Constants.SCREEN_WIDTH - Game_Constants.POPUP_WIDTH) // 2 + 50, (Game_Constants.SCREEN_HEIGHT - Game_Constants.POPUP_HEIGHT) // 2 + 190), (300, 50), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
        },
        Game_State.OPTIONS : {
            "Back": Button("Back", ((Game_Constants.SCREEN_WIDTH - Game_Constants.POPUP_WIDTH) // 2 + 50, (Game_Constants.SCREEN_HEIGHT - Game_Constants.POPUP_HEIGHT) // 2 + 190), (300, 50), font, Colors.BLACK, Game_Constants.BUTTON_IMAGE_PATH, Game_Constants.HOVER_IMAGE_PATH),
        },
        Game_State.EXIT : {},
    }
    key_actions = {
        pygame.K_ESCAPE: "escape",
        pygame.K_BACKSPACE: "backspace",
        pygame.K_RETURN: "enter",
        pygame.K_DELETE: "delete",
        pygame.K_TAB: "tab",
    }

    """Class to manage different game screens."""
    def __init__(self) -> None:
        self.game_state = Game_State.WELCOME
        self.battle_state = Battle_State.HOME
        self.battle_log = []
        self.hero = None
        self.monster = None
        self.current_quest = None
        self.running = False
        self.popup_running = False
        self.village = Village("Village", 1000, self.font)
        
        # Initialize the mixer for music
        pygame.mixer.init()
        # Load and play background music
        pygame.mixer.music.load(fileIO.resource_path("music\\background_music.mp3"))  # Replace with your music file path
        pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # Play music in a loop

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((Game_Constants.SCREEN_WIDTH, Game_Constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Village Defense")
        pygame.display.set_icon(pygame.image.load(fileIO.resource_path("icon.ico")))

        for state in self.buttons:
            if isinstance(self.buttons[state], dict):
                for button in self.buttons[state].values():
                    if isinstance(button, Button):
                        button.load_background()
                    elif isinstance(button, dict):
                        for b in button.values():
                            if isinstance(b, Button):
                                b.load_background()
            elif isinstance(self.buttons[state], Button):
                self.buttons[state].load_background()

        for quest in quest_list:
            self.buttons[Game_State.QUEST]["Quests"].add_button(
                QuestButton(
                    quest,
                    (20, 20),
                    (Game_Constants.SCREEN_WIDTH - 150, 100),
                    self.font,
                    Colors.BLACK
                ))
        
        for button in self.buttons[Game_State.QUEST]["Quests"].buttons:
            button.load_background()

        
        
    def update(self) -> None:
        self.clock.tick(Game_Constants.FPS)
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
            "game_state": self.game_state.name,  # Save the current game state
            "village": {
                "name": self.village.name,
                "health": self.village.health,
            },  # Save village data
            "quests": [
                {
                    "name": quest_button.quest.name,
                    "monsters_slain": quest_button.quest.monsters_slain,
                }
                for quest_button in self.buttons[Game_State.QUEST]["Quests"].buttons
            ],  # Save quest progress
        })
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
            self.game_state = Game_State[save_data.get("game_state", "WELCOME")]

            # Load village data
            if "village" in save_data:
                self.village.name = save_data["village"].get("name", "Village")
                self.village.health = save_data["village"].get("health", 1000)

            # Load quest progress
            if "quests" in save_data:
                for quest_data in save_data["quests"]:
                    for quest_button in self.buttons[Game_State.QUEST]["Quests"].buttons:
                        if quest_button.quest.name == quest_data["name"]:
                            quest_button.quest.monsters_slain = quest_data["monsters_slain"]
        
    def show_esc_popup(self) -> None:
        """Show the escape popup menu."""
        self.popup_running = True
        exit_text = "Exit Game" if self.game_state == Game_State.NEW_GAME else "Save and Exit"

        self.buttons[Game_State.PAUSE]["Exit"].update_text(exit_text)

        while self.popup_running:
            draw_popup("Pause Menu", self.buttons[Game_State.PAUSE], self.screen, self.font)
            self.events()
            self.update()
        
        if self.game_state == Game_State.WELCOME and exit_text == "Save and Exit":
            self.save_game()

    def draw_quest_complete(self, surface, quest):
        """Draw a quest completion popup."""
        # Create temporary buttons for the popup
        popup_buttons = {
            "Claim Reward": Button(
                f"Claim {quest.reward.name}",
                ((Game_Constants.SCREEN_WIDTH - Game_Constants.POPUP_WIDTH) // 2 + 50, 
                (Game_Constants.SCREEN_HEIGHT - Game_Constants.POPUP_HEIGHT) // 2 + 50),
                (300, 50),
                self.font,
                Colors.BLACK,
                Game_Constants.BUTTON_IMAGE_PATH,
                Game_Constants.HOVER_IMAGE_PATH
            )
        }
        
        # Draw the popup
        draw_popup("Quest Complete!", popup_buttons, surface, self.font)
        
        # Handle the button click
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if popup_buttons["Claim Reward"].is_clicked(event):
                        self.hero.add_item(quest.reward)
                        running = False
            self.update()

    def welcome_screen(self) -> None:
        """Welcome screen with options to start a new game or load an existing game."""
        self.running = True

        if fileIO.save_file_exists():
            self.buttons[Game_State.WELCOME]["Load Game"].unlock()
        else:
            self.buttons[Game_State.WELCOME]["Load Game"].lock()
            
        while self.running:
            self.screen.fill(Colors.WHITE)

            draw_text_centered("Welcome to Village Defense!", self.font, Colors.BLACK, self.screen, Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT // 2 - 100)

            for button in self.buttons[Game_State.WELCOME].values():
                button.draw(self.screen)

            self.events()
            self.update()

    def options_screen(self) -> None:
        """Options screen for adjusting game settings."""
        options_running = True
        music_volume = pygame.mixer.music.get_volume()
        
        while options_running:
            # Draw the base popup
            draw_popup("Options", self.buttons[Game_State.OPTIONS], self.screen, self.font)
            
            # Draw volume slider
            volume_x = (Game_Constants.SCREEN_WIDTH - Game_Constants.POPUP_WIDTH) // 2 + 50
            volume_y = (Game_Constants.SCREEN_HEIGHT - Game_Constants.POPUP_HEIGHT) // 2 + 120
            
            # Draw volume label
            draw_text("Music Volume", self.font, Colors.BLACK, self.screen, volume_x, volume_y - 30)
            
            # Draw slider background
            pygame.draw.rect(self.screen, Colors.GRAY, (volume_x, volume_y, 300, 10))
            
            # Draw volume level
            pygame.draw.rect(self.screen, Colors.BLUE, (volume_x, volume_y, 300 * music_volume, 10))
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = Game_State.EXIT
                    options_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button_name, button in self.buttons[Game_State.OPTIONS].items():
                        if button.is_clicked(event):
                            if button_name == "Back":
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
        hero_name = ""
        hero_class = ""
        self.running = True        

        knight = make_hero("Knight", "Knight")
        assassin = make_hero("Assassin", "Assassin")

        while self.running:
            if self.buttons[Game_State.NEW_GAME]["Knight"].is_selected():
                hero_class = "Knight"
            elif self.buttons[Game_State.NEW_GAME]["Assassin"].is_selected():
                hero_class = "Assassin"
            else:
                hero_class = ""
            
            if hero_class and hero_name:
                self.buttons[Game_State.NEW_GAME]["Create Hero"].unlock()
            else:
                self.buttons[Game_State.NEW_GAME]["Create Hero"].lock()

            self.screen.fill(Colors.WHITE)
            
            draw_hero_preview(self.screen, self.font, knight, self.buttons[Game_State.NEW_GAME]["Knight"])
            draw_hero_preview(self.screen, self.font, assassin, self.buttons[Game_State.NEW_GAME]["Assassin"])

            draw_text(f"Hero Name: {hero_name}", self.font, Colors.BLACK, self.screen, Game_Constants.SCREEN_WIDTH // 2 - self.font.size("Hero Name: ")[0], Game_Constants.SCREEN_HEIGHT // 2 + self.font.get_linesize())
            draw_text(f"Hero Class: {hero_class}", self.font, Colors.BLACK, self.screen, Game_Constants.SCREEN_WIDTH // 2 - self.font.size("Hero Class: ")[0], Game_Constants.SCREEN_HEIGHT // 2 + self.font.get_linesize() * 2.5)

            for button in list(self.buttons[Game_State.NEW_GAME].values())[2:]:
                button.draw(self.screen)

            action = self.events()
            if action is not None:
                if action == "Knight":
                    print("Knight selected")
                    hero_class = "Knight"
                elif action == "Assassin":
                    print("Assassin selected")
                    hero_class = "Assassin"
                elif action == "backspace":
                    hero_name = hero_name[:-1]
                elif action == "delete":
                    hero_name = ""
                elif action == "tab":
                    hero_name += "   "
                elif action and len(action) == 1 and action.isprintable():
                    if len(hero_name) < 20:
                        hero_name += action
            self.update()
        if self.game_state == Game_State.MAIN_GAME:
            self.hero = knight if hero_class == "Knight" else assassin
            self.hero.name = hero_name

    def main_game(self) -> None:
        """Main game screen."""
        self.running = True
        while self.running:
            self.screen.fill(Colors.WHITE)
            # Draw the village
            self.village.draw(self.screen, Game_Constants.SCREEN_WIDTH // 2 - 100, 50)

            # Draw the hero
            self.hero.draw(self.screen, self.font, 0, Game_Constants.SCREEN_HEIGHT // 2)

            # Draw Buttons
            for button in self.buttons[Game_State.MAIN_GAME].values():
                button.draw(self.screen)

            self.events()
            self.update()

    def shop_screen(self) -> None:
        """Shop screen where the hero can buy items."""
        self.running = True
        
        while self.running:
            if self.village.shop.can_buy_selected(self.hero) and self.buttons[Game_State.SHOP]["Purchase"].is_locked():
                self.buttons[Game_State.SHOP]["Purchase"].unlock()
            elif not self.village.shop.can_buy_selected(self.hero) and not self.buttons[Game_State.SHOP]["Purchase"].is_locked():
                self.buttons[Game_State.SHOP]["Purchase"].lock()
            
            self.screen.fill(Colors.WHITE)
            self.hero.draw(self.screen, self.font, 0, Game_Constants.SCREEN_HEIGHT // 2)
            self.village.shop.draw(self.screen)

            for button in self.buttons[Game_State.SHOP].values():
                button.draw(self.screen)

            self.events()
            self.update()

    def quest_screen(self) -> None:

        self.running = True
        quest_selected = False
        
        while self.running:

            if self.buttons[Game_State.QUEST]["Quests"].selected is not None and not self.buttons[Game_State.QUEST]["Quests"].buttons[self.buttons[Game_State.QUEST]["Quests"].selected].quest.is_complete():
                quest_selected = True
            else:
                quest_selected = False

            if quest_selected and self.buttons[Game_State.QUEST]["Start"].is_locked():
                self.buttons[Game_State.QUEST]["Start"].unlock()
            elif not quest_selected and not self.buttons[Game_State.QUEST]["Start"].is_locked():
                self.buttons[Game_State.QUEST]["Start"].lock()

            self.screen.fill(Colors.WHITE)
            self.buttons[Game_State.QUEST]["Quests"].draw(self.screen)
            for button in list(self.buttons[Game_State.QUEST].values())[1:]:
                button.draw(self.screen)
                
            self.events()
            self.update()

    def battle_screen(self) -> None:
        """Battle screen where the hero fights a monster."""
        self.running = True
        self.battle_state = Battle_State.HOME

        tooltip = Tooltip(f"Attack {self.monster.name} with your {self.hero.weapon.name}!", self.font)

        if self.current_quest != self.buttons[Game_State.QUEST]["Quests"].selected:
            self.current_quest = self.buttons[Game_State.QUEST]["Quests"].selected
            self.monster = None

        if self.monster is None or not self.monster.is_alive():
            self.monster = self.buttons[Game_State.QUEST]["Quests"].buttons[self.current_quest].quest.get_monster()

        button_border = pygame.Rect(Game_Constants.BATTLE_SCREEN_BUTTON_BORDER_X, Game_Constants.BATTLE_SCREEN_BUTTON_BORDER_Y, Game_Constants.BATTLE_SCREEN_BUTTON_BORDER_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_BORDER_HEIGHT)
        log_border = pygame.Rect(Game_Constants.BATTLE_SCREEN_LOG_BORDER_X, Game_Constants.BATTLE_SCREEN_LOG_BORDER_Y, Game_Constants.BATTLE_SCREEN_LOG_BORDER_WIDTH, Game_Constants.BATTLE_SCREEN_LOG_BORDER_HEIGHT)

        while self.running:
            self.screen.fill(Colors.WHITE)
            self.hero.draw(self.screen, self.font, 0,  25)
            self.monster.draw(self.screen, self.font, Game_Constants.SCREEN_WIDTH // 2, 25)

            pygame.draw.rect(self.screen, Colors.BLACK, button_border, width=5, border_radius=10)
            pygame.draw.rect(self.screen, Colors.BLACK, log_border, width=5, border_radius=10)

            lines = 0
            for i, log_entry in enumerate(self.battle_log[-15:]):
                lines += draw_wrapped_text(log_entry, self.font, Colors.BLACK, self.screen, Game_Constants.BATTLE_SCREEN_LOG_X, Game_Constants.BATTLE_SCREEN_LOG_Y + (i + lines) * self.font.get_linesize(), Game_Constants.BATTLE_SCREEN_LOG_WIDTH)

            if self.battle_state == Battle_State.HOME:
                if self.hero.has_potions() and self.buttons[Game_State.BATTLE][Battle_State.HOME]["Use Potion"].is_locked():
                    self.buttons[Game_State.BATTLE][Battle_State.HOME]["Use Potion"].unlock()
                elif not self.hero.has_potions() and not self.buttons[Game_State.BATTLE][Battle_State.HOME]["Use Potion"].is_locked():
                    self.buttons[Game_State.BATTLE][Battle_State.HOME]["Use Potion"].lock()

            elif self.battle_state == Battle_State.USE_ITEM:
                for button in self.buttons[Game_State.BATTLE][self.battle_state].values():
                    if button.text == "Health Potion":
                        if self.hero.potion_bag["Health Potion"] > 0 and button.is_locked():
                            button.unlock()
                        elif self.hero.potion_bag["Health Potion"] == 0 and not button.is_locked():
                            button.lock()
                    elif button.text == "Damage Potion":
                        if self.hero.potion_bag["Damage Potion"] > 0 and button.is_locked():
                            button.unlock()
                        elif self.hero.potion_bag["Damage Potion"] == 0 and not button.is_locked():
                            button.lock()
                    elif button.text == "Block Potion":
                        if self.hero.potion_bag["Block Potion"] > 0 and button.is_locked():
                            button.unlock()
                        elif self.hero.potion_bag["Block Potion"] == 0 and not button.is_locked():
                            button.lock()
            
            for button in self.buttons[Game_State.BATTLE][self.battle_state].values():
                button.draw(self.screen)

            if self.battle_state == Battle_State.HOME:
                mouse_pos = pygame.mouse.get_pos()
                if self.buttons[Game_State.BATTLE][Battle_State.HOME]["Attack"].rect.collidepoint(mouse_pos):
                    tooltip.draw(self.screen, mouse_pos[0] + 10, mouse_pos[1])

            self.events()
    
            if self.hero.is_alive() and not self.monster.is_alive() and self.battle_state != Battle_State.MONSTER_DEFEATED:
                ("Monster defeated!")
                self.battle_log.append(f"{self.monster.name} has been defeated!")
                self.battle_log.append(f"{self.hero.name} gains {self.monster.experience} experience and 10 gold.")
                self.hero.gain_experience(self.monster.experience)
                self.hero.add_gold(self.monster.gold)
                self.buttons[Game_State.QUEST]["Quests"].buttons[self.current_quest].quest.slay_monster(self.monster)
                if self.buttons[Game_State.QUEST]["Quests"].buttons[self.current_quest].quest.is_complete():
                    all_quests_complete = all(
                        quest_button.quest.is_complete() for quest_button in self.buttons[Game_State.QUEST]["Quests"].buttons)
                    if all_quests_complete:
                        self.game_state = Game_State.VICTORY
                        self.running = False
                    else:
                        self.draw_quest_complete(self.screen, self.buttons[Game_State.QUEST]["Quests"].buttons[self.current_quest].quest)
                        self.game_state = Game_State.QUEST
                        self.running = False
                else:
                    self.battle_state = Battle_State.MONSTER_DEFEATED
            elif not self.hero.is_alive():
                print("Hero defeated!")
                self.game_state = Game_State.DEFEAT
                self.running = False
            self.update()    
    
    def victory_screen(self) -> None:
        """Victory screen shown when all quests are completed."""
        self.running = True
        while self.running:
            self.screen.fill(Colors.WHITE)
            draw_text_centered("Victory!", self.font, Colors.GOLD, self.screen, 
                Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT // 2 - 100)
            draw_text_centered(f"{self.hero.name} has saved the village!", self.font, Colors.BLACK, 
                self.screen, Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT // 2 - 50)
            draw_text_centered("Press ESC to return to the main menu", self.font, Colors.BLACK, 
                self.screen, Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT // 2 + 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = Game_State.EXIT
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = Game_State.WELCOME
                        self.running = False
            self.update()

    def defeat_screen(self) -> None:
        """Defeat screen shown when hero or village health reaches 0."""
        self.running = True
        defeat_reason = "The village has fallen!" if self.village.health <= 0 else f"{self.hero.name} has been slain!"
        
        while self.running:
            self.screen.fill(Colors.WHITE)
            draw_text_centered(defeat_reason, self.font, Colors.RED, self.screen, 
                Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT // 2 - 100)
            draw_text_centered("Game Over", self.font, Colors.BLACK, self.screen, 
                Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT // 2 - 50)
            draw_text_centered("Press ESC to return to the main menu", self.font, Colors.BLACK, 
                self.screen, Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT // 2 + 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = Game_State.EXIT
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = Game_State.WELCOME
                        self.running = False
            self.update()

    def events(self) -> str:
        for event in pygame.event.get():
            if self.popup_running:
                if event.type == pygame.QUIT:
                    self.game_state = Game_State.EXIT
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.key_actions and event.key in self.key_actions:
                        if self.key_actions[event.key] == "escape" and self.game_state != Game_State.WELCOME:
                            self.popup_running = False
                        else:
                            return self.key_actions[event.key]
                    else:
                        if event.unicode and len(event.unicode) == 1 and event.unicode.isprintable():
                            return event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button_name, button in self.buttons[Game_State.PAUSE].items():
                        if button.is_clicked(event):
                            if button_name == "Resume":
                                self.popup_running = False
                            elif button_name == "Options":
                                self.options_screen()
                            elif button_name == "Exit":
                                self.game_state = Game_State.WELCOME
                                self.popup_running = False
                                self.running = False
            else:
                if self.game_state == Game_State.QUEST:
                    self.buttons[Game_State.QUEST]["Quests"].handle_event(event)
                if event.type == pygame.QUIT:
                    self.game_state = Game_State.EXIT
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.key_actions and event.key in self.key_actions:
                        if self.key_actions[event.key] == "escape" and self.game_state != Game_State.WELCOME:
                            self.show_esc_popup()
                        else:
                            return self.key_actions[event.key]
                    else:
                        if event.unicode and len(event.unicode) == 1 and event.unicode.isprintable():
                            return event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_state == Game_State.WELCOME:
                        """Handle events for the welcome screen."""
                        for button_name, button in self.buttons[Game_State.WELCOME].items():
                            if button.is_clicked(event):
                                if button_name == "New Game":
                                    self.game_state = Game_State.NEW_GAME
                                    self.running = False
                                elif button_name == "Load Game" and not button.is_locked():
                                    self.load_game()
                                    self.game_state = Game_State.MAIN_GAME
                                    self.running = False
                                elif button_name == "Options":
                                    self.options_screen()
                                elif button_name == "Exit Game":
                                    self.game_state = Game_State.EXIT
                                    self.running = False
                    elif self.game_state == Game_State.NEW_GAME:
                        """Handle events for the new game screen."""
                        for button_name, button in self.buttons[Game_State.NEW_GAME].items():
                            if button.is_clicked(event):
                                if button_name == "Knight":
                                    button.select()
                                    self.buttons[Game_State.NEW_GAME]["Assassin"].deselect()
                                elif button_name == "Assassin":
                                    button.select()
                                    self.buttons[Game_State.NEW_GAME]["Knight"].deselect()
                                elif button_name == "Back":
                                    self.buttons[Game_State.NEW_GAME]["Assassin"].deselect()
                                    self.buttons[Game_State.NEW_GAME]["Knight"].deselect()
                                    self.game_state = Game_State.WELCOME
                                    self.running = False
                                elif button_name == "Create Hero":
                                    if not self.buttons[Game_State.NEW_GAME]["Create Hero"].is_locked():
                                        self.game_state = Game_State.MAIN_GAME
                                        self.running = False
                    elif self.game_state == Game_State.MAIN_GAME:
                        """Handle events for the main game screen."""
                        for button_name, button in self.buttons[Game_State.MAIN_GAME].items():
                            if button.is_clicked(event):
                                if button_name == "Menu":
                                    self.show_esc_popup()
                                elif button_name == "Quest":
                                    self.game_state = Game_State.QUEST
                                    self.running = False
                                elif button_name == "Shop":
                                    self.game_state = Game_State.SHOP
                                    self.running = False
                    elif self.game_state == Game_State.QUEST:
                        for button_name, button in self.buttons[Game_State.QUEST].items():
                            if button_name == "Quests":
                                continue
                            elif button.is_clicked(event):
                                if button_name == "Back":
                                    self.game_state = Game_State.MAIN_GAME
                                    self.running = False
                                elif button_name == "Start":
                                    self.game_state = Game_State.BATTLE
                                    self.running = False
                    elif self.game_state == Game_State.BATTLE:
                        """Handle events for the battle screen."""
                        if self.battle_state == Battle_State.HOME:
                            for button_name, button in self.buttons[Game_State.BATTLE][Battle_State.HOME].items():
                                if button.is_clicked(event):
                                    if button_name == "Attack":
                                        self.hero.attack(self.monster)
                                        self.battle_log.append(f"{self.hero.name} attacks {self.monster.name} with {self.hero.weapon.name} for {self.hero.weapon.damage + self.hero.potion_damage} damage.")
                                        if self.hero.potion_damage > 0:
                                            self.hero.potion_damage = 0
                                        if self.monster.is_alive():
                                            self.monster.attack(self.hero)
                                            self.battle_log.append(f"{self.monster.name} attacks {self.hero.name} for {self.monster.damage} damage.")
                                        return button_name
                                    elif button_name == "Use Potion":
                                        print("use potion selected")
                                        if self.hero.has_potions():
                                            self.battle_state = Battle_State.USE_ITEM
                                    elif button_name == "Defend":
                                        print("Use armor selected")
                                    elif button_name == "Flee":
                                        print("Flee selected")
                                        self.battle_log.append(f"{self.hero.name} flees from {self.monster.name}.")
                                        self.village.take_damage(self.monster.damage)
                                        self.game_state = Game_State.MAIN_GAME
                                        self.running = False
                        elif self.battle_state == Battle_State.USE_ITEM:
                            for button_name, button in self.buttons[Game_State.BATTLE][Battle_State.USE_ITEM].items():
                                if button.is_clicked(event):
                                    if button_name == "Health Potion":
                                        print("Health Potion selected")
                                        self.hero.use_potion("Health Potion")
                                        self.battle_log.append(f"{self.hero.name} uses Health Potion.")
                                    elif button_name == "Damage Potion":
                                        print("Damage Potion selected")
                                        self.hero.use_potion("Damage Potion")
                                        self.battle_log.append(f"{self.hero.name} uses Damage Potion.")
                                    elif button_name == "Block Potion":
                                        print("Block Potion selected")
                                        self.hero.use_potion("Block Potion")
                                        self.battle_log.append(f"{self.hero.name} uses Block Potion.")
                                    elif button_name == "Back":
                                        print("Back selected")
                                        self.battle_state = Battle_State.HOME
                        elif self.battle_state == Battle_State.MONSTER_DEFEATED:
                            for button_name, button in self.buttons[Game_State.BATTLE][Battle_State.MONSTER_DEFEATED].items():
                                if button.is_clicked(event):
                                    if button_name == "Continue Fighting":
                                        self.monster = self.buttons[Game_State.QUEST]["Quests"].buttons[self.buttons[Game_State.QUEST]["Quests"].selected].quest.get_monster()
                                        self.battle_state = Battle_State.HOME
                                    elif button_name == "Retreat":
                                        self.game_state = Game_State.MAIN_GAME
                                        self.running = False
                    elif self.game_state == Game_State.SHOP:
                        """Handle events for the shop screen."""
                        for button_name, button in self.village.shop.cards.items():
                            if button.is_clicked(event):
                                self.village.shop.card_selected(button_name)
                        for button_name, button in self.buttons[Game_State.SHOP].items():
                            if button.is_clicked(event):
                                if button_name == "Purchase":
                                    self.village.shop.buy_item(self.hero)
                                elif button_name == "Leave":
                                    self.game_state = Game_State.MAIN_GAME
                                    self.running = False
        return None