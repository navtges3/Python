from src.game.core.constants import *
from src.game.entities.items import *
from src.game.utils.fileIO import *
import pygame
import random
from typing import List, Optional, Tuple, Union

from src.game.ui.button import Button

class Tooltip:
    """A class for displaying tooltips with text."""

    def __init__(self, text: str, font: pygame.font.Font) -> None:
        """
        Initialize a tooltip.

        Args:
            text: Text to display in the tooltip
            font: Font to use for rendering text
        """
        self.text: str = text
        self.font: pygame.font.Font = font
        self.padding: int = 5
        self.background_color: Tuple[int, int, int] = Colors.LIGHT_GRAY
        self.text_color: Tuple[int, int, int] = Colors.BLACK
        
    def draw(self, surface: pygame.Surface, x: int, y: int) -> None:
        """
        Draw the tooltip on the surface.

        Args:
            surface: Surface to draw on
            x: X coordinate to draw at
            y: Y coordinate to draw at
        """
        lines: List[str] = self.text.split('\n')
        width: int = max(self.font.size(line)[0] for line in lines)
        height: int = self.font.get_linesize() * len(lines)
        
        # Draw background
        pygame.draw.rect(surface, self.background_color,
                        (x, y, width + self.padding * 2,
                         height + self.padding * 2))
        draw_multiple_lines(self.text, self.font, self.text_color, surface, x + 5, y + 5)

def draw_item(item: Item, button: Button, surface: pygame.Surface, border_color: Tuple[int, int, int]) -> None:
    """
    Draw an item on the screen.

    Args:
        item: Item to draw
        button: Button to draw the item on
        surface: Surface to draw on
        border_color: Color of the button border
    """
    button.draw(surface, False, border_color)
    draw_text(item.name, button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 10)
    if isinstance(item, Weapon):
        draw_text(f"Damage: {item.damage}", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 40)
    elif isinstance(item, Armor):
        draw_text(f"Block: {item.block}", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 40)
        draw_text(f"Block %: {item.block_chance:.1%}", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 70)
        draw_text(f"Dodge %: {item.dodge_chance:.1%}", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 100)

    draw_text(f"Cost: {item.value}G", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 130)

def draw_text(text: str, font: pygame.font.Font, color: Tuple[int, int, int], surface: pygame.Surface, x: int, y: int) -> None:
    """
    Draw text on the screen at the specified position.

    Args:
        text: Text to draw
        font: Font to use for rendering
        color: RGB color tuple for the text
        surface: Surface to draw on
        x: X coordinate to draw at
        y: Y coordinate to draw at
    """
    textobj: pygame.Surface = font.render(text, True, color)
    textrect: pygame.Rect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)

def draw_text_centered(text: str, font: pygame.font.Font, color: Tuple[int, int, int], surface: pygame.Surface, x: int, y: int) -> None:
    """
    Draw centered text on the screen at the specified position.

    Args:
        text: Text to draw
        font: Font to use for rendering
        color: RGB color tuple for the text
        surface: Surface to draw on
        x: X coordinate of center
        y: Y coordinate of center
    """
    textobj: pygame.Surface = font.render(text, True, color)
    textrect: pygame.Rect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def draw_wrapped_text(text: str, font: pygame.font.Font, color: Tuple[int, int, int], surface: pygame.Surface, x: int, y: int, max_width: int) -> int:
    """
    Draw wrapped text on the screen at the specified position.

    Args:
        text: Text to draw
        font: Font to use for rendering
        color: RGB color tuple for the text
        surface: Surface to draw on
        x: X coordinate to draw at
        y: Y coordinate to draw at
        max_width: Maximum width in pixels before wrapping

    Returns:
        Number of lines drawn
    """
    words: List[str] = text.split(' ')
    wrapped_lines: List[str] = []
    current_line: str = ""

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
        text_surface: pygame.Surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y + i * font.get_linesize()))
    return i

def draw_multiple_lines(text: str, font: pygame.font.Font, color: Tuple[int, int, int], surface: pygame.Surface, x: int, y: int) -> None:
    """
    Draw multiple lines of text on the screen at the specified position.

    Args:
        text: Text to draw (lines separated by newlines)
        font: Font to use for rendering
        color: RGB color tuple for the text
        surface: Surface to draw on
        x: X coordinate to draw at
        y: Y coordinate to draw at
    """
    lines: List[str] = text.split("\n")
    for i, line in enumerate(lines):
        draw_text(line, font, color, surface, x, y + i * 30)

def draw_health_bar(surface: pygame.Surface, font: pygame.font.Font, x: int, y: int, width: int, height: int, health_low: int, health_high: int) -> None:
    """
    Draw a health bar on the screen.

    Args:
        surface: Surface to draw on
        font: Font to use for rendering text
        x: X coordinate to draw at
        y: Y coordinate to draw at
        width: Width of the health bar
        height: Height of the health bar
        health_low: Current health value
        health_high: Maximum health value
    """
    health_percentage: float = health_low / health_high if health_high > 0 else 0
    if health_percentage < 0:
        health_percentage = 0
    elif health_percentage > 1:
        health_percentage = 1
    health_bar_rect: pygame.Rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, Colors.RED, health_bar_rect)
    health_fill_rect: pygame.Rect = pygame.Rect(x, y, width * health_percentage, height)
    pygame.draw.rect(surface, Colors.GREEN, health_fill_rect)
    draw_text_centered(f"{health_low}/{health_high}", font, Colors.BLACK, surface, x + width // 2, y + height // 2 + 2)

class TextBox:
    """A text box that handles keyboard input with persistent text."""
    
    def __init__(self, rect: pygame.Rect, font: pygame.font.Font, placeholder: str = "") -> None:
        """
        Initialize the text box.
        
        Args:
            rect: The rectangle defining the position and size of the text box
            font: The font to use for rendering text
            placeholder: Text to display when the text box is empty
        """
        self.rect: pygame.Rect = rect
        self.font: pygame.font.Font = font
        self.placeholder: str = placeholder
        self.text: str = ""
        self.temp_text: str = ""  # Stores temporary text while active
        self.active: bool = False
        self.background_color: Tuple[int, int, int] = Colors.WHITE
        self.border_color: Tuple[int, int, int] = Colors.GRAY
        self.text_color: Tuple[int, int, int] = Colors.BLACK
        self.placeholder_color: Tuple[int, int, int] = Colors.LIGHT_GRAY
        self.active_border_color: Tuple[int, int, int] = Colors.BLUE
        self.padding: int = 5
        
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle pygame events for text input.
        
        Args:
            event: The event to handle
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state when clicked
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.temp_text = self.text  # Store current text
            else:
                self.active = False
                self.text = self.temp_text  # Save the temporary text
                self.temp_text = ""  # Clear temporary text buffer
                
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.text = self.temp_text  # Save the temporary text
                self.temp_text = ""  # Clear temporary text buffer
            elif event.key == pygame.K_BACKSPACE:
                self.temp_text = self.temp_text[:-1]
            else:
                # Add character to temp_text if it's a printable character
                if event.unicode.isprintable():
                    self.temp_text += event.unicode
                    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the text box on the screen.
        
        Args:
            surface: The surface to draw on
        """
        # Draw background and border
        pygame.draw.rect(surface, self.background_color, self.rect)
        pygame.draw.rect(surface, 
                        self.active_border_color if self.active else self.border_color, 
                        self.rect, 
                        2)
        
        # Draw text or placeholder
        display_text: str = self.temp_text if self.active else self.text
        if not display_text and not self.active and self.placeholder:
            # Draw placeholder text
            text_surface: pygame.Surface = self.font.render(self.placeholder, True, self.placeholder_color)
        else:
            # Draw actual text
            text_surface: pygame.Surface = self.font.render(display_text, True, self.text_color)
            
        # Position text in the center of the box
        text_rect: pygame.Rect = text_surface.get_rect(
            center=(self.rect.x + self.rect.width // 2,
                   self.rect.y + self.rect.height // 2)
        )
        surface.blit(text_surface, text_rect)