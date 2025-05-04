
import random
from hero import make_hero
from monster import get_monster
from items import *
from constants import *
from ui_helpers import *
import fileIO
import pygame
import math
           
def handle_popup_events(events:list[pygame.event.Event], buttons:dict[str, callable]=None, key_actions:dict[int, str]=None):
    """Handle events and return the action taken."""
    for event in events:
        if event.type == pygame.QUIT:
            return "quit"
        elif event.type == pygame.KEYDOWN:
            if key_actions and event.key in key_actions:
                return key_actions[event.key]
            else:
                if event.unicode and len(event.unicode) == 1 and event.unicode.isprintable():
                    return event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if buttons is not None:
                for button_name, button_data in buttons.items():
                    if button_data["rect"].collidepoint(event.pos):
                        return button_name
    return None

def draw_hero_preview(surface, font, x:int, y:int, hero, button:Button, selected:bool=False) -> pygame.Rect:
    """Draw the hero preview on the screen."""
    # Border 
    hero_border = button.rect.copy()

    # Weapon
    if hero.equipment is not None:
        equipment_border = pygame.Rect(hero_border.x + hero_border.width // 2, hero_border.y + 50, hero_border.width // 2, hero_border.height // 3)
        draw_text_centered(hero.equipment.name, font, Colors.BLACK, surface, equipment_border.x + equipment_border.width // 2, equipment_border.y + font.get_linesize() // 2 + 10)
        draw_multiple_lines(f"Damage {hero.equipment.damage}", font, Colors.BLACK, surface, equipment_border.x + 10, equipment_border.y + font.get_linesize() + 25)
        pygame.draw.rect(surface, Colors.LIGHT_RED, equipment_border, width=3, border_radius=10)
    # Armor
    if hero.protection is not None:
        protection_border = pygame.Rect(hero_border.x + hero_border.width // 2 , hero_border.y + hero_border.height // 3 + 50, hero_border.width // 2, hero_border.height // 3 * 2 - 50)
        draw_text_centered(hero.protection.name, font, Colors.BLACK, surface, protection_border.x + protection_border.width // 2, protection_border.y + font.get_linesize() // 2 + 10)
        protection_text = f"Block: {hero.protection.block}\nDodge: {hero.protection.dodge}"
        draw_multiple_lines(protection_text, font, Colors.BLACK, surface, protection_border.x + 10, protection_border.y + font.get_linesize() + 25)
        pygame.draw.rect(surface, Colors.LIGHT_BLUE, protection_border, width=3, border_radius=10)

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
            "Fighter":      Button("Fighter", (10, 10), (Game_Constants.SCREEN_WIDTH // 2 - 20, Game_Constants.SCREEN_HEIGHT // 2 - 20), font, Colors.BLACK, Colors.WHITE, Colors.WHITE),
            "Rogue":        Button("Rogue", (Game_Constants.SCREEN_WIDTH // 2 + 10, 10), (Game_Constants.SCREEN_WIDTH // 2 - 20, Game_Constants.SCREEN_HEIGHT // 2 - 20), font, Colors.BLACK, Colors.WHITE, Colors.WHITE),
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
            "Potion Card":  Button("Potion Card", (Game_Constants.SCREEN_WIDTH // 8, 25), (Game_Constants.SCREEN_WIDTH // 16 * 3, Game_Constants.SCREEN_HEIGHT // 3), font, Colors.BLACK, Colors.LIGHT_GRAY, Colors.GRAY),
            "Weapon Card":  Button("Weapon Card", (Game_Constants.SCREEN_WIDTH // 32 * 13, 25), (Game_Constants.SCREEN_WIDTH // 16 * 3, Game_Constants.SCREEN_HEIGHT // 3), font, Colors.BLACK, Colors.LIGHT_RED, Colors.RED),
            "Armor Card":   Button("Armor Card", (Game_Constants.SCREEN_WIDTH // 16 * 11, 25), (Game_Constants.SCREEN_WIDTH // 16 * 3, Game_Constants.SCREEN_HEIGHT // 3), font, Colors.BLACK, Colors.LIGHT_BLUE, Colors.BLUE),
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
        self.hero = None
        self.monster = None
        self.running = False

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

    def events(self, buttons:dict[str, Button]=None) -> str:
        if buttons is None:
            buttons = self.buttons[self.game_state]
        for event in pygame.event.get():
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
                if buttons is not None:
                    if self.game_state != Game_State.BATTLE:
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
                    for button_name, button in buttons.items():
                        if button.is_clicked(event):
                            return button_name
        return None

    def update(self) -> None:
        self.clock.tick(Game_Constants.FPS)
        pygame.display.update()

    def quit(self) -> None:
        """Quit the game."""
        pygame.quit()

    def show_esc_popup(self) -> None:
        """Show the escape popup menu."""
        popup_running = True
        popup_x = (Game_Constants.SCREEN_WIDTH - Game_Constants.POPUP_WIDTH) // 2
        popup_y = (Game_Constants.SCREEN_HEIGHT - Game_Constants.POPUP_HEIGHT) // 2
        exit_text = "Exit Game" if self.game_state == Game_State.NEW_GAME else "Save and Exit"

        buttons = {
            "Resume": Button("Resume", (popup_x + 50, popup_y + 50), (300, 50), self.font, Colors.BLACK, Colors.GREEN, Colors.LIGHT_GREEN),
            exit_text: Button(exit_text, (popup_x + 50, popup_y + 120), (300, 50), self.font, Colors.BLACK, Colors.RED, Colors.LIGHT_RED),
        }

        while popup_running:
            draw_popup("Pause Menu", buttons, self.screen, self.font)
            action = self.events(buttons)
            if action == "Resume":
                popup_running = False
            elif action == exit_text:
                if self.game_state != Game_State.NEW_GAME:
                    fileIO.save_game(self.hero)
                self.game_state = Game_State.WELCOME
                self.running = False
                popup_running = False
            elif action == "quit":
                self.game_state = Game_State.EXIT
                self.running = False
                popup_running = False
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
            action = self.events()
            if action == "quit":
                self.game_state = Game_State.EXIT
                self.running = False
            elif action == "New Game":
                print("New Game selected")
                self.game_state = Game_State.NEW_GAME
                self.running = False
            elif action == "Load Game" and self.hero is not None:
                print("Load Game selected")
                self.game_state = Game_State.MAIN_GAME
                self.running = False
            elif action == "Exit Game":
                print("Exit Game selected")
                self.game_state = Game_State.EXIT
                self.running = False
            self.update()

    def new_game_screen(self) -> None:
        """New game screen for creating a hero."""
        hero_name = ""
        hero_class = ""
        self.running = True

        hero_image = pygame.image.load(fileIO.resource_path("images/knight.jpg")).convert()
        hero_image = pygame.transform.scale(hero_image, (100, 100))

        fighter = make_hero("Fighter", "Fighter", hero_image)
        rogue = make_hero("Rogue", "Rogue", hero_image)


        while self.running:
            self.screen.fill(Colors.WHITE)
            create_button_color = Colors.GREEN if hero_name and hero_class else Colors.LIGHT_GRAY
            create_hover_color = Colors.LIGHT_GREEN if hero_name and hero_class else Colors.LIGHT_GRAY
            if create_button_color != self.buttons[Game_State.NEW_GAME]["Create Hero"].button_color:
                self.buttons[Game_State.NEW_GAME]["Create Hero"].button_color = create_button_color
                self.buttons[Game_State.NEW_GAME]["Create Hero"].hover_color = create_hover_color
            
            draw_hero_preview(self.screen, self.font, 10, 10, fighter, self.buttons[Game_State.NEW_GAME]["Fighter"], selected=hero_class == "Fighter")
            draw_hero_preview(self.screen, self.font, Game_Constants.SCREEN_WIDTH // 2 + 10, 10, rogue, self.buttons[Game_State.NEW_GAME]["Rogue"], selected=hero_class == "Rogue")
            draw_text(f"Hero Name: {hero_name}", self.font, Colors.BLACK, self.screen, Game_Constants.SCREEN_WIDTH // 2 - self.font.size("Hero Name: ")[0], Game_Constants.SCREEN_HEIGHT // 2 + self.font.get_linesize())
            draw_text(f"Hero Class: {hero_class}", self.font, Colors.BLACK, self.screen, Game_Constants.SCREEN_WIDTH // 2 - self.font.size("Hero Class: ")[0], Game_Constants.SCREEN_HEIGHT // 2 + self.font.get_linesize() * 2.5)

            for button in list(self.buttons[Game_State.NEW_GAME].values())[2:]:
                button.draw(self.screen)

            action = self.events(self.buttons[Game_State.NEW_GAME])
            if action is not None:
                if action == "Fighter":
                    print("Fighter selected")
                    hero_class = "Fighter"
                elif action == "Rogue":
                    print("Rogue selected")
                    hero_class = "Rogue"
                elif action == "Back":
                    print("Back selected")
                    self.game_state = Game_State.WELCOME
                    self.running = False
                elif action == "Create Hero" or action == "enter":
                    print("Create Hero selected")
                    if hero_name and hero_class:
                        self.hero = fighter if hero_class == "Fighter" else rogue
                        self.monster = get_monster(self.hero.level)
                        self.game_state = Game_State.MAIN_GAME
                        self.running = False
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

    def battle_screen(self) -> None:
        """Battle screen where the hero fights a monster."""
        self.running = True
        battle_log = []
        battle_state = Battle_Action.HOME

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
            for i, log_entry in enumerate(battle_log[-15:]):
                lines += draw_wrapped_text(log_entry, self.font, Colors.BLACK, self.screen, Game_Constants.BATTLE_SCREEN_LOG_X, Game_Constants.BATTLE_SCREEN_LOG_Y + (i + lines) * self.font.get_linesize(), Game_Constants.BATTLE_SCREEN_LOG_WIDTH)

            if battle_state == Battle_Action.HOME:
                protection_button_color = Colors.LIGHT_BLUE if self.hero.protection is not None and self.hero.protection.is_available() else Colors.LIGHT_GRAY
                if protection_button_color != self.buttons[Game_State.BATTLE][battle_state]["Defend"].button_color:
                    self.buttons[Game_State.BATTLE][battle_state]["Defend"].button_color = protection_button_color
            elif battle_state == Battle_Action.USE_ITEM:
                for button in self.buttons[Game_State.BATTLE][battle_state].values():
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
            
            for button in self.buttons[Game_State.BATTLE][battle_state].values():
                button.draw(self.screen)

            action = self.events(self.buttons[Game_State.BATTLE][battle_state])
            if action is not None:
                if action == "Attack":
                    print("weapon attack selected")
                    self.monster.take_damage(self.hero.equipment.damage + self.hero.potion_damage)
                    battle_log.append(f"{self.hero.name} attacks {self.monster.name} with {self.hero.equipment.name} for {self.hero.equipment.damage + self.hero.potion_damage} damage.")
                    if self.hero.potion_damage > 0:
                        self.hero.potion_damage = 0
                    if self.monster.alive:
                        self.hero.take_damage(self.monster.damage)
                        battle_log.append(f"{self.monster.name} attacks {self.hero.name} for {self.monster.damage} damage.")
                elif action == "Use Potion":
                    print("use potion selected")
                    if self.hero.has_potions():
                        battle_state = Battle_Action.USE_ITEM                            
                elif action == "Defend":
                    print("Use Protection selected")
                    if self.hero.protection is not None and self.hero.protection.is_available():
                        self.hero.protection.use()
                        battle_log.append(f"{self.hero.name} uses {self.hero.protection.name} for {self.hero.protection.duration} turns.")
                    if self.monster.alive:
                        self.hero.take_damage(self.monster.damage)
                        battle_log.append(f"{self.monster.name} attacks {self.hero.name} for {self.monster.damage} damage.")
                elif action == "Flee":
                    print("Flee selected")
                    self.game_state = Game_State.MAIN_GAME
                    self.running = False
                elif action == "Health Potion" and self.hero.potion_bag["Health Potion"] > 0:
                    print("Health Potion selected")
                    self.hero.use_potion("Health Potion")
                    battle_log.append(f"{self.hero.name} uses Health Potion.")
                elif action == "Damage Potion" and self.hero.potion_bag["Damage Potion"] > 0:
                    print("Damage Potion selected")
                    self.hero.use_potion("Damage Potion")
                    battle_log.append(f"{self.hero.name} uses Damage Potion.")
                elif action == "Block Potion" and self.hero.potion_bag["Block Potion"] > 0:
                    print("Block Potion selected")
                    self.hero.use_potion("Block Potion")
                    battle_log.append(f"{self.hero.name} uses Block Potion.")
                elif action == "Back":
                    print("Back selected")
                    battle_state = Battle_Action.HOME
                elif action == "Continue Fighting":
                    print("Continue Fighting selected")
                    self.monster = get_monster(self.hero.level)
                    battle_state = Battle_Action.HOME
                elif action == "Retreat":
                    print("Retreat selected")
                    self.game_state = Game_State.MAIN_GAME
                    self.running = False
    
            if self.hero.alive and not self.monster.alive and battle_state != Battle_Action.MONSTER_DEFEATED:
                print("Monster defeated!")
                battle_log.append(f"{self.monster.name} has been defeated!")
                battle_log.append(f"{self.hero.name} gains {self.monster.experience} experience and 10 gold.")
                self.hero.gain_experience(self.monster.experience)
                self.hero.add_gold(10)
                battle_state = Battle_Action.MONSTER_DEFEATED
            elif not self.hero.alive:
                print("Hero defeated!")
                self.game_state = Game_State.GAME_OVER
                self.running = False
            self.update()

    def shop_screen(self) -> None:
        """Shop screen where the hero can buy items."""
        card_selected = None
        self.running = True
        potion_name = random.choice(list(potion_dictionary.keys()))
        weapon_name = random.choice(list(weapon_dictionary.keys()))
        armor_name = random.choice(list(armor_dictionary.keys()))

        purchase_button_colors = (Colors.GRAY, Colors.LIGHT_GRAY)
        card_price = 0
        
        while self.running:
            if card_selected is not None:
                if card_selected == "Potion Card":
                    card_price = potion_dictionary[potion_name].value
                elif card_selected == "Weapon Card":
                    card_price = weapon_dictionary[weapon_name].value
                elif card_selected == "Armor Card":
                    card_price = armor_dictionary[armor_name].value
                else:
                    card_price = 0
            if card_selected is None:
                purchase_button_colors = (Colors.GRAY, Colors.LIGHT_GRAY)
            else:
                purchase_button_colors = (Colors.GREEN, Colors.LIGHT_GREEN) if self.hero.gold >= card_price else (Colors.GRAY, Colors.LIGHT_GRAY)
            if purchase_button_colors != (self.buttons[Game_State.SHOP]["Purchase"].button_color, self.buttons[Game_State.SHOP]["Purchase"].hover_color):
                self.buttons[Game_State.SHOP]["Purchase"].button_color = purchase_button_colors[0]
                self.buttons[Game_State.SHOP]["Purchase"].hover_color = purchase_button_colors[1]

            self.screen.fill(Colors.WHITE)
            self.hero.draw(self.screen, self.font, 0, Game_Constants.SCREEN_HEIGHT // 2)

            for buttons in list(self.buttons[Game_State.SHOP].values())[:2]:
                buttons.draw(self.screen)
            for buttons in self.buttons[Game_State.MAIN_GAME].values():
                buttons.draw(self.screen)

            potion_border = Colors.LIGHT_GREEN if card_selected == "Potion Card" else Colors.BLACK
            weapon_border = Colors.LIGHT_GREEN if card_selected == "Weapon Card" else Colors.BLACK
            armor_border = Colors.LIGHT_GREEN if card_selected == "Armor Card" else Colors.BLACK

            draw_item(potion_dictionary[potion_name], self.buttons[Game_State.SHOP]["Potion Card"], self.screen, potion_border)
            draw_item(weapon_dictionary[weapon_name], self.buttons[Game_State.SHOP]["Weapon Card"], self.screen, weapon_border)
            draw_item(armor_dictionary[armor_name], self.buttons[Game_State.SHOP]["Armor Card"], self.screen, armor_border)

            action = self.events()
            if action is not None:
                if action == "Potion Card":
                    print("Health Potion selected")
                    if card_selected == "Potion Card":
                        card_selected = None
                    else:
                        card_selected = "Potion Card"
                elif action == "Weapon Card":
                    print("Weapon Card selected")
                    if card_selected == "Weapon Card":
                        card_selected = None
                    else:
                        card_selected = "Weapon Card"
                elif action == "Armor Card":
                    print("Armor Card selected")
                    if card_selected == "Armor Card":
                        card_selected = None
                    else:
                        card_selected = "Armor Card"
                elif action == "Purchase" and card_selected is not None:
                    print("Purchase selected")
                    if self.hero.gold >= card_price:
                        if card_selected == "Potion Card":
                            self.hero.spend_gold(potion_dictionary[potion_name].value)
                            self.hero.add_potion(potion_name, 1)
                            potion_name = random.choice(list(potion_dictionary.keys()))
                        elif card_selected == "Weapon Card":
                            self.hero.spend_gold(weapon_dictionary[weapon_name].value)
                            self.hero.equipment = weapon_dictionary[weapon_name]
                            while weapon_name == self.hero.equipment.name:
                                weapon_name = random.choice(list(weapon_dictionary.keys()))
                        elif card_selected == "Armor Card":
                            self.hero.spend_gold(armor_dictionary[armor_name].value)
                            self.hero.protection = armor_dictionary[armor_name]
                            while armor_name == self.hero.protection.name:
                                armor_name = random.choice(list(armor_dictionary.keys()))
                elif action == "Leave":
                    print("Back to Main selected")
                    self.game_state = Game_State.MAIN_GAME
                    self.running = False
            self.update()
        if card_selected is not None:
            self.buttons[Game_State.SHOP][card_selected].button_color = Colors.LIGHT_GRAY

    def main_game(self) -> None:
        """Main game screen."""
        self.running = True
        while self.running:
            self.screen.fill(Colors.WHITE)
            self.hero.draw(self.screen, self.font, 0, 25)
            for button in self.buttons[Game_State.MAIN_GAME].values():
                button.draw(self.screen)
            draw_text_centered("Main Game", self.font, Colors.BLACK, self.screen, Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT // 2 + 50)

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
