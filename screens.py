
import random
from hero import Hero, make_hero
from monster import Monster, get_monster
from items import equipment_dictionary, armor_dictionary
from constants import GameState
import fileIO
import pygame

pygame.init()

# Initialize the mixer for music
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load(fileIO.resource_path("music\\background_music.mp3"))  # Replace with your music file path
pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play music in a loop

POPUP_WIDTH = 400
POPUP_HEIGHT = 200

# Set up the game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Village Defense")
pygame.display.set_icon(pygame.image.load(fileIO.resource_path("icon.ico")))

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

# Fonts
font = pygame.font.Font(None, 36)

def draw_text(text:str, font:pygame.font, color:tuple, surface:pygame.Rect, x:int, y:int) -> None:
    """Draw text on the screen at the specified position."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)

def draw_text_centered(text:str, font:pygame.font, color:tuple, surface:pygame.Rect, x:int, y:int) -> None:
    """Draw centered text on the screen at the specified position."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def draw_wrapped_text(text:str, font:pygame.font, color:tuple, surface:pygame.Rect, x:int, y:int, max_width:int) -> int:
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

def draw_multiple_lines(text:str, font:pygame.font, color:tuple, surface:pygame.Rect, x:int, y:int) -> None:
    """Draw multiple lines of text on the screen at the specified position."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        draw_text(line, font, color, surface, x, y + i * 30)

def draw_button(text, font, color, surface, x, y, width, height):
    """Draw a button with text on the screen."""
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, button_rect, border_radius=10)
    pygame.draw.rect(surface, BLACK, button_rect, width=2, border_radius=10)
    draw_text(text, font, BLACK, surface, x + width // 2 - font.size(text)[0] // 2, y + height // 2 - font.size(text)[1] // 2)

def draw_buttons(buttons:list[tuple[str, pygame.Rect, tuple[int, int, int]]]) -> None:
    """Draw multiple buttons on the screen."""
    for button_text, button_rect, color in buttons:
        draw_button(button_text, font, color, screen, button_rect.x, button_rect.y, button_rect.width, button_rect.height)

def draw_hero(hero:Hero) -> None:
    """Draw the hero's information on the screen."""
    # Hero Information
    hero_text = f"Name: {hero.name}\nHealth: {hero.health}    Level: {hero.level}\nGold: {hero.gold}    Exp: {hero.experience}"
    if hero.special is not None:
        hero_text += f"\nSpecial: {hero.special}"
    if hero.equipment is not None:
        hero_text += f"\nWeapon: {hero.equipment}"
    if hero.protection is not None:
        hero_text += f"\nProtection: {hero.protection}"
    hero_background = pygame.Rect(5, 5, SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10)
    pygame.draw.rect(screen, BLUE, hero_background, width=2, border_radius=10)
    draw_multiple_lines(hero_text, font, BLACK, screen, 15, 15)
     # Protection Status
    if hero.special is not None:
        special_status_text = f"{hero.special}: Cooldown {hero.special.active}" if hero.special and hero.special.active > 0 else f"{hero.special}: Available"
        special_status_color = RED if hero.special and hero.special.active > 0 else GREEN
        draw_text(special_status_text, font, special_status_color, screen, 15, SCREEN_HEIGHT // 2 - 100)
    if hero.protection is not None:
        protection_status_text = f"{hero.protection}: Active {hero.protection.active} Turns" if hero.protection and hero.protection.active > 0 else f"{hero.protection}: Inactive"
        protection_status_color = GREEN if hero.protection and hero.protection.active > 0 else RED
        draw_text(protection_status_text, font, protection_status_color, screen, 15, SCREEN_HEIGHT // 2 - 50)

    hero_image = pygame.image.load(fileIO.resource_path(f"sprites\{hero.image}"))
    hero_image = pygame.transform.scale(hero_image, (100, 100))
    screen.blit(hero_image, (SCREEN_WIDTH // 2 - 120, 20))

def draw_monster(monster:Monster) -> None:
    """Draw the monster's information on the screen."""
    monster_text = f"Monster: {monster.name}\nHealth: {monster.health}\nDamage: {monster.damage}"   
    monster_background = pygame.Rect(SCREEN_WIDTH // 2 + 5, 5, SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10)
    pygame.draw.rect(screen, RED, monster_background, width=2, border_radius=10)
    draw_multiple_lines(monster_text, font, BLACK, screen, SCREEN_WIDTH //2 + 15, 15)

    monster_image = pygame.image.load(fileIO.resource_path(f"sprites\{monster.image}"))
    monster_image = pygame.transform.scale(monster_image, (100, 100))
    screen.blit(monster_image, (SCREEN_WIDTH - 120, 20))

def draw_popup(title:str, buttons:list[tuple[str, pygame.Rect, tuple[int, int, int]]]) -> None:
    """Draw a popup window with a title and buttons."""
    popup_x = (SCREEN_WIDTH - POPUP_WIDTH) // 2
    popup_y = (SCREEN_HEIGHT - POPUP_HEIGHT) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, POPUP_WIDTH, POPUP_HEIGHT)

    pygame.draw.rect(screen, WHITE, popup_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, popup_rect, width=5, border_radius=10)
    draw_text_centered(title, font, BLACK, screen, SCREEN_WIDTH // 2, popup_y + 20)

    draw_buttons(buttons)
                
def handle_events(events:list[pygame.event.Event], buttons:dict[str, callable]=None, key_actions:dict[int, str]=None):
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


class Screens:
    """Class to manage different game screens."""
    def __init__(self) -> None:
        #self.game_state = GameState.WELCOME
        return

    def quit(self) -> None:
        """Quit the game."""
        pygame.quit()

    def show_esc_popup(self, hero:Hero, game_state:GameState) -> GameState:
        """Show the escape popup menu."""
        popup_running = True
        popup_x = (SCREEN_WIDTH - POPUP_WIDTH) // 2
        popup_y = (SCREEN_HEIGHT - POPUP_HEIGHT) // 2
        exit_text = "Exit Game" if game_state == GameState.NEW_GAME else "Save and Exit"

        buttons = {
            "Resume": {"rect": pygame.Rect(popup_x + 50, popup_y + 50, 300, 50), "color": LIGHT_GREEN},
            exit_text: {"rect": pygame.Rect(popup_x + 50, popup_y + 120, 300, 50), "color": LIGHT_BLUE},
        }
        key_actions = {
            pygame.K_ESCAPE: exit_text,
        }

        while popup_running:
            draw_popup("Pause Menu", [(text, data["rect"], data["color"]) for text, data in buttons.items()])
            action = handle_events(pygame.event.get(), buttons, key_actions)
            if action == "Resume":
                popup_running = False
            elif action == exit_text:
                if game_state != GameState.NEW_GAME:
                    fileIO.save_game(hero)
                game_state = GameState.WELCOME
                popup_running = False
            elif action == "quit":
                game_state = GameState.EXIT
                popup_running = False
            pygame.display.update()
        return game_state
    
    def keep_fighting_popup(self) -> GameState:
        """Show the popup after defeating a monster."""
        popup_running = True
        popup_x = (SCREEN_WIDTH - POPUP_WIDTH) // 2
        popup_y = (SCREEN_HEIGHT - POPUP_HEIGHT) // 2
        
        buttons = {
            "Continue Fighting": {"rect": pygame.Rect(popup_x + 50, popup_y + 50, 300, 50), "color": LIGHT_GREEN},
            "Retreat": {"rect": pygame.Rect(popup_x + 50, popup_y + 120, 300, 50), "color": LIGHT_RED},
        }

        while popup_running:
            draw_popup("Monster Defeated!", [(text, data["rect"], data["color"]) for text, data in buttons.items()])
            action = handle_events(pygame.event.get(), buttons)

            if action == "Continue Fighting":
                popup_running = False
                game_state = GameState.BATTLE
            elif action == "Retreat":
                game_state = GameState.MAIN_GAME
                popup_running = False
            elif action == "quit":
                game_state = GameState.EXIT
                popup_running = False
            pygame.display.update()
        return game_state
    
    def new_game_screen(self) -> tuple[GameState, Hero]:
        """New game screen for creating a hero."""
        hero = None
        hero_name = ""
        hero_class = ""
        running = True        
        key_actions = {
            pygame.K_ESCAPE: "escape",
            pygame.K_BACKSPACE: "backspace",
            pygame.K_RETURN: "enter",
            pygame.K_DELETE: "delete",
            pygame.K_TAB: "tab",
        }
        while running:
            screen.fill(WHITE)
            create_button_color = LIGHT_GREEN if hero_name and hero_class else LIGHT_GRAY
            buttons = {
                "Fighter": {"rect": pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 30, 200, 50), "color": LIGHT_RED},
                "Rogue": {"rect" : pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 100, 200, 50), "color": LIGHT_GREEN},
                "Back": {"rect": pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 170, 200, 50), "color": LIGHT_RED},
                "Create Hero": {"rect": pygame.Rect(SCREEN_WIDTH // 16 * 9, SCREEN_HEIGHT - 70, 250, 50), "color": create_button_color},
            }
            
            draw_text(f"Hero Name: {hero_name}", font, BLACK, screen, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 100)
            draw_text(f"Choose your class: {hero_class}", font, BLACK, screen, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 30)
            draw_buttons([(text, data["rect"], data["color"]) for text, data in buttons.items()])

            action = handle_events(pygame.event.get(), buttons, key_actions)
            if action == "escape":
                next_state = self.show_esc_popup(hero, GameState.NEW_GAME)
                if next_state == GameState.WELCOME:
                    running = False
            elif action == "quit":
                next_state = GameState.EXIT
                running = False
            elif action == "Fighter":
                print("Fighter selected")
                hero_class = "Fighter"
            elif action == "Rogue":
                print("Rogue selected")
                hero_class = "Rogue"
            elif action == "Back":
                print("Back selected")
                next_state = GameState.WELCOME
                running = False
            elif action == "Create Hero" or action == "enter":
                print("Create Hero selected")
                if hero_name and hero_class:
                    hero = make_hero(hero_name, hero_class)
                    next_state = GameState.MAIN_GAME
                    running = False
            elif action == "backspace":
                hero_name = hero_name[:-1]
            elif action == "delete":
                hero_name = ""
            elif action == "tab":
                hero_name += "   "
            elif action and len(action) == 1 and action.isprintable():
                if len(hero_name) < 20:
                    hero_name += action
            pygame.display.update()
        return next_state, hero

    def welcome_screen(self) -> tuple[GameState, Hero]:
        """Welcome screen with options to start a new game or load an existing game."""
        running = True
        hero = fileIO.load_game()

        if hero is not None:
            buttons = {
                "New Game": {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50), "color": LIGHT_GREEN},
                "Load Game": {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50), "color": LIGHT_BLUE},
                "Exit Game": {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50), "color": LIGHT_RED},
            }
        else:
            buttons = {
                "New Game": {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50), "color": LIGHT_GREEN},
                "Exit Game": {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50), "color": LIGHT_RED},
            }
        key_actions = {
            pygame.K_ESCAPE: "escape",
        }
        while running:
            screen.fill(WHITE)
            draw_text_centered("Welcome to Village Defense!", font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
            draw_buttons([(text, data["rect"], data["color"]) for text, data in buttons.items()])
            action = handle_events(pygame.event.get(), buttons, key_actions)
            if action == "quit":
                next_state = GameState.EXIT
                running = False
            elif action == "New Game":
                print("New Game selected")
                next_state = GameState.NEW_GAME
                running = False
            elif action == "Load Game":
                print("Load Game selected")
                next_state = GameState.MAIN_GAME
                running = False
            elif action == "Exit Game":
                print("Exit Game selected")
                next_state = GameState.EXIT
                running = False
            pygame.display.update()
        return next_state, hero

    def battle_screen(self, hero:Hero, monster:Monster) -> GameState:
        """Battle screen where the hero fights a monster."""
        running = True
        battle_log = []

        action_background = pygame.Rect(5, SCREEN_HEIGHT // 2 + 5, SCREEN_WIDTH //2 - 10, SCREEN_HEIGHT // 2 - 10)
        log_background = pygame.Rect(SCREEN_WIDTH // 2 + 5, SCREEN_HEIGHT // 2 + 5, SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10)

        while running:
            screen.fill(WHITE)
            draw_hero(hero)
            draw_monster(monster)
            pygame.draw.rect(screen, GREEN, action_background, width=2, border_radius=10)
            pygame.draw.rect(screen, LIGHT_GRAY, log_background, width=2, border_radius=10)

            protection_button_color = LIGHT_BLUE if hero.protection is not None and hero.protection.active == 0 else LIGHT_GRAY
            special_button_color = LIGHT_GREEN if hero.special is not None and hero.special.active == 0 else LIGHT_GRAY

            lines = 0
            for i, log_entry in enumerate(battle_log[-5:]):
                lines += draw_wrapped_text(log_entry, font, BLACK, screen, SCREEN_WIDTH // 2 + 15, SCREEN_HEIGHT // 2 + 15 + (i + lines) * font.get_linesize(), SCREEN_WIDTH // 2 - 30)

            buttons = {
                hero.equipment.name: {"rect": pygame.Rect(15, SCREEN_HEIGHT // 2 + 20, 200, 50), "color": LIGHT_RED},
                hero.special.name: {"rect" : pygame.Rect(15, SCREEN_HEIGHT // 2 + 80, 200, 50), "color": special_button_color},
                hero.protection.name: {"rect": pygame.Rect(15, SCREEN_HEIGHT // 2 + 140, 200, 50), "color": protection_button_color},
                "Flee": {"rect": pygame.Rect(15, SCREEN_HEIGHT // 2 + 200, 200, 50), "color": LIGHT_YELLOW},
            }
            key_actions = {
                pygame.K_ESCAPE: "escape",
            }

            draw_buttons([(text, data["rect"], data["color"]) for text, data in buttons.items()])

            action = handle_events(pygame.event.get(), buttons, key_actions)
            if action == "escape":
                next_state = self.show_esc_popup(hero, GameState.BATTLE)
                if next_state == GameState.WELCOME:
                    running = False
            elif action == "quit":
                next_state = GameState.EXIT
                running = False
            elif action == hero.equipment.name:
                print("weapon attack selected")
                monster.take_damage(hero.equipment.damage)
                battle_log.append(f"{hero.name} attacks {monster.name} with {hero.equipment.name} for {hero.equipment.damage} damage.")
                if monster.alive:
                    hero.take_damage(monster.damage)
                    battle_log.append(f"{monster.name} attacks {hero.name} for {monster.damage} damage.")
            elif action == hero.special.name:
                print("special attack selected")
                damage = hero.use_special()
                monster.take_damage(damage)
                battle_log.append(f"{hero.name} uses {hero.special.name} on {monster.name} for {damage} damage.")
                if monster.alive:
                    hero.take_damage(monster.damage)
                    battle_log.append(f"{monster.name} attacks {hero.name} for {monster.damage} damage.")
            elif action == hero.protection.name:
                print("Use Protection selected")
                if hero.protection is not None and hero.protection.active == 0:
                    hero.protection.active = hero.protection.cooldown
                    battle_log.append(f"{hero.name} uses {hero.protection.name} for {hero.protection.cooldown} turns.")
            elif action == "Flee":
                print("Flee selected")
                next_state = GameState.MAIN_GAME
                running = False
    
            if hero.alive and not monster.alive:
                print("Monster defeated!")
                hero.gain_experience(monster.experience)
                hero.add_gold(10)
                next_state = self.keep_fighting_popup()
                if next_state == GameState.BATTLE:
                    monster = get_monster(hero.level)
                elif next_state == GameState.MAIN_GAME:
                    running = False
            elif not hero.alive:
                print("Hero defeated!")
                next_state = GameState.GAME_OVER
                running = False
            pygame.display.update()
        return next_state

    def shop_screen(self, hero:Hero) -> GameState:
        """Shop screen where the hero can buy items."""
        running = True
        equipment_name = random.choice(list(equipment_dictionary.keys()))

        buttons = {
            "Buy Health": {"rect": pygame.Rect(15, SCREEN_HEIGHT // 2 + 20, 250, 50), "color": LIGHT_GRAY},
            equipment_name: {"rect" : pygame.Rect(15, SCREEN_HEIGHT // 2 + 120, 250, 50), "color": LIGHT_GRAY},
            "Back to Main": {"rect": pygame.Rect(15, SCREEN_HEIGHT - 70, 250, 50), "color": LIGHT_RED},
        }
        key_actions = {
            pygame.K_ESCAPE: "escape",
        }
        
        while running:
            screen.fill(WHITE)
            draw_hero(hero)
            buy_health_cost = 25
            buy_equipment_cost = 50

            health_button_color = LIGHT_GREEN if hero.gold >= buy_health_cost else LIGHT_GRAY
            equipment_button_color = LIGHT_GREEN if hero.gold >= buy_equipment_cost and equipment_name is not None else LIGHT_GRAY

            buttons.update({
                "Buy Health": {"rect": pygame.Rect(15, SCREEN_HEIGHT // 2 + 20, 250, 50), "color": health_button_color},
                equipment_name: {"rect" : pygame.Rect(15, SCREEN_HEIGHT // 2 + 120, 250, 50), "color": equipment_button_color},
            })

            draw_buttons([(text, data["rect"], data["color"]) for text, data in buttons.items()])
            draw_text(f"Cost: {buy_health_cost}", font, BLACK, screen, 15, SCREEN_HEIGHT // 2 + 80)
            draw_text(f"Cost: {buy_equipment_cost}", font, BLACK, screen, 15, SCREEN_HEIGHT // 2 + 180)

            action = handle_events(pygame.event.get(), buttons, key_actions)
            if action == "escape":
                next_state = self.show_esc_popup(hero, GameState.SHOP)
                if next_state == GameState.WELCOME:
                    running = False
            elif action == "quit":
                next_state = GameState.EXIT
                running = False
            elif action == "Buy Health":
                print("Buy Health selected")
                if hero.gold >= buy_health_cost:
                    hero.health += 10
                    hero.gold -= buy_health_cost
                else:
                    print("Not enough gold!")
            elif action == equipment_name:
                print("Buy Damage selected")
                if hero.gold >= buy_equipment_cost:
                    hero.gold -= buy_equipment_cost
                    hero.equipment = equipment_dictionary[equipment_name]
                    equipment_name = random.choice(list(equipment_dictionary.keys()))
                else:
                    print("Not enough gold!")
            elif action == "Back to Main":
                print("Back to Main selected")
                next_state = GameState.MAIN_GAME
                running = False
            
            pygame.display.update()
        return next_state

    def main_game(self, hero:Hero) -> GameState:
        """Main game screen."""
        running = True
        buttons = {
            "Battle": {"rect": pygame.Rect(15, SCREEN_HEIGHT // 2 + 20, 200, 50), "color": LIGHT_RED},
            "Shop": {"rect" : pygame.Rect(15, SCREEN_HEIGHT // 2 + 80, 200, 50), "color": LIGHT_YELLOW},
        }
        key_actions = {
            pygame.K_ESCAPE: "escape",
        }
        while running:
            screen.fill(WHITE)
            draw_hero(hero)
            
            #Action Box
            action_background = pygame.Rect(5, SCREEN_HEIGHT // 2 + 5, SCREEN_WIDTH - 10, SCREEN_HEIGHT // 2 - 10)
            pygame.draw.rect(screen, GREEN, action_background, width=2, border_radius=10)

            draw_buttons([(text, data["rect"], data["color"]) for text, data in buttons.items()])

            action = handle_events(pygame.event.get(), buttons, key_actions)
            if action == "escape":
                next_state = self.show_esc_popup(hero, GameState.MAIN_GAME)
                if next_state == GameState.WELCOME:
                    running = False
            elif action == "quit":
                next_state = GameState.EXIT
                running = False
            elif action == "Battle":
                print("Battle selected")
                next_state = GameState.BATTLE
                running = False
            elif action == "Shop":
                print("Shop selected")
                next_state = GameState.SHOP
                running = False
            
            pygame.display.update()
        return next_state
    
    def game_over_screen(self, hero:Hero):
        """Game over screen."""
        running = True
        while running:
            screen.fill(WHITE)
            draw_text_centered(f"{hero.name} has been slain!", font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
            draw_text_centered("Game Over", font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            draw_text_centered("Press ESC to return to the main menu", font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        next_state = GameState.WELCOME
                        running = False

            pygame.display.update()
        return next_state