import pygame
from typing import Optional, Tuple

class TextBox:
    def __init__(self, rect: pygame.Rect, font: pygame.font.Font, placeholder: str = "") -> None:
        self.rect = rect
        self.font = font
        self.text = ""
        self.temp_text = ""
        self.active = False
        self.placeholder = placeholder
        self.color_inactive = pygame.Color('gray')
        self.color_active = pygame.Color('black')
        self.color = self.color_inactive
        self.max_chars = 20

    def handle_event(self, event: pygame.event.Event) -> None:
        if not self.active:
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.text = self.temp_text
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.temp_text = self.temp_text[:-1]
            elif len(self.temp_text) < self.max_chars and event.unicode.isprintable():
                self.temp_text += event.unicode

    def draw(self, screen: pygame.Surface) -> None:
        # Draw the text box
        pygame.draw.rect(screen, self.color_active if self.active else self.color_inactive, self.rect, 2)
        
        # Render text or placeholder
        display_text = self.temp_text if self.active else (self.text or self.placeholder)
        text_surface = self.font.render(display_text, True, self.color_active if (self.active or self.text) else self.color_inactive)
        
        # Center text vertically and align left with padding
        text_x = self.rect.x + 5
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y)) 