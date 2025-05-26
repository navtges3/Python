
import pygame
from constants import Colors
from button import Button

class ScrollableButtons:
    """A scrollable container that manages and displays buttons with scrollbar functionality."""
    
    def __init__(self, x: int, y: int, width: int, height: int, button_height: int, button_spacing: int = 10):
        """Initialize the ScrollableButtons container.
        
        Args:
            x: X position of the container
            y: Y position of the container
            width: Width of the container
            height: Height of the container
            button_height: Height of each button
            button_spacing: Vertical spacing between buttons (default 10)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.scroll_offset = 0
        self.button_height = button_height
        self.button_spacing = button_spacing
        self.buttons: list[Button] = []
        self.selected = None

        # Scrollbar setup
        self.scrollbar_width = 10
        self.scrollbar_rect = pygame.Rect(
            self.rect.right - self.scrollbar_width,
            self.rect.top,
            self.scrollbar_width,
            self.rect.height
        )
        self.scrollbar_handle_rect = pygame.Rect(
            self.rect.right - self.scrollbar_width,
            self.rect.top,
            self.scrollbar_width,
            50  # Initial height, will be adjusted in draw
        )
        self.dragging_scrollbar = False

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle mouse wheel and scrollbar events.
        
        Args:
            event: The pygame event to handle
        """
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset += event.y * 20
            self._clamp_scroll_offset()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.scrollbar_handle_rect.collidepoint(event.pos):
                self.dragging_scrollbar = True
            elif self.rect.collidepoint(event.pos):
                mouse_y = event.pos[1] - self.scroll_offset
                for button in self.buttons:
                    if button.rect.collidepoint(event.pos[0], mouse_y):
                        if self.selected is None:
                            self.selected = self.buttons.index(button)
                            button.toggle()
                        elif button.is_toggled():
                            self.selected = None
                            button.toggle()
                        else:
                            if self.selected is not None and 0 <= self.selected < len(self.buttons):
                                self.buttons[self.selected].toggle()
                            self.selected = self.buttons.index(button)
                            button.toggle()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_scrollbar = False
        elif event.type == pygame.MOUSEMOTION and self.dragging_scrollbar:
            content_height = len(self.buttons) * (self.button_height + self.button_spacing)
            if content_height > self.rect.height:
                movement_ratio = (event.pos[1] - self.rect.top) / self.rect.height
                self.scroll_offset = -movement_ratio * (content_height - self.rect.height)
                self._clamp_scroll_offset()

    def _clamp_scroll_offset(self) -> None:
        """Clamp the scroll offset to prevent scrolling beyond content bounds."""
        content_height = len(self.buttons) * (self.button_height + self.button_spacing)
        min_offset = -max(0, content_height - self.rect.height)
        self.scroll_offset = max(min_offset, min(0, self.scroll_offset))

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the scrollable area, buttons, and scrollbar.
        
        Args:
            surface: The pygame surface to draw on
        """
        # Create a clipping surface for the content
        surface.set_clip(self.rect)

        # Draw buttons
        for i, button in enumerate(self.buttons):
            button.rect.y = self.rect.y + i * (self.button_height + self.button_spacing) + self.scroll_offset
            if self.rect.colliderect(button.rect):
                button.draw(surface)

        surface.set_clip(None)  # Reset clipping

        # Draw scrollbar if needed
        content_height = len(self.buttons) * (self.button_height + self.button_spacing)
        if content_height > self.rect.height:
            # Draw scrollbar background
            pygame.draw.rect(surface, Colors.LIGHT_GRAY, self.scrollbar_rect)

            # Calculate and draw scrollbar handle
            handle_height = max(30, (self.rect.height / content_height) * self.rect.height)
            handle_pos = self.rect.top + (-self.scroll_offset / content_height) * self.rect.height

            self.scrollbar_handle_rect.height = handle_height
            self.scrollbar_handle_rect.top = handle_pos

            # Clamp handle position
            self.scrollbar_handle_rect.clamp_ip(self.scrollbar_rect)

            # Draw handle
            pygame.draw.rect(surface, Colors.GRAY, self.scrollbar_handle_rect)

    def add_button(self, button: Button) -> None:
        """Add a button to the scrollable area.
        
        Args:
            button: The Button instance to add
        """
        button_y = len(self.buttons) * (self.button_height + self.button_spacing)
        button.rect.x = self.rect.x
        button.rect.y = self.rect.y + button_y
        button.rect.width = self.rect.width - self.scrollbar_width
        self.buttons.append(button)

    def remove_button(self, button_index: int) -> None:
        """Remove a button from the scrollable area by index.
        
        Args:
            button_index: The index of the button to remove
        """
        if 0 <= button_index < len(self.buttons):
            # Remove the button
            self.buttons.pop(button_index)
            
            # Reset selected button if needed
            if self.selected == button_index:
                self.selected = None
            elif self.selected is not None and self.selected > button_index:
                self.selected -= 1
            
            # Reposition remaining buttons
            for i, button in enumerate(self.buttons):
                button_y = i * (self.button_height + self.button_spacing)
                button.rect.y = self.rect.y + button_y

    def clear_buttons(self) -> None:
        """Remove all buttons from the scrollable area."""
        self.buttons.clear()
        self.selected = None
        self.scroll_offset = 0
        
    def get_selected_button(self) -> Button | None:
        """Get the currently selected button.
        
        Returns:
            The selected Button instance or None if no button is selected
        """
        if self.selected is not None and 0 <= self.selected < len(self.buttons):
            return self.buttons[self.selected]
        return None
