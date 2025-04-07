from hero import Hero
from monster import Monster
from items import equipmentDictionary, protectionDictionary, lootDictionary
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

# This function is used to render text on the screen at a specified position.
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

class Screens:

    def quit(self) -> None:
        pygame.quit()

    def show_esc_popup(self, hero: Hero, game_state: GameState) -> GameState:
        """Display a pop-up window with Save and Quit and Load Game options."""
        popup_running = True
        popup_width = 400
        popup_height = 200
        popup_x = (SCREEN_WIDTH - popup_width) // 2
        popup_y = (SCREEN_HEIGHT - popup_height) // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    
        while popup_running:
            # Draw the semi-transparent background
            # screen.fill((0, 0, 0, 128))  # Semi-transparent black background
            pygame.draw.rect(screen, WHITE, popup_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, popup_rect, width=5, border_radius=10)  # Border for the popup
            draw_text_centered("Game Paused", font, BLACK, screen, SCREEN_WIDTH // 2, popup_y + 20)
    
            # Draw buttons
            save_quit_button = draw_button("Save and Quit", font, GRAY, screen, popup_x + 50, popup_y + 50, 300, 50)
            resume_game_button = draw_button("Resume Game", font, GRAY, screen, popup_x + 50, popup_y + 120, 300, 50)
    
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameState.GAME_OVER
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if save_quit_button.collidepoint(event.pos):
                        print("Save and Quit selected")
                        fileIO.save_game(hero)  # Save the game
                        return GameState.GAME_OVER
                    elif resume_game_button.collidepoint(event.pos):
                        print("Resume Game selected")
                        return  game_state # Or another state for loading the game
    
            pygame.display.update()

    def new_game_screen(self) -> tuple[GameState, Hero]:
        input_text = ""
        running = True
        while running:
            screen.fill(WHITE)

            draw_text(f"Hero Name: {input_text}", font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    next_state = GameState.GAME_OVER
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        print(f"New Hero Created: {input_text}")
                        hero = Hero(input_text, 10, equipmentDictionary["Sword"], protectionDictionary["Chainmail"])
                        fileIO.save_game(hero)
                        next_state = GameState.MAIN_GAME
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            pygame.display.update()
        return next_state, hero

    def welcome_screen(self) -> tuple[GameState, Hero]:
        hero = None
        running = True

        while running:
            screen.fill(WHITE)  # Fill the screen with white

            new_game_button = draw_button("New Game", font, GRAY, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50)
            load_game_button = draw_button("Load Game", font, GRAY, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    next_state = GameState.GAME_OVER
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if new_game_button.collidepoint(event.pos):  # Check if "New Game" button is clicked
                        print("New Game selected")
                        next_state = GameState.NEW_GAME
                        running = False  # Exit the welcome screen
                    elif load_game_button.collidepoint(event.pos):  # Check if "Load Game" button is clicked
                        print("Load Game selected")
                        next_state = GameState.MAIN_GAME
                        hero = fileIO.load_game()
                        running = False  # Exit the welcome screen

            pygame.display.update()  # Update the display
        return next_state, hero

    def battle_screen(self, hero:Hero, monster:Monster) -> GameState:
        """Battle screen where the hero fights a monster."""
        running = True
        while running:
            screen.fill(WHITE)

            #Hero Box
            hero_text = f"Name: {hero.name}/nHealth: {hero.health}/nLevel: {hero.level}/nExp: {hero.experience}"
            hero_background = pygame.Rect(5, 5, SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10)
            pygame.draw.rect(screen, BLUE, hero_background, width=2, border_radius=10)
            draw_multiple_lines(hero_text, font, BLACK, screen, 15, 15)

            #Monster Box
            monster_text = f"Monster: {monster.name}/nHealth: {monster.health}/nDamage: {monster.damage}"   
            monster_background = pygame.Rect(SCREEN_WIDTH // 2 + 5, 5, SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10)
            pygame.draw.rect(screen, RED, monster_background, width=2, border_radius=10)
            draw_multiple_lines(monster_text, font, BLACK, screen, SCREEN_WIDTH //2 + 15, 15)

            #Action Box
            action_background = pygame.Rect(5, SCREEN_HEIGHT // 2 + 5, SCREEN_WIDTH - 10, SCREEN_HEIGHT // 2 - 80)
            pygame.draw.rect(screen, GREEN, action_background, width=2, border_radius=10)
            weapon_button = draw_button("Weapon Attack", font, BLUE, screen, 15, SCREEN_HEIGHT // 2 + 20, 200, 50)
            class_button = draw_button("Class Attack", font, BLUE, screen, 15, SCREEN_HEIGHT // 2 + 80, 200, 50)
            protection_button = draw_button("Use Protection", font, BLUE, screen, 245, SCREEN_HEIGHT // 2 + 20, 200, 50)
            flee_button = draw_button("Flee", font, BLUE, screen, 245, SCREEN_HEIGHT // 2 + 80, 200, 50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    next_state = GameState.GAME_OVER
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        next_state = self.show_esc_popup(hero, GameState.BATTLE)
                        if next_state == GameState.GAME_OVER:
                            running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if weapon_button.collidepoint(event.pos):
                        print("Weapon Attack selected")
                        monster.take_damage(hero.equipment.damage)
                        if monster.is_alive():
                            hero.take_damage(monster.damage)
                        else:
                            print(f"{monster.name} defeated!")
                            hero.gain_experience(monster.experience)
                            next_state = GameState.MAIN_GAME
                            running = False
                    if class_button.collidepoint(event.pos):
                        print("Class Attack selected")
                        monster.take_damage(hero.use_special())
                        if monster.is_alive():
                            hero.take_damage(monster.damage)
                        else:
                            print(f"{monster.name} defeated!")
                            hero.gain_experience(monster.experience)
                            next_state = GameState.MAIN_GAME
                            running = False
                    if protection_button.collidepoint(event.pos):
                        print("Use Protection selected")
                    if flee_button.collidepoint(event.pos):
                        print("Flee selected")
                        next_state = GameState.MAIN_GAME
                        running = False

            pygame.display.update()
        return next_state

    def main_game(self, hero:Hero) -> GameState:
        """Main game screen."""
        running = True
        while running:
            screen.fill(WHITE)
            hero_text = f"Name: {hero.name}/nHealth: {hero.health}/nLevel: {hero.level}/nExp: {hero.experience}"
            hero_background = pygame.Rect(5, 5, SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10)
            pygame.draw.rect(screen, BLUE, hero_background, width=2, border_radius=10)
            draw_multiple_lines(hero_text, font, BLACK, screen, 15, 15)
            
            #Action Box
            action_background = pygame.Rect(5, SCREEN_HEIGHT // 2 + 5, SCREEN_WIDTH - 10, SCREEN_HEIGHT // 2 - 80)
            pygame.draw.rect(screen, GREEN, action_background, width=2, border_radius=10)
            battle_button = draw_button("Fight Goblins", font, BLUE, screen, 15, SCREEN_HEIGHT // 2 + 20, 200, 50)
            shop_button = draw_button("Go to Shop", font, BLUE, screen, 15, SCREEN_HEIGHT // 2 + 80, 200, 50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    next_state = GameState.GAME_OVER
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        next_state = self.show_esc_popup(hero, GameState.MAIN_GAME)
                        if next_state == GameState.GAME_OVER:
                            running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if battle_button.collidepoint(event.pos):
                        print("Battle selected")
                        next_state = GameState.BATTLE
                        running = False
            
            pygame.display.update()
        return next_state