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
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# This function is used to render text on the screen at a specified position.
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x, y))
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
            hero_text = f"Name: {hero.name}/nHealth: {hero.health}/nLevel: {hero.level}/nExp: {hero.experience}"
            monster_text = f"Monster: {monster.name}/nHealth: {monster.health}/nDamage: {monster.damage}"

            hero_background = pygame.Rect(5, 5, SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10)
            monster_background = pygame.Rect(SCREEN_WIDTH // 2 + 5, 5, SCREEN_WIDTH // 2 - 10, SCREEN_HEIGHT // 2 - 10)

            pygame.draw.rect(screen, BLUE, hero_background)
            pygame.draw.rect(screen, RED, monster_background)

            draw_multiple_lines(hero_text, font, BLACK, screen, 50, 50)
            draw_multiple_lines(monster_text, font, BLACK, screen, SCREEN_WIDTH //2 + 50, 50)

            draw_text("Press ESC to quit", font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    next_state = GameState.GAME_OVER
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        next_state = GameState.GAME_OVER
                        running = False

            pygame.display.update()
        return next_state

    def main_game(self, hero:Hero) -> GameState:
        """Main game screen."""
        running = True
        while running:
            screen.fill(WHITE)
            hero_text = f"Name: {hero.name}/nHealth: {hero.health}/nLevel: {hero.level}/nExp: {hero.experience}"

            draw_multiple_lines(hero_text, font, BLACK, screen, 50, 50)
            
            battle_button = draw_button("Battle", font, BLUE, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50)

            draw_text("Press ESC to quit", font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    next_state = GameState.GAME_OVER
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        next_state = GameState.GAME_OVER
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if battle_button.collidepoint(event.pos):
                        print("Battle selected")
                        next_state = GameState.BATTLE
                        running = False
            
            pygame.display.update()
        return next_state