
import random
from hero import Hero, make_hero
from monster import Monster, get_monster
from items import *
from constants import *
import fileIO
import pygame
import math

# Set up the game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
POPUP_WIDTH = 400
POPUP_HEIGHT = 200

FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (211, 211, 211)
LIGHT_BLUE = (173, 216, 230)
LIGHT_RED = (255, 182, 193)
LIGHT_YELLOW = (255, 255, 224)
LIGHT_GREEN = (144, 238, 144)
GOLD = (255, 215, 0)

class Button:
    def __init__(self, text, pos, size, font:pygame.font, text_color, button_color, hover_color):
        self.text = text
        self.pos = pos
        self.size = size
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color

        self.rect = pygame.Rect(pos, size,)
        self.surface = self.font.render(self.text, True, self.text_color)

    def draw(self, screen, draw_text=True, border_color=BLACK) -> None:
        # Change color on hover
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect, border_radius=5)
        else:
            pygame.draw.rect(screen, self.button_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, border_color, self.rect, width=2, border_radius=5)

        # Center text on button
        if draw_text:
            text_rect = self.surface.get_rect(center=self.rect.center)
            screen.blit(self.surface, text_rect)

    def is_clicked(self, event):
        # Check if button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def draw_item(item:Item, button:Button, surface, border_color) -> None:
    """Draw an item on the screen."""
    button.draw(surface, False, border_color)
    draw_text(item.name, button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 10)
    if isinstance(item, Weapon):
        draw_text(f"Damage: {item.damage}", button.font, button.text_color,surface, button.pos[0] + 10, button.pos[1] + 40)
    elif isinstance(item, Armor):
        draw_text(f"Block: {item.block}", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 40)
        draw_text(f"Dodge: {item.dodge}", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 70)
        draw_text(f"Cooldown: {item.cooldown}", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 100)

    draw_text(f"Cost: {item.value}G", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 130)

def draw_text(text:str, font:pygame.font, color:tuple, surface, x:int, y:int) -> None:
    """Draw text on the screen at the specified position."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)

def draw_text_centered(text:str, font:pygame.font, color:tuple, surface, x:int, y:int) -> None:
    """Draw centered text on the screen at the specified position."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def draw_wrapped_text(text:str, font:pygame.font, color:tuple, surface, x:int, y:int, max_width:int) -> int:
    """Draw wrapped text on the screen at the specified position."""
    words = text.split(' ')
    wrapped_lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line)
            current_line = word
    if current_line:
        wrapped_lines.append(current_line)

    for i, line in enumerate(wrapped_lines):
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y + i * font.get_linesize()))
    return i

def draw_multiple_lines(text:str, font:pygame.font, color:tuple, surface, x:int, y:int) -> None:
    """Draw multiple lines of text on the screen at the specified position."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        draw_text(line, font, color, surface, x, y + i * 30)

def draw_health_bar(surface, x:int, y:int, width:int, height:int, health_percentage:float) -> None:
    """Draw a health bar on the screen."""
    if health_percentage < 0:
        health_percentage = 0
    elif health_percentage > 1:
        health_percentage = 1
    health_bar_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, RED, health_bar_rect)
    health_fill_rect = pygame.Rect(x, y, width * health_percentage, height)
    pygame.draw.rect(surface, GREEN, health_fill_rect)

def draw_hero(hero:Hero, surface, font,) -> None:
    """Draw the hero's information on the surface."""

    # Border
    hero_border = pygame.Rect(0, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    pygame.draw.rect(surface, BLUE, hero_border, width=5, border_radius=10)

    # Portrait
    hero_image = pygame.image.load(fileIO.resource_path(f"images\\{hero.image}")).convert()
    hero_image = pygame.transform.scale(hero_image, (100, 100))
    surface.blit(hero_image, (hero_border.x + 10, hero_border.y + 10))

    # Health Bar
    health_bar_width = 90
    health_bar_height = 10
    health_bar_x = hero_border.x + 15
    health_bar_y = hero_border.y + hero_image.get_height() + 15
    health_percentage = hero.health / hero.max_health
    draw_health_bar(surface, health_bar_x, health_bar_y, health_bar_width, health_bar_height, health_percentage)

    # Hero Stats
    hero_text = f"{hero.name}\nLevel: {hero.level}\nExp: {hero.experience}\nGold: {hero.gold}"
    draw_multiple_lines(hero_text, font, BLACK, surface, hero_border.x + hero_image.get_width() + 10, hero_border.y + 10)

    potion_text = f"Potion Bag:\n -Health Potion: {hero.potion_bag['Health Potion']}\n -Damage Potion: {hero.potion_bag['Damage Potion']}\n -Block Potion: {hero.potion_bag['Block Potion']}"
    draw_multiple_lines(potion_text, font, BLACK, surface, hero_border.x + hero_border.width // 2 + 10, hero_border.y + 10)

    # Draw the hero's weapon and protection
    if hero.equipment is not None:
        equipment_border = pygame.Rect(hero_border.x + 10, hero_border.y + 140, hero_border.width // 2 - 15, hero_border.height - 150)
        pygame.draw.rect(surface, LIGHT_RED, equipment_border, width=2, border_radius=10)
        equipment_text = f"{hero.equipment.name}\nDamage {hero.equipment.damage}"
        draw_multiple_lines(equipment_text, font, BLACK, surface, equipment_border.x + 5, equipment_border.y + 5)
    if hero.protection is not None:
        protection_border = pygame.Rect(hero_border.x + hero_border.width // 2 + 5, hero_border.y + 140, hero_border.width // 2 - 15, hero_border.height - 150)
        pygame.draw.rect(surface, LIGHT_BLUE, protection_border, width=2, border_radius=10)
        protection_text = f"{hero.protection.name}\nBlock: {hero.protection.block}\nDodge: {hero.protection.dodge}"
        draw_multiple_lines(protection_text, font, BLACK, surface, protection_border.x + 5, protection_border.y + 5)

def draw_monster(monster:Monster, surface, font, x:int, y:int) -> None:
    """Draw the monster's information on the screen."""
    monster_text = f"{monster.name}\nStrength: {monster.damage}"  
    # Border 
    monster_border = pygame.Rect(x, y, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10)
    pygame.draw.rect(surface, RED, monster_border, width=5, border_radius=10)
    # Image
    monster_image = pygame.image.load(fileIO.resource_path(f"images\\{monster.image}")).convert()
    monster_image = pygame.transform.scale(monster_image, (100, 100))
    surface.blit(monster_image, (monster_border.x + 10, monster_border.y + 10))
    
    health_bar_width = 90
    health_bar_height = 10
    health_bar_x = monster_border.x + 15
    health_bar_y = monster_border.y + monster_image.get_height() + 15
    health_percentage = monster.health / monster.start_health
    draw_health_bar(surface, health_bar_x, health_bar_y, health_bar_width, health_bar_height, health_percentage)
    draw_multiple_lines(monster_text, font, BLACK, surface, monster_border.x + monster_image.get_width() + 10, monster_border.y + 10)

def draw_popup(title:str, buttons:dict[str, callable], surface, font) -> None:
    """Draw a popup window with a title and buttons."""
    popup_x = (SCREEN_WIDTH - POPUP_WIDTH) // 2
    popup_y = (SCREEN_HEIGHT - POPUP_HEIGHT) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, POPUP_WIDTH, POPUP_HEIGHT)

    pygame.draw.rect(surface, WHITE, popup_rect, border_radius=10)
    pygame.draw.rect(surface, BLACK, popup_rect, width=5, border_radius=10)
    draw_text_centered(title, font, BLACK, surface, SCREEN_WIDTH // 2, popup_y + 20)

    for button in buttons.values():
        button.draw(surface)
                
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


class Game:
    pygame.init()

    font = pygame.font.Font(None, 24)
    
    buttons = {
        GameState.WELCOME : {
            "New Game":     Button("New Game", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20), (200, 50), font, BLACK, GREEN, LIGHT_GREEN),
            "Load Game":    Button("Load Game", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40), (200, 50), font, BLACK, BLUE, LIGHT_BLUE),
            "Exit Game":    Button("Exit Game", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100), (200, 50), font, BLACK, RED, LIGHT_RED),
        },
        GameState.NEW_GAME : {
            "Fighter":      Button("Fighter", (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 30), (200, 50), font, BLACK, RED, LIGHT_RED),
            "Rogue":        Button("Rogue", (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 100), (200, 50), font, BLACK, GREEN, LIGHT_GREEN),
            "Back":         Button("Back", (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 170), (200, 50), font, BLACK, RED, LIGHT_RED),
            "Create Hero":  Button("Create Hero", (SCREEN_WIDTH // 16 * 9, SCREEN_HEIGHT - 70), (250, 50), font, BLACK, GRAY, LIGHT_GRAY),
        },
        GameState.MAIN_GAME : {
            "Menu":         Button("Menu", (0, SCREEN_HEIGHT - SCREEN_HEIGHT // 12), (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 12), font, BLACK, RED, LIGHT_RED),
            "Inventory":    Button("Inventory", (SCREEN_WIDTH // 4, SCREEN_HEIGHT - SCREEN_HEIGHT // 12), (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 12), font, BLACK, BLUE, LIGHT_BLUE),
            "Battle":       Button("Battle", (SCREEN_WIDTH // 2, SCREEN_HEIGHT - SCREEN_HEIGHT // 12), (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 12), font, BLACK, RED, LIGHT_RED),
            "Shop":         Button("Shop", (SCREEN_WIDTH // 4 * 3, SCREEN_HEIGHT - SCREEN_HEIGHT // 12), (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 12), font, BLACK, YELLOW, LIGHT_YELLOW),
        },
        GameState.BATTLE : {
            PlayerAction.HOME:{
            "Attack":       Button("Attack", (SCREEN_WIDTH // 2 + 15, SCREEN_HEIGHT // 2 + 20), (200, 50), font, BLACK, RED, LIGHT_RED),
            "Use Potion":   Button("Use Potion", (SCREEN_WIDTH // 2 + 15, SCREEN_HEIGHT // 2 + 75), (200, 50), font, BLACK, GREEN, LIGHT_GREEN),
            "Defend":    Button("Defend", (SCREEN_WIDTH // 2 + 15, SCREEN_HEIGHT // 2 + 130), (200, 50), font, BLACK, LIGHT_GRAY, LIGHT_GRAY),
            "Flee":         Button("Flee", (SCREEN_WIDTH // 2 + 15, SCREEN_HEIGHT // 2 + 185), (200, 50), font, BLACK, YELLOW, LIGHT_YELLOW),
            },
            PlayerAction.USE_ITEM:{
            "Health Potion": Button("Health Potion", (SCREEN_WIDTH // 2 + 15, SCREEN_HEIGHT // 2 + 20), (200, 50), font, BLACK, GREEN, LIGHT_GREEN),
            "Damage Potion": Button("Damage Potion", (SCREEN_WIDTH // 2 + 15, SCREEN_HEIGHT // 2 + 75), (200, 50), font, BLACK, RED, LIGHT_RED),
            "Block Potion":  Button("Block Potion", (SCREEN_WIDTH // 2 + 15, SCREEN_HEIGHT // 2 + 130), (200, 50), font, BLACK, BLUE, LIGHT_BLUE),
            "Back":         Button("Back", (SCREEN_WIDTH // 2 + 15, SCREEN_HEIGHT // 2 + 185), (200, 50), font, BLACK, RED, LIGHT_RED),
            },
        },
        GameState.SHOP : {
            "Purchase":     Button("Purchase", (SCREEN_WIDTH // 2 + 15, SCREEN_HEIGHT // 2 + 20), (250, 50), font, BLACK, LIGHT_GRAY, LIGHT_GRAY),
            "Leave":        Button("Leave", (SCREEN_WIDTH // 2 + 15, SCREEN_HEIGHT // 2 + 75), (250, 50), font, BLACK, RED, LIGHT_RED),
            "Potion Card":  Button("Potion Card", (SCREEN_WIDTH // 8, 25), (SCREEN_WIDTH // 16 * 3, SCREEN_HEIGHT // 3), font, BLACK, LIGHT_GRAY, GRAY),
            "Weapon Card":  Button("Weapon Card", (SCREEN_WIDTH // 32 * 13, 25), (SCREEN_WIDTH // 16 * 3, SCREEN_HEIGHT // 3), font, BLACK, LIGHT_RED, RED),
            "Armor Card":   Button("Armor Card", (SCREEN_WIDTH // 16 * 11, 25), (SCREEN_WIDTH // 16 * 3, SCREEN_HEIGHT // 3), font, BLACK, LIGHT_BLUE, BLUE),
        },
        GameState.GAME_OVER : {},
        GameState.EXIT : {},
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
        self.game_state = GameState.WELCOME
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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Village Defense")
        pygame.display.set_icon(pygame.image.load(fileIO.resource_path("icon.ico")))

    def events(self, buttons:dict[str, Button]=None) -> str:
        if buttons is None:
            buttons = self.buttons[self.game_state]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.EXIT
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.key_actions and event.key in self.key_actions:
                    if self.key_actions[event.key] == "escape" and self.game_state != GameState.WELCOME:
                        self.show_esc_popup()
                    else:
                        return self.key_actions[event.key]
                else:
                    if event.unicode and len(event.unicode) == 1 and event.unicode.isprintable():
                        return event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons is not None:
                    for button_name, button in self.buttons[GameState.MAIN_GAME].items():
                        if button.is_clicked(event):
                            if button_name == "Menu":
                                self.show_esc_popup()
                            elif button_name == "Inventory":
                                pass
                            elif button_name == "Battle" and self.game_state != GameState.BATTLE:
                                self.game_state = GameState.BATTLE
                                self.running = False
                            elif button_name == "Shop" and self.game_state != GameState.SHOP:
                                self.game_state = GameState.SHOP
                                self.running = False
                    for button_name, button in buttons.items():
                        if button.is_clicked(event):
                            return button_name
        return None

    def update(self) -> None:
        self.clock.tick(FPS)
        pygame.display.update()

    def quit(self) -> None:
        """Quit the game."""
        pygame.quit()

    def show_esc_popup(self) -> None:
        """Show the escape popup menu."""
        popup_running = True
        popup_x = (SCREEN_WIDTH - POPUP_WIDTH) // 2
        popup_y = (SCREEN_HEIGHT - POPUP_HEIGHT) // 2
        exit_text = "Exit Game" if self.game_state == GameState.NEW_GAME else "Save and Exit"

        buttons = {
            "Resume": Button("Resume", (popup_x + 50, popup_y + 50), (300, 50), self.font, BLACK, LIGHT_GREEN, GREEN),
            exit_text: Button(exit_text, (popup_x + 50, popup_y + 120), (300, 50), self.font, BLACK, LIGHT_RED, RED),
        }

        while popup_running:
            draw_popup("Pause Menu", buttons, self.screen, self.font)
            action = self.events(buttons)
            if action == "Resume":
                popup_running = False
            elif action == exit_text:
                if self.game_state != GameState.NEW_GAME:
                    fileIO.save_game(self.hero)
                self.game_state = GameState.WELCOME
                self.running = False
                popup_running = False
            elif action == "quit":
                self.game_state = GameState.EXIT
                self.running = False
                popup_running = False
            self.update()
    
    def keep_fighting_popup(self) -> None:
        """Show the popup after defeating a monster."""
        popup_running = True
        popup_x = (SCREEN_WIDTH - POPUP_WIDTH) // 2
        popup_y = (SCREEN_HEIGHT - POPUP_HEIGHT) // 2
        
        buttons = {
            "Continue Fighting": Button("Continue Fighting", (popup_x + 50, popup_y + 50), (300, 50), self.font, BLACK, GREEN, LIGHT_GREEN),
            "Retreat": Button("Retreat", (popup_x + 50, popup_y + 120), (300, 50), self.font, BLACK, RED, LIGHT_RED),
        }

        while popup_running:
            draw_popup("Monster Defeated!", buttons, self.screen, self.font)
            action = self.events(buttons)
            if action == "Continue Fighting":
                popup_running = False
                self.game_state = GameState.BATTLE
            elif action == "Retreat":
                self.game_state = GameState.MAIN_GAME
                popup_running = False
            elif action == "quit":
                self.game_state = GameState.EXIT
                popup_running = False
            self.update()

    def welcome_screen(self) -> None:
        """Welcome screen with options to start a new game or load an existing game."""
        self.running = True
        self.hero = fileIO.load_game()
            
        while self.running:
            self.screen.fill(WHITE)

            draw_text_centered("Welcome to Village Defense!", self.font, BLACK, self.screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
            if self.hero is not None:
                self.buttons[GameState.WELCOME]["Load Game"].button_color = BLUE
                self.buttons[GameState.WELCOME]["Load Game"].hover_color = LIGHT_BLUE
            else:
                self.buttons[GameState.WELCOME]["Load Game"].button_color = LIGHT_GRAY
                self.buttons[GameState.WELCOME]["Load Game"].hover_color = LIGHT_GRAY

            for button in self.buttons[GameState.WELCOME].values():
                button.draw(self.screen)
            action = self.events()
            if action == "quit":
                self.game_state = GameState.EXIT
                self.running = False
            elif action == "New Game":
                print("New Game selected")
                self.game_state = GameState.NEW_GAME
                self.running = False
            elif action == "Load Game" and self.hero is not None:
                print("Load Game selected")
                self.game_state = GameState.MAIN_GAME
                self.running = False
            elif action == "Exit Game":
                print("Exit Game selected")
                self.game_state = GameState.EXIT
                self.running = False
            self.update()

    def new_game_screen(self) -> None:
        """New game screen for creating a hero."""
        hero_name = ""
        hero_class = ""
        self.running = True

        while self.running:
            self.screen.fill(WHITE)
            create_button_color = GREEN if hero_name and hero_class else LIGHT_GRAY
            create_hover_color = LIGHT_GREEN if hero_name and hero_class else LIGHT_GRAY
            if create_button_color != self.buttons[GameState.NEW_GAME]["Create Hero"].button_color:
                self.buttons[GameState.NEW_GAME]["Create Hero"].button_color = create_button_color
                self.buttons[GameState.NEW_GAME]["Create Hero"].hover_color = create_hover_color
            
            draw_text(f"Hero Name: {hero_name}", self.font, BLACK, self.screen, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 100)
            draw_text(f"Choose your class: {hero_class}", self.font, BLACK, self.screen, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 30)

            for button in self.buttons[GameState.NEW_GAME].values():
                button.draw(self.screen)

            action = self.events(self.buttons[GameState.NEW_GAME])
            if action is not None:
                if action == "Fighter":
                    print("Fighter selected")
                    hero_class = "Fighter"
                elif action == "Rogue":
                    print("Rogue selected")
                    hero_class = "Rogue"
                elif action == "Back":
                    print("Back selected")
                    self.game_state = GameState.WELCOME
                    self.running = False
                elif action == "Create Hero" or action == "enter":
                    print("Create Hero selected")
                    if hero_name and hero_class:
                        self.hero = make_hero(hero_name, hero_class)
                        self.game_state = GameState.MAIN_GAME
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
        battle_state = PlayerAction.HOME

        if self.monster is None or not self.monster.alive:
            self.monster = get_monster(self.hero.level)
        
        while self.running:
            self.screen.fill(WHITE)
            draw_hero(self.hero, self.screen, self.font)
            draw_monster(self.monster, self.screen, self.font, 0, 0)

            if battle_state == PlayerAction.HOME:
                protection_button_color = LIGHT_BLUE if self.hero.protection is not None and self.hero.protection.active == 0 else LIGHT_GRAY
                if protection_button_color != self.buttons[GameState.BATTLE][battle_state]["Defend"].button_color:
                    self.buttons[GameState.BATTLE][battle_state]["Defend"].button_color = protection_button_color
            elif battle_state == PlayerAction.USE_ITEM:
                for button in self.buttons[GameState.BATTLE][battle_state].values():
                    if button.text == "Health Potion":
                        if self.hero.potion_bag["Health Potion"] > 0:
                            button.button_color = GREEN
                            button.hover_color = LIGHT_GREEN
                        else:
                            button.button_color = LIGHT_GRAY
                            button.hover_color = LIGHT_GRAY
                    elif button.text == "Damage Potion":
                        if self.hero.potion_bag["Damage Potion"] > 0:
                            button.button_color = RED
                            button.hover_color = LIGHT_RED
                        else:
                            button.button_color = LIGHT_GRAY
                            button.hover_color = LIGHT_GRAY
                    elif button.text == "Block Potion":
                        if self.hero.potion_bag["Block Potion"] > 0:
                            button.button_color = BLUE
                            button.hover_color = LIGHT_BLUE
                        else:
                            button.button_color = LIGHT_GRAY
                            button.hover_color = LIGHT_GRAY

            lines = 0
            for i, log_entry in enumerate(battle_log[-5:]):
                lines += draw_wrapped_text(log_entry, self.font, BLACK, self.screen, SCREEN_WIDTH // 2 + 15, 15 + (i + lines) * self.font.get_linesize(), SCREEN_WIDTH // 2 - 30)
            
            for button in self.buttons[GameState.BATTLE][battle_state].values():
                button.draw(self.screen)
            for button in self.buttons[GameState.MAIN_GAME].values():
                button.draw(self.screen)

            action = self.events(self.buttons[GameState.BATTLE][battle_state])
            if action is not None:
                if action == "Attack":
                    print("weapon attack selected")
                    self.monster.take_damage(self.hero.equipment.damage)
                    battle_log.append(f"{self.hero.name} attacks {self.monster.name} with {self.hero.equipment.name} for {self.hero.equipment.damage} damage.")
                    if self.monster.alive:
                        self.hero.take_damage(self.monster.damage)
                        battle_log.append(f"{self.monster.name} attacks {self.hero.name} for {self.monster.damage} damage.")
                elif action == "Use Potion":
                    print("use potion selected")
                    if self.hero.has_potions():
                        battle_state = PlayerAction.USE_ITEM                            
                elif action == "Defend":
                    print("Use Protection selected")
                    if self.hero.protection is not None and self.hero.protection.active == 0:
                        self.hero.protection.active = self.hero.protection.cooldown
                        battle_log.append(f"{self.hero.name} uses {self.hero.protection.name} for {self.hero.protection.cooldown} turns.")
                elif action == "Flee":
                    print("Flee selected")
                    self.game_state = GameState.MAIN_GAME
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
                    battle_state = PlayerAction.HOME
    
            if self.hero.alive and not self.monster.alive:
                print("Monster defeated!")
                battle_log.append(f"{self.monster.name} has been defeated!")
                battle_log.append(f"{self.hero.name} gains {self.monster.experience} experience and 10 gold.")
                self.hero.gain_experience(self.monster.experience)
                self.hero.add_gold(10)
                self.keep_fighting_popup()
                if self.game_state == GameState.BATTLE:
                    self.monster = get_monster(self.hero.level)
                elif self.game_state == GameState.MAIN_GAME:
                    self.running = False
            elif not self.hero.alive:
                print("Hero defeated!")
                self.game_state = GameState.GAME_OVER
                self.running = False
            self.update()

    def shop_screen(self) -> None:
        """Shop screen where the hero can buy items."""
        card_selected = None
        self.running = True
        potion_name = random.choice(list(potion_dictionary.keys()))
        weapon_name = random.choice(list(weapon_dictionary.keys()))
        armor_name = random.choice(list(armor_dictionary.keys()))

        purchase_button_colors = (GRAY, LIGHT_GRAY)
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
                purchase_button_colors = (GRAY, LIGHT_GRAY)
            else:
                purchase_button_colors = (GREEN, LIGHT_GREEN) if self.hero.gold >= card_price else (GRAY, LIGHT_GRAY)
            if purchase_button_colors != (self.buttons[GameState.SHOP]["Purchase"].button_color, self.buttons[GameState.SHOP]["Purchase"].hover_color):
                self.buttons[GameState.SHOP]["Purchase"].button_color = purchase_button_colors[0]
                self.buttons[GameState.SHOP]["Purchase"].hover_color = purchase_button_colors[1]

            self.screen.fill(WHITE)
            draw_hero(self.hero, self.screen, self.font)

            for buttons in list(self.buttons[GameState.SHOP].values())[:2]:
                buttons.draw(self.screen)
            for buttons in self.buttons[GameState.MAIN_GAME].values():
                buttons.draw(self.screen)

            potion_border = LIGHT_GREEN if card_selected == "Potion Card" else BLACK
            weapon_border = LIGHT_GREEN if card_selected == "Weapon Card" else BLACK
            armor_border = LIGHT_GREEN if card_selected == "Armor Card" else BLACK

            draw_item(potion_dictionary[potion_name], self.buttons[GameState.SHOP]["Potion Card"], self.screen, potion_border)
            draw_item(weapon_dictionary[weapon_name], self.buttons[GameState.SHOP]["Weapon Card"], self.screen, weapon_border)
            draw_item(armor_dictionary[armor_name], self.buttons[GameState.SHOP]["Armor Card"], self.screen, armor_border)

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
                    self.game_state = GameState.MAIN_GAME
                    self.running = False
            self.update()
        if card_selected is not None:
            self.buttons[GameState.SHOP][card_selected].button_color = LIGHT_GRAY

    def main_game(self) -> None:
        """Main game screen."""
        self.running = True
        while self.running:
            self.screen.fill(WHITE)
            draw_hero(self.hero, self.screen, self.font)
            for button in self.buttons[GameState.MAIN_GAME].values():
                button.draw(self.screen)
            draw_text_centered("Main Game", self.font, BLACK, self.screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)

            self.events()
            
            self.update()
    
    def game_over_screen(self) -> None:
        """Game over screen."""
        self.running = True
        while self.running:
            self.screen.fill(WHITE)
            draw_text_centered(f"{self.hero.name} has been slain!", self.font, BLACK, self.screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
            draw_text_centered("Game Over", self.font, BLACK, self.screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            draw_text_centered("Press ESC to return to the main menu", self.font, BLACK, self.screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.EXIT
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.WELCOME
                        self.running = False

            self.update()
