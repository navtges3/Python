import pygame

class Tooltip:
    def __init__(self, text: str, font: pygame.font.Font, padding: int = 5) -> None:
        self.text = text
        self.font = font
        self.padding = padding
        self.background_color = pygame.Color('white')
        self.border_color = pygame.Color('black')
        self.text_color = pygame.Color('black')
        self._create_surface()
        
    def _create_surface(self) -> None:
        text_surface = self.font.render(self.text, True, self.text_color)
        self.width = text_surface.get_width() + (self.padding * 2)
        self.height = text_surface.get_height() + (self.padding * 2)
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.background_color)
        pygame.draw.rect(self.surface, self.border_color, (0, 0, self.width, self.height), 1)
        self.surface.blit(text_surface, (self.padding, self.padding))
        
    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        screen.blit(self.surface, (x, y)) 