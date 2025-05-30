import pygame
from typing import Union, Tuple

class Tooltip:
    def __init__(self, text: str, font: pygame.font.Font, text_color: pygame.Color = pygame.Color('black'), padding: Union[int, Tuple[int, int]] = 5) -> None:
        self.text = text
        self.font = font
        self.background_color = pygame.Color('white')
        self.border_color = pygame.Color('black')
        self.text_color = text_color
        
        # Convert padding to a tuple if it's an integer
        if isinstance(padding, int):
            self.padding = (padding, padding)  # (horizontal, vertical)
        else:
            self.padding = padding
            
        self._create_surface()
        
    def _create_surface(self) -> None:
        # Handle multiline text
        lines = self.text.split('\n')
        text_surfaces = [self.font.render(line, True, self.text_color) for line in lines]
        
        # Calculate total width and height needed
        max_width = max(surface.get_width() for surface in text_surfaces)
        total_height = sum(surface.get_height() for surface in text_surfaces)
        line_spacing = 2  # Add small spacing between lines
        
        # Calculate final dimensions including padding
        self.width = max_width + (self.padding[0] * 2)
        self.height = total_height + (self.padding[1] * 2) + (line_spacing * (len(lines) - 1))
        
        # Create surface and fill background
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.background_color)
        
        # Draw border
        pygame.draw.rect(self.surface, self.border_color, (0, 0, self.width, self.height), 1)
        
        # Draw each line of text
        current_y = self.padding[1]
        for surface in text_surfaces:
            self.surface.blit(surface, (self.padding[0], current_y))
            current_y += surface.get_height() + line_spacing
        
    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        screen.blit(self.surface, (x, y)) 