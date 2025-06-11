import pygame
from src.game.ui.spritesheet import SpriteSheet
from src.game.core.constants import Colors
from src.game.ui.tooltip import Tooltip
from typing import Optional, Tuple

# Button states
BUTTON_DEFUALT = 0
BUTTON_HOVER = 1
BUTTON_LOCKED  = 2
BUTTON_SELECTED = 3

class Button():
    def __init__(self, button_sheet: SpriteSheet, x: int, y: int, frame_width: int, frame_height: int, scale: float):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.button_sheet = button_sheet
        self.scale = scale
        self.rect = pygame.rect.Rect((x, y), (int(frame_width * scale), int(frame_height * scale)))

        self.visible = True
        self.state = BUTTON_DEFUALT

        self.tooltip: Optional[Tooltip] = None
    
    def reset(self) -> None:
        """Reset the button, set state to BUTTON_DEFAULT"""
        self.state = BUTTON_DEFUALT

    def lock(self) -> None:
        """Lock the button, preventing interaction."""
        self.state = BUTTON_LOCKED

    def unlock(self) -> None:
        """Unlock the button, allowing interaction."""
        if self.is_locked():
            self.state = BUTTON_DEFUALT

    def is_locked(self) -> bool:
        """
        Check if the button is locked.
        
        Returns:
            True if the button is locked, False otherwise
        """
        return self.state == BUTTON_LOCKED
    
    def select(self) -> None:
        """Set the button state to selected"""
        if not self.is_locked():
            self.state = BUTTON_SELECTED

    def deselect(self) -> None:
        """Set the button state to default"""
        if self.is_selected():
            self.state = BUTTON_DEFUALT

    def is_selected(self) -> bool:
        """Check if the button is selected
        
        Returns:
            True if the button is selected, False otherwise
        """
        return self.state == BUTTON_SELECTED

    def hide(self) -> None:
        """Make the button invisible."""
        self.visible = False

    def show(self) -> None:
        """Make the button visible."""
        self.visible = True

    def is_visible(self) -> bool:
        """
        Check if the button is visible.
        
        Returns:
            True if the button is visible, False otherwise
        """
        return self.visible
    
    def draw(self, surface: Optional[pygame.Surface]):
        """
        Draw the button if a surface is provided and the button is visible.
        
        Args:
            surface: Optional pygame surface to draw on
        """
        mouse_pos = pygame.mouse.get_pos()

        if self.state == BUTTON_DEFUALT and self.rect.collidepoint(mouse_pos):
            self.state = BUTTON_HOVER
        elif self.state == BUTTON_HOVER and not self.rect.collidepoint(mouse_pos):
            self.state = BUTTON_DEFUALT

        if surface is not None and self.visible:
            image = self.button_sheet.get_image(self.state, self.frame_width, self.frame_height, self.scale, Colors.BLACK)
            surface.blit(image, (self.rect.x, self.rect.y))
    
    def draw_tooltip(self, surface: Optional[pygame.Surface]) -> None:
        """
        Draw the tooltip if the mouse is hovering over the button.
        Should be called after all other drawing is complete.
        
        Args:
            surface: Optional pygame surface to draw on
        """
        if surface is not None and self.visible and self.tooltip and self.rect.collidepoint(pygame.mouse.get_pos()):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Position tooltip above the mouse cursor
            tooltip_y = mouse_y - self.tooltip.height - 5
            # Center tooltip horizontally on mouse cursor
            tooltip_x = mouse_x - (self.tooltip.width // 2)
            # Keep tooltip inside screen bounds (assuming surface is screen)
            tooltip_x = max(5, min(surface.get_width() - self.tooltip.width - 5, tooltip_x))
            tooltip_y = max(5, tooltip_y)
            self.tooltip.draw(surface, tooltip_x, tooltip_y)

    def set_tooltip(self, text: str, font: pygame.font.Font, text_color: pygame.Color = pygame.Color('black'), padding: int = 5) -> None:
        """
        Set or update the button's tooltip.

        Args:
            text: Text to display in the tooltip
            font: Font to use for the tooltip text
            text_color: Color of the tooltip text
            padding: Padding around the tooltip text
        """
        self.tooltip = Tooltip(text, font, text_color, padding)

class TextButton(Button):
    """A button that displays text on top of the button graphic."""

    def __init__(self, button_sheet: SpriteSheet, x: int, y: int, frame_width: int, frame_height: int, scale: float,
                text: str, font: pygame.font.Font, text_color: Tuple[int, int, int] = Colors.BLACK) -> None:
        """
        Initialize a new text button.

        Args:
            button_sheet: Spritesheet containing button graphics
            x: X coordinate of the button
            y: Y coordinate of the button
            width: Width of the button
            height: Height of the button
            scale: Scale factor for the button
            text: Text to display on the button
            font: Font to use for the text
            text_color: RGB color tuple for the text
        """
        super().__init__(button_sheet, x, y, frame_width, frame_height, scale)
        self.text: str = text
        self.font: pygame.font.Font = font
        self.text_color: Tuple[int, int, int] = text_color
        self.text_surface: pygame.Surface = self.font.render(text, True, text_color)
        self.locked_surface: pygame.Surface = self.font.render(self.text, True, Colors.GRAY)
        self._update_text_position()

    def _update_text_position(self) -> None:
        """Update the text rectangle to remain centered in the button."""
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface: Optional[pygame.Surface]) -> None:
        """
        Draw the button and its text.
        
        Args:
            surface: Optional pygame surface to draw on
        """
        super().draw(surface)

        if surface is not None and self.visible:
            # Ensure text stays centered even if button rect changes
            self._update_text_position()
            
            if self.state == BUTTON_LOCKED:
                surface.blit(self.locked_surface, self.text_rect)
            else:
                surface.blit(self.text_surface, self.text_rect)

    def update_text(self, new_text: str) -> None:
        """
        Update the button's text.
        
        Args:
            new_text: New text to display on the button
        """
        self.text = new_text
        self.text_surface = self.font.render(new_text, True, self.text_color)
        self.locked_surface = self.font.render(new_text, True, Colors.GRAY)
        self._update_text_position()