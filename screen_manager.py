from constants import *
from ui_helpers import *

class ScreenManager:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw_popup(self, title, buttons, color=Colors.WHITE):
        """Draw a popup window with a title and buttons."""
        popup_x = (GameConstants.SCREEN_WIDTH - GameConstants.POPUP_WIDTH) // 2
        popup_y = (GameConstants.SCREEN_HEIGHT - GameConstants.POPUP_HEIGHT) // 2
        popup_rect = pygame.Rect(popup_x, popup_y, GameConstants.POPUP_WIDTH, GameConstants.POPUP_HEIGHT)

        pygame.draw.rect(self.screen, Colors.WHITE, popup_rect, border_radius=10)
        pygame.draw.rect(self.screen, Colors.BLACK, popup_rect, width=5, border_radius=10)
        draw_text_centered(title, self.font, Colors.BLACK, self.screen, GameConstants.SCREEN_WIDTH // 2, popup_y + 20)

        for button in buttons.values():
            button.draw(self.screen)

    def draw_battle_screen(self, hero, monster, battle_log, buttons: list[Button]):
        button_border = pygame.Rect(
            GameConstants.BATTLE_SCREEN_BUTTON_BORDER_X,
            GameConstants.BATTLE_SCREEN_BUTTON_BORDER_Y,
            GameConstants.BATTLE_SCREEN_BUTTON_BORDER_WIDTH,
            GameConstants.BATTLE_SCREEN_BUTTON_BORDER_HEIGHT
        )
        log_border = pygame.Rect(
            GameConstants.BATTLE_SCREEN_LOG_BORDER_X,
            GameConstants.BATTLE_SCREEN_LOG_BORDER_Y,
            GameConstants.BATTLE_SCREEN_LOG_BORDER_WIDTH,
            GameConstants.BATTLE_SCREEN_LOG_BORDER_HEIGHT
        )
        self.screen.fill(Colors.WHITE)
        hero.draw(self.screen, self.font, 0,  25)
        monster.draw(self.screen, self.font, GameConstants.SCREEN_WIDTH // 2, 25)

        pygame.draw.rect(self.screen, Colors.BLACK, button_border, width=5, border_radius=10)
        pygame.draw.rect(self.screen, Colors.BLACK, log_border, width=5, border_radius=10)

        lines = 0
        for i, log_entry in enumerate(battle_log[-15:]):
            lines += draw_wrapped_text(log_entry, self.font, Colors.BLACK, self.screen, GameConstants.BATTLE_SCREEN_LOG_X, GameConstants.BATTLE_SCREEN_LOG_Y + (i + lines) * self.font.get_linesize(), GameConstants.BATTLE_SCREEN_LOG_WIDTH)

        for button in buttons:
            button.draw(self.screen)