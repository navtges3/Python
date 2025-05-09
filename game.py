
import random
from hero import make_hero
from monster import get_monster
from items import *
from constants import *
from ui_helpers import *
from village import Village
import fileIO
import pygame
import math

def draw_hero_preview(surface, font, x:int, y:int, hero, button:Button, selected:bool=False) -> pygame.Rect:
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
        armor_text = f"Block: {hero.armor.block}\nDodge: {hero.armor.dodge}"
        draw_multiple_lines(armor_text, font, Colors.BLACK, surface, armor_border.x + 10, armor_border.y + font.get_linesize() + 25)
        pygame.draw.rect(surface, Colors.LIGHT_BLUE, armor_border, width=3, border_radius=10)

    # Name
    draw_text_centered(hero.name, font, Colors.BLACK, surface, hero_border.x + hero_border.width // 2, hero_border.y + font.get_linesize() // 2 + 10)

    # Image
    surface.blit(hero.image, (hero_border.x + 10, hero_border.y + font.get_linesize() + 10))
    if selected:
        pygame.draw.rect(surface, hero.border_color, hero_border, width=5, border_radius=10)
    else:
        pygame.draw.rect(surface, Colors.GRAY, hero_border, width=5, border_radius=10)
    return hero_border


class Game:
    pygame.init()

    font = pygame.font.Font(None, 24)
    
    buttons = {
        Game_State.WELCOME : {
            "New Game":     Button("New Game", (Game_Constants.SCREEN_WIDTH // 2 - 100, Game_Constants.SCREEN_HEIGHT // 2 - 20), (200, 50), font, Colors.BLACK, Colors.GREEN, Colors.LIGHT_GREEN),
            "Load Game":    Button("Load Game", (Game_Constants.SCREEN_WIDTH // 2 - 100, Game_Constants.SCREEN_HEIGHT // 2 + 40), (200, 50), font, Colors.BLACK, Colors.BLUE, Colors.LIGHT_BLUE),
            "Exit Game":    Button("Exit Game", (Game_Constants.SCREEN_WIDTH // 2 - 100, Game_Constants.SCREEN_HEIGHT // 2 + 100), (200, 50), font, Colors.BLACK, Colors.RED, Colors.LIGHT_RED),
        },
        Game_State.NEW_GAME : {
            "Knight":       Button("Knight", (10, 10), (Game_Constants.SCREEN_WIDTH // 2 - 20, Game_Constants.SCREEN_HEIGHT // 2 - 20), font, Colors.BLACK, Colors.WHITE, Colors.WHITE),
            "Assassin":     Button("Assassin", (Game_Constants.SCREEN_WIDTH // 2 + 10, 10), (Game_Constants.SCREEN_WIDTH // 2 - 20, Game_Constants.SCREEN_HEIGHT // 2 - 20), font, Colors.BLACK, Colors.WHITE, Colors.WHITE),
            "Back":         Button("Back", (Game_Constants.SCREEN_WIDTH // 2 - 210, Game_Constants.SCREEN_HEIGHT // 4 * 3), (200, 50), font, Colors.BLACK, Colors.RED, Colors.LIGHT_RED),
            "Create Hero":  Button("Create Hero", (Game_Constants.SCREEN_WIDTH // 2 + 10, Game_Constants.SCREEN_HEIGHT // 4 * 3), (250, 50), font, Colors.BLACK, Colors.GRAY, Colors.LIGHT_GRAY),
        },
        Game_State.MAIN_GAME : {
            "Menu":         Button("Menu", (0, Game_Constants.SCREEN_HEIGHT - Game_Constants.SCREEN_HEIGHT // 12), (Game_Constants.SCREEN_WIDTH // 4, Game_Constants.SCREEN_HEIGHT // 12), font, Colors.BLACK, Colors.RED, Colors.LIGHT_RED),
            "Inventory":    Button("Inventory", (Game_Constants.SCREEN_WIDTH // 4, Game_Constants.SCREEN_HEIGHT - Game_Constants.SCREEN_HEIGHT // 12), (Game_Constants.SCREEN_WIDTH // 4, Game_Constants.SCREEN_HEIGHT // 12), font, Colors.BLACK, Colors.BLUE, Colors.LIGHT_BLUE),
            "Battle":       Button("Battle", (Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT - Game_Constants.SCREEN_HEIGHT // 12), (Game_Constants.SCREEN_WIDTH // 4, Game_Constants.SCREEN_HEIGHT // 12), font, Colors.BLACK, Colors.RED, Colors.LIGHT_RED),
            "Shop":         Button("Shop", (Game_Constants.SCREEN_WIDTH // 4 * 3, Game_Constants.SCREEN_HEIGHT - Game_Constants.SCREEN_HEIGHT // 12), (Game_Constants.SCREEN_WIDTH // 4, Game_Constants.SCREEN_HEIGHT // 12), font, Colors.BLACK, Colors.YELLOW, Colors.LIGHT_YELLOW),
        },
        Game_State.BATTLE : {
            Battle_Action.HOME:{
                "Attack":       Button("Attack",        (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 0), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Colors.RED, Colors.LIGHT_RED),
                "Use Potion":   Button("Use Potion",    (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 1), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Colors.GREEN, Colors.LIGHT_GREEN),
                "Defend":       Button("Defend",        (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 2), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Colors.LIGHT_GRAY, Colors.LIGHT_GRAY),
                "Flee":         Button("Flee",          (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 3), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Colors.YELLOW, Colors.LIGHT_YELLOW),
            },
            Battle_Action.USE_ITEM:{
                "Health Potion": Button("Health Potion",    (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 0), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Colors.GREEN, Colors.LIGHT_GREEN),
                "Damage Potion": Button("Damage Potion",    (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 1), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Colors.RED, Colors.LIGHT_RED),
                "Block Potion":  Button("Block Potion",     (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 2), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Colors.BLUE, Colors.LIGHT_BLUE),
                "Back":          Button("Back",             (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 3), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Colors.RED, Colors.LIGHT_RED),
            },
            Battle_Action.MONSTER_DEFEATED:{
                "Continue Fighting":    Button("Continue Fighting", (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 0), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Colors.GREEN, Colors.LIGHT_GREEN),
                "Retreat":              Button("Retreat",           (Game_Constants.BATTLE_SCREEN_BUTTON_X, Game_Constants.BATTLE_SCREEN_BUTTON_Y + Game_Constants.BATTLE_SCREEN_BUTTON_INCREMENT * 1), (Game_Constants.BATTLE_SCREEN_BUTTON_WIDTH, Game_Constants.BATTLE_SCREEN_BUTTON_HEIGHT), font, Colors.BLACK, Colors.RED, Colors.LIGHT_RED),
            },
        },
        Game_State.SHOP : {
            "Purchase":     Button("Purchase", (Game_Constants.SCREEN_WIDTH // 2 + 15, Game_Constants.SCREEN_HEIGHT // 2 + 20), (250, 50), font, Colors.BLACK, Colors.LIGHT_GRAY, Colors.LIGHT_GRAY),
            "Leave":        Button("Leave", (Game_Constants.SCREEN_WIDTH // 2 + 15, Game_Constants.SCREEN_HEIGHT // 2 + 75), (250, 50), font, Colors.BLACK, Colors.RED, Colors.LIGHT_RED),
        },
        Game_State.PAUSE : {
            "Resume": Button("Resume", ((Game_Constants.SCREEN_WIDTH - Game_Constants.POPUP_WIDTH) // 2 + 50, (Game_Constants.SCREEN_HEIGHT - Game_Constants.POPUP_HEIGHT) // 2 + 50), (300, 50), font, Colors.BLACK, Colors.GREEN, Colors.LIGHT_GREEN),
            "Exit": Button("Exit", ((Game_Constants.SCREEN_WIDTH - Game_Constants.POPUP_WIDTH) // 2 + 50, (Game_Constants.SCREEN_HEIGHT - Game_Constants.POPUP_HEIGHT) // 2 + 120), (300, 50), font, Colors.BLACK, Colors.RED, Colors.LIGHT_RED),
        },
        Game_State.GAME_OVER : {},
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
        self.battle_state = Battle_Action.HOME
        self.battle_log = []
        self.hero = None
        self.monster = None
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
                            elif button_name == "Exit":
                                self.game_state = Game_State.WELCOME
                                self.popup_running = False
                                self.running = False
            else:
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
                                elif button_name == "Load Game" and self.hero is not None:
                                    self.game_state = Game_State.MAIN_GAME
                                    self.running = False
                                elif button_name == "Exit Game":
                                    self.game_state = Game_State.EXIT
                                    self.running = False
                    elif self.game_state == Game_State.NEW_GAME:
                        """Handle events for the new game screen."""
                        for button_name, button in self.buttons[Game_State.NEW_GAME].items():
                            if button.is_clicked(event):
                                if button_name == "Knight":
                                    return button_name
                                elif button_name == "Assassin":
                                    return button_name
                                elif button_name == "Back":
                                    self.game_state = Game_State.WELCOME
                                    self.running = False
                                elif button_name == "Create Hero":
                                    if self.hero is not None:
                                        self.monster = get_monster(self.hero.level)
                                        self.game_state = Game_State.MAIN_GAME
                                        self.running = False
                    elif self.game_state == Game_State.BATTLE:
                        """Handle events for the battle screen."""
                        if self.battle_state == Battle_Action.HOME:
                            for button_name, button in self.buttons[Game_State.BATTLE][Battle_Action.HOME].items():
                                if button.is_clicked(event):
                                    if button_name == "Attack":
                                        self.monster.take_damage(self.hero.weapon.damage + self.hero.potion_damage)
                                        self.battle_log.append(f"{self.hero.name} attacks {self.monster.name} with {self.hero.weapon.name} for {self.hero.weapon.damage + self.hero.potion_damage} damage.")
                                        if self.hero.potion_damage > 0:
                                            self.hero.potion_damage = 0
                                        if self.monster.alive:
                                            self.hero.take_damage(self.monster.damage)
                                            self.battle_log.append(f"{self.monster.name} attacks {self.hero.name} for {self.monster.damage} damage.")
                                        return button_name
                                    elif button_name == "Use Potion":
                                        print("use potion selected")
                                        if self.hero.has_potions():
                                            self.battle_state = Battle_Action.USE_ITEM
                                    elif button_name == "Defend":
                                        print("Use armor selected")
                                        if self.hero.armor is not None and self.hero.armor.is_available():
                                            self.hero.armor.use()
                                            self.battle_log.append(f"{self.hero.name} uses {self.hero.armor.name} for {self.hero.armor.duration} turns.")
                                        if self.monster.alive:
                                            self.hero.take_damage(self.monster.damage)
                                            self.battle_log.append(f"{self.monster.name} attacks {self.hero.name} for {self.monster.damage} damage.")
                                    elif button_name == "Flee":
                                        print("Flee selected")
                                        self.battle_log.append(f"{self.hero.name} flees from {self.monster.name}.")
                                        self.village.take_damage(self.monster.damage)
                                        self.game_state = Game_State.MAIN_GAME
                                        self.running = False
                        elif self.battle_state == Battle_Action.USE_ITEM:
                            for button_name, button in self.buttons[Game_State.BATTLE][Battle_Action.USE_ITEM].items():
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
                                        self.battle_state = Battle_Action.HOME
                        elif self.battle_state == Battle_Action.MONSTER_DEFEATED:
                            for button_name, button in self.buttons[Game_State.BATTLE][Battle_Action.MONSTER_DEFEATED].items():
                                if button.is_clicked(event):
                                    if button_name == "Continue Fighting":
                                        self.monster = get_monster(self.hero.level)
                                        self.battle_state = Battle_Action.HOME
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
                    if self.game_state != Game_State.BATTLE:
                        """Handle events for the main game screen."""
                        for button_name, button in self.buttons[Game_State.MAIN_GAME].items():
                            if button.is_clicked(event):
                                if button_name == "Menu":
                                    self.show_esc_popup()
                                elif button_name == "Inventory":
                                    pass
                                elif button_name == "Battle" and self.game_state != Game_State.BATTLE:
                                    self.game_state = Game_State.BATTLE
                                    self.running = False
                                elif button_name == "Shop" and self.game_state != Game_State.SHOP:
                                    self.game_state = Game_State.SHOP
                                    self.running = False
        return None

    def update(self) -> None:
        self.clock.tick(Game_Constants.FPS)
        pygame.display.update()

    def quit(self) -> None:
        """Quit the game."""
        pygame.quit()

    def show_esc_popup(self) -> None:
        """Show the escape popup menu."""
        self.popup_running = True
        exit_text = "Exit Game" if self.game_state == Game_State.NEW_GAME else "Save and Exit"

        self.buttons[Game_State.PAUSE]["Exit"].update_text(exit_text)

        while self.popup_running:
            draw_popup("Pause Menu", self.buttons[Game_State.PAUSE], self.screen, self.font)
            self.events()
            self.update()

    def welcome_screen(self) -> None:
        """Welcome screen with options to start a new game or load an existing game."""
        self.running = True
        self.hero = fileIO.load_game()
            
        while self.running:
            self.screen.fill(Colors.WHITE)

            draw_text_centered("Welcome to Village Defense!", self.font, Colors.BLACK, self.screen, Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT // 2 - 100)
            if self.hero is not None:
                self.buttons[Game_State.WELCOME]["Load Game"].button_color = Colors.BLUE
                self.buttons[Game_State.WELCOME]["Load Game"].hover_color = Colors.LIGHT_BLUE
            else:
                self.buttons[Game_State.WELCOME]["Load Game"].button_color = Colors.LIGHT_GRAY
                self.buttons[Game_State.WELCOME]["Load Game"].hover_color = Colors.LIGHT_GRAY

            for button in self.buttons[Game_State.WELCOME].values():
                button.draw(self.screen)

            self.events()
            self.update()

    def new_game_screen(self) -> None:
        """New game screen for creating a hero."""
        hero_name = ""
        hero_class = ""
        self.running = True

        knight_image = pygame.image.load(fileIO.resource_path("images/knight.png")).convert()
        knight_image = pygame.transform.scale(knight_image, (100, 100))

        assassin_image = pygame.image.load(fileIO.resource_path("images/assassin.png")).convert()
        assassin_image = pygame.transform.scale(assassin_image, (100, 100))

        knight = make_hero("Knight", "Knight", knight_image)
        assassin = make_hero("Assassin", "Assassin", assassin_image)


        while self.running:
            self.screen.fill(Colors.WHITE)
            create_button_color = Colors.GREEN if hero_name and hero_class else Colors.LIGHT_GRAY
            create_hover_color = Colors.LIGHT_GREEN if hero_name and hero_class else Colors.LIGHT_GRAY
            if create_button_color != self.buttons[Game_State.NEW_GAME]["Create Hero"].button_color:
                self.buttons[Game_State.NEW_GAME]["Create Hero"].button_color = create_button_color
                self.buttons[Game_State.NEW_GAME]["Create Hero"].hover_color = create_hover_color
            
            draw_hero_preview(self.screen, self.font, 10, 10, knight, self.buttons[Game_State.NEW_GAME]["Knight"], selected=hero_class == "Knight")
            draw_hero_preview(self.screen, self.font, Game_Constants.SCREEN_WIDTH // 2 + 10, 10, assassin, self.buttons[Game_State.NEW_GAME]["Assassin"], selected=hero_class == "Assassin")

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
            self.monster = get_monster(self.hero.level)

    def battle_screen(self) -> None:
        """Battle screen where the hero fights a monster."""
        self.running = True
        self.battle_state = Battle_Action.HOME

        if self.monster is None or not self.monster.alive:
            self.monster = get_monster(self.hero.level)
        
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

            if self.battle_state == Battle_Action.HOME:
                armor_button_color = Colors.LIGHT_BLUE if self.hero.armor is not None and self.hero.armor.is_available() else Colors.LIGHT_GRAY
                if armor_button_color != self.buttons[Game_State.BATTLE][self.battle_state]["Defend"].button_color:
                    self.buttons[Game_State.BATTLE][self.battle_state]["Defend"].button_color = armor_button_color
            elif self.battle_state == Battle_Action.USE_ITEM:
                for button in self.buttons[Game_State.BATTLE][self.battle_state].values():
                    if button.text == "Health Potion":
                        if self.hero.potion_bag["Health Potion"] > 0:
                            button.button_color = Colors.GREEN
                            button.hover_color = Colors.LIGHT_GREEN
                        else:
                            button.button_color = Colors.LIGHT_GRAY
                            button.hover_color = Colors.LIGHT_GRAY
                    elif button.text == "Damage Potion":
                        if self.hero.potion_bag["Damage Potion"] > 0:
                            button.button_color = Colors.RED
                            button.hover_color = Colors.LIGHT_RED
                        else:
                            button.button_color = Colors.LIGHT_GRAY
                            button.hover_color = Colors.LIGHT_GRAY
                    elif button.text == "Block Potion":
                        if self.hero.potion_bag["Block Potion"] > 0:
                            button.button_color = Colors.BLUE
                            button.hover_color = Colors.LIGHT_BLUE
                        else:
                            button.button_color = Colors.LIGHT_GRAY
                            button.hover_color = Colors.LIGHT_GRAY
            
            for button in self.buttons[Game_State.BATTLE][self.battle_state].values():
                button.draw(self.screen)

            self.events()
    
            if self.hero.alive and not self.monster.alive and self.battle_state != Battle_Action.MONSTER_DEFEATED:
                print("Monster defeated!")
                self.battle_log.append(f"{self.monster.name} has been defeated!")
                self.battle_log.append(f"{self.hero.name} gains {self.monster.experience} experience and 10 gold.")
                self.hero.gain_experience(self.monster.experience)
                self.hero.add_gold(10)
                self.battle_state = Battle_Action.MONSTER_DEFEATED
            elif not self.hero.alive:
                print("Hero defeated!")
                self.game_state = Game_State.GAME_OVER
                self.running = False
            self.update()

    def shop_screen(self) -> None:
        """Shop screen where the hero can buy items."""
        self.running = True
        purchase_button_colors = (Colors.GRAY, Colors.LIGHT_GRAY)
        card_price = 0
        
        while self.running:
            if self.village.shop.card_selected_key is None:
                purchase_button_colors = (Colors.GRAY, Colors.LIGHT_GRAY)
            else:
                purchase_button_colors = (Colors.GREEN, Colors.LIGHT_GREEN) if self.hero.gold >= card_price else (Colors.GRAY, Colors.LIGHT_GRAY)
            if purchase_button_colors != (self.buttons[Game_State.SHOP]["Purchase"].button_color, self.buttons[Game_State.SHOP]["Purchase"].hover_color):
                self.buttons[Game_State.SHOP]["Purchase"].button_color = purchase_button_colors[0]
                self.buttons[Game_State.SHOP]["Purchase"].hover_color = purchase_button_colors[1]

            self.screen.fill(Colors.WHITE)
            self.hero.draw(self.screen, self.font, 0, Game_Constants.SCREEN_HEIGHT // 2)
            self.village.shop.draw(self.screen)

            for button in self.buttons[Game_State.SHOP].values():
                button.draw(self.screen)
            for button in self.buttons[Game_State.MAIN_GAME].values():
                button.draw(self.screen)

            self.events()
            self.update()

    def main_game(self) -> None:
        """Main game screen."""
        self.running = True
        while self.running:
            self.screen.fill(Colors.WHITE)
            # Draw the village
            self.village.draw(self.screen, Game_Constants.SCREEN_WIDTH // 2 - 100, 50)

            # Draw the hero
            self.hero.draw(self.screen, self.font, 50, Game_Constants.SCREEN_HEIGHT // 2)

            # Draw Buttons
            for button in self.buttons[Game_State.MAIN_GAME].values():
                button.draw(self.screen)

            self.events()
            self.update()
    
    def game_over_screen(self) -> None:
        """Game over screen."""
        self.running = True
        while self.running:
            self.screen.fill(Colors.WHITE)
            draw_text_centered(f"{self.hero.name} has been slain!", self.font, Colors.BLACK, self.screen, Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT // 2 - 100)
            draw_text_centered("Game Over", self.font, Colors.BLACK, self.screen, Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT // 2 - 50)
            draw_text_centered("Press ESC to return to the main menu", self.font, Colors.BLACK, self.screen, Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT // 2 + 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = Game_State.EXIT
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = Game_State.WELCOME
                        self.running = False

            self.update()
