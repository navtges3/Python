from hero import Hero
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

# Fonts
font = pygame.font.Font(None, 36)

# This function is used to render text on the screen at a specified position.
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

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

        # Define button rectangles
        new_game_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50)
        load_game_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)

        while running:
            screen.fill(WHITE)  # Fill the screen with white

            # Draw buttons
            pygame.draw.rect(screen, GRAY, new_game_button)
            pygame.draw.rect(screen, GRAY, load_game_button)

            # Draw button text
            draw_text("New Game", font, BLACK, screen, new_game_button.centerx, new_game_button.centery)
            draw_text("Load Game", font, BLACK, screen, load_game_button.centerx, load_game_button.centery)

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

    def main_game(self, hero:Hero) -> GameState:
        """Main game screen."""
        running = True
        while running:
            screen.fill(BLUE)

            draw_text(f"Name: {hero.name}", font, WHITE, screen, 100, 20)
            draw_text(f"Health: {hero.health}", font, WHITE, screen, 100, 50)
            draw_text(f"Level: {hero.level}", font, WHITE, screen, 100, 80)
            draw_text(f"Exp: {hero.experience}", font, WHITE, screen, 100, 110)

            draw_text("Press ESC to quit", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)

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