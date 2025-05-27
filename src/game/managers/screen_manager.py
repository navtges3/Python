import pygame
from src.game.core.constants import Colors, GameConstants
from src.game.ui.ui_helpers import draw_text_centered

class ScreenManager:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font):
        self.screen = screen
        self.font = font

    def draw_popup(self, title: str, buttons: dict) -> None:
        """Draw a popup window with title and buttons."""
        # Draw semi-transparent background
        overlay = pygame.Surface((GameConstants.SCREEN_WIDTH, GameConstants.SCREEN_HEIGHT))
        overlay.fill(Colors.BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        # Draw popup window
        popup_rect = pygame.Rect(
            (GameConstants.SCREEN_WIDTH - GameConstants.POPUP_WIDTH) // 2,
            (GameConstants.SCREEN_HEIGHT - GameConstants.POPUP_HEIGHT) // 2,
            GameConstants.POPUP_WIDTH,
            GameConstants.POPUP_HEIGHT
        )
        pygame.draw.rect(self.screen, Colors.WHITE, popup_rect)
        pygame.draw.rect(self.screen, Colors.BLACK, popup_rect, 2)

        # Draw title
        draw_text_centered(
            title,
            self.font,
            Colors.BLACK,
            self.screen,
            GameConstants.SCREEN_WIDTH // 2,
            (GameConstants.SCREEN_HEIGHT - GameConstants.POPUP_HEIGHT) // 2 + 20
        )

        # Draw buttons
        for button in buttons.values():
            button.draw(self.screen) 