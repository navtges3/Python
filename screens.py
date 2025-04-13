from hero import Hero, make_hero
from monster import Monster
from items import equipmentDictionary, protectionDictionary, lootDictionary, next_equipment_dictionary
from constants import GameState
import fileIO
import pygame

pygame.init()

# Set up the game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Village Defense")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)

def draw_text_centered(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def draw_multiple_lines(text, font, color, surface, x, y):
    lines = text.split("/n")
    for i, line in enumerate(lines):
        draw_text(line, font, color, surface, x, y + i * 30)

def draw_button(text, font, color, surface, x, y, width, height) -> pygame.Rect:
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, button_rect)
    draw_text(text, font, BLACK, surface, x + width // 2 - font.size(text)[0] // 2, y + height // 2 - font.size(text)[1] // 2)
    return button_rect

def draw_hero(hero:Hero) -> None:
    """Draw the hero's stats on the screen."""
    hero_text = f"Name: {hero.name}/nHealth: {hero.health}/nLevel: {hero.level}"
    if hero.special is not None:
        hero_text += f"/nSpecial: {hero.special.name}"
    if hero.equipment is not None:
        hero_text += f"/nWeapon: {hero.equipment.name}/nDamage: {hero.equipment.damage}"
    hero_text += f"/nExp: {hero.experience}/nGold: {hero.gold}"
    hero_background = pygame.Rect(5, 5, SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10)
    pygame.draw.rect(screen, BLUE, hero_background, width=2, border_radius=10)
    draw_multiple_lines(hero_text, font, BLACK, screen, 15, 15)

    hero_image = pygame.image.load(f"sprites\{hero.image}")
    hero_image = pygame.transform.scale(hero_image, (100, 100))
    screen.blit(hero_image, (SCREEN_WIDTH // 2 - 120, 20))

def draw_monster(monster:Monster) -> None:
    monster_text = f"Monster: {monster.name}/nHealth: {monster.health}/nDamage: {monster.damage}"   
    monster_background = pygame.Rect(SCREEN_WIDTH // 2 + 5, 5, SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10)
    pygame.draw.rect(screen, RED, monster_background, width=2, border_radius=10)
    draw_multiple_lines(monster_text, font, BLACK, screen, SCREEN_WIDTH //2 + 15, 15)

    monster_image = pygame.image.load(f"sprites\{monster.image}")
    monster_image = pygame.transform.scale(monster_image, (100, 100))
    screen.blit(monster_image, (SCREEN_WIDTH - 120, 20))

class Screens:

    def quit(self) -> None:
        pygame.quit()

    def show_esc_popup(self, hero:Hero, game_state:GameState) -> GameState:
        """Display a pop-up window with Save and Quit and Load Game options."""
        popup_running = True
        popup_width = 400
        popup_height = 200
        popup_x = (SCREEN_WIDTH - popup_width) // 2
        popup_y = (SCREEN_HEIGHT - popup_height) // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

        if game_state == GameState.NEW_GAME:
            exit_text = "Exit Game"
        else:
            exit_text = "Save and Exit"

        while popup_running:
            # Draw the semi-transparent background
            pygame.draw.rect(screen, WHITE, popup_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, popup_rect, width=5, border_radius=10)
            draw_text_centered("Game Paused", font, BLACK, screen, SCREEN_WIDTH // 2, popup_y + 20)
    
            # Draw buttons
            save_quit_button = draw_button(exit_text, font, GRAY, screen, popup_x + 50, popup_y + 50, 300, 50)
            resume_game_button = draw_button("Resume Game", font, GRAY, screen, popup_x + 50, popup_y + 120, 300, 50)
    
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_state = GameState.GAME_OVER
                    popup_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        popup_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if save_quit_button.collidepoint(event.pos):
                        print("Save and Quit selected")
                        fileIO.save_game(hero)
                        game_state = GameState.WELCOME
                        popup_running = False
                    elif resume_game_button.collidepoint(event.pos):
                        print("Resume Game selected")
                        popup_running = False

            pygame.display.update()
        return game_state

    def new_game_screen(self) -> tuple[GameState, Hero]:
        hero_name = ""
        hero_class = ""
        running = True

        while running:
            screen.fill(WHITE)

            draw_text(f"Hero Name: {hero_name}", font, BLACK, screen, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 100)
            draw_text(f"Choose your class: {hero_class}", font, BLACK, screen, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 30)
            fighter_button = draw_button("Fighter", font, GRAY, screen, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 30, 200, 50)
            rogue_button = draw_button("Rogue", font, GRAY, screen, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 100, 200, 50)
            create_button = draw_button("Create Hero", font, GRAY, screen, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 170, 200, 50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    next_state = GameState.GAME_OVER
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        hero_name = hero_name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        next_state = self.show_esc_popup(None, GameState.NEW_GAME)
                        if next_state == GameState.WELCOME:
                            running = False
                    elif event.key == pygame.K_RETURN:
                        print("Enter key pressed")
                        if hero_name and hero_class:
                            next_state = GameState.MAIN_GAME
                            running = False
                    else:
                        hero_name += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if fighter_button.collidepoint(event.pos):
                        print("Fighter selected")
                        hero_class = "Fighter"
                    elif rogue_button.collidepoint(event.pos):
                        print("Rogue selected")
                        hero_class = "Rogue"
                    elif create_button.collidepoint(event.pos):
                        print("Create Hero selected")
                        if hero_name and hero_class:
                            next_state = GameState.MAIN_GAME
                            running = False

            pygame.display.update()

        hero = make_hero(hero_name, hero_class)
        return next_state, hero

    def welcome_screen(self) -> tuple[GameState, Hero]:
        hero = None
        running = True

        hero = fileIO.load_game()

        while running:
            screen.fill(WHITE)

            new_game_button = draw_button("New Game", font, GRAY, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50)
            if hero is not None:
                load_game_button = draw_button("Load Game", font, GRAY, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
                close_game_button = draw_button("Exit Game", font, GRAY, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
            else:
                load_game_button = None
                close_game_button = draw_button("Exit Game", font, GRAY, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    next_state = GameState.GAME_OVER
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if new_game_button.collidepoint(event.pos):
                        print("New Game selected")
                        next_state = GameState.NEW_GAME
                        running = False
                    elif load_game_button and load_game_button.collidepoint(event.pos):
                        print("Load Game selected")
                        next_state = GameState.MAIN_GAME
                        running = False
                    elif close_game_button.collidepoint(event.pos):
                        print("Exit Game selected")
                        next_state = GameState.GAME_OVER
                        running = False

            pygame.display.update()
        return next_state, hero

    def battle_screen(self, hero:Hero, monster:Monster) -> GameState:
        """Battle screen where the hero fights a monster."""
        running = True
        while running:
            screen.fill(WHITE)

            #Hero Box
            draw_hero(hero)

            #Monster Box
            draw_monster(monster)

            #Action Box
            action_background = pygame.Rect(5, SCREEN_HEIGHT // 2 + 5, SCREEN_WIDTH - 10, SCREEN_HEIGHT // 2 - 80)
            pygame.draw.rect(screen, GREEN, action_background, width=2, border_radius=10)
            weapon_button = draw_button("Weapon Attack", font, GRAY, screen, 15, SCREEN_HEIGHT // 2 + 20, 200, 50)
            class_button = draw_button("Class Attack", font, GRAY, screen, 15, SCREEN_HEIGHT // 2 + 80, 200, 50)
            protection_button = draw_button("Use Protection", font, GRAY, screen, 245, SCREEN_HEIGHT // 2 + 20, 200, 50)
            flee_button = draw_button("Flee", font, GRAY, screen, 245, SCREEN_HEIGHT // 2 + 80, 200, 50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    next_state = GameState.GAME_OVER
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        next_state = self.show_esc_popup(hero, GameState.BATTLE)
                        if next_state == GameState.WELCOME:
                            running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if weapon_button.collidepoint(event.pos):
                        print("Weapon Attack selected")
                        monster.take_damage(hero.equipment.damage)
                        if monster.alive:
                            hero.take_damage(monster.damage)
                    if class_button.collidepoint(event.pos):
                        print("Class Attack selected")
                        monster.take_damage(hero.use_special())
                        if monster.alive:
                            hero.take_damage(monster.damage)
                    if protection_button.collidepoint(event.pos):
                        print("Use Protection selected")
                    if flee_button.collidepoint(event.pos):
                        print("Flee selected")
                        next_state = GameState.MAIN_GAME
                        running = False
            
            if hero.alive and not monster.alive:
                print("Monster defeated!")
                hero.gain_experience(monster.experience)
                hero.add_gold(10)
                next_state = GameState.MAIN_GAME
                running = False
            elif not hero.alive:
                print("Hero defeated!")
                next_state = GameState.WELCOME
                running = False
            pygame.display.update()
        return next_state

    def shop_screen(self, hero:Hero) -> GameState:
        running = True

        next_equipment = next_equipment_dictionary[hero.equipment.name]

        while running:
            screen.fill(WHITE)
            draw_hero(hero)

            # Buy Health
            buy_health_button = draw_button("Buy Health", font, GRAY, screen, 15, SCREEN_HEIGHT // 2 + 20, 250, 50)
            buy_health_cost = 75
            draw_text(f"Cost: {buy_health_cost}", font, BLACK, screen, 15, SCREEN_HEIGHT // 2 + 80)

            # Buy damage
            equipment_button = draw_button("Upgrade Equipment", font, GRAY, screen, 15, SCREEN_HEIGHT // 2 + 120, 250, 50)
            buy_damage_cost = 150
            draw_text(f"Cost: {buy_damage_cost}", font, BLACK, screen, 15, SCREEN_HEIGHT // 2 + 180)

            # Back to Main Game
            back_button = draw_button("Back to Main", font, GRAY, screen, 15, SCREEN_HEIGHT - 70, 250, 50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    next_state = GameState.GAME_OVER
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        next_state = self.show_esc_popup(hero, GameState.SHOP)
                        if next_state == GameState.WELCOME:
                            running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if buy_health_button.collidepoint(event.pos):
                        print("Buy Health selected")
                        if hero.gold >= buy_health_cost:
                            hero.health += 10
                            hero.gold -= buy_health_cost
                        else:
                            print("Not enough gold!")
                    elif equipment_button.collidepoint(event.pos):
                        print("Buy Damage selected")
                        if hero.gold >= buy_damage_cost:
                            hero.gold -= buy_damage_cost
                            hero.equipment = equipmentDictionary[next_equipment]
                        else:
                            print("Not enough gold!")
                    elif back_button.collidepoint(event.pos):
                        print("Back to Main selected")
                        next_state = GameState.MAIN_GAME
                        running = False

            pygame.display.update()
        return next_state

    def main_game(self, hero:Hero) -> GameState:
        """Main game screen."""
        running = True
        while running:
            screen.fill(WHITE)
            
            draw_hero(hero)
            
            #Action Box
            action_background = pygame.Rect(5, SCREEN_HEIGHT // 2 + 5, SCREEN_WIDTH - 10, SCREEN_HEIGHT // 2 - 80)
            pygame.draw.rect(screen, GREEN, action_background, width=2, border_radius=10)
            battle_button = draw_button("Fight Goblins", font, GRAY, screen, 15, SCREEN_HEIGHT // 2 + 20, 200, 50)
            shop_button = draw_button("Go to Shop", font, GRAY, screen, 15, SCREEN_HEIGHT // 2 + 80, 200, 50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    next_state = GameState.GAME_OVER
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        next_state = self.show_esc_popup(hero, GameState.MAIN_GAME)
                        if next_state == GameState.WELCOME:
                            running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if battle_button.collidepoint(event.pos):
                        print("Battle selected")
                        next_state = GameState.BATTLE
                        running = False
                    elif shop_button.collidepoint(event.pos):
                        print("Shop selected")
                        next_state = GameState.SHOP
                        running = False
            
            pygame.display.update()
        return next_state