import pygame
from src.game.core.constants import GameState
from typing import Tuple, Optional, List, Dict, Any

class EventManager:
    """Manages event handling and processing for the game."""
    
    def __init__(self):
        """Initialize the event manager."""
        self.button_delay_timer = 0
        self.BUTTON_DELAY = 250  # 250ms = 0.25 seconds
        self.key_actions = {
            pygame.K_ESCAPE: "escape",
            pygame.K_BACKSPACE: "backspace",
            pygame.K_RETURN: "enter",
            pygame.K_DELETE: "delete",
            pygame.K_TAB: "tab",
        }
        
    def can_click_buttons(self) -> bool:
        """Check if enough time has passed to allow button clicks."""
        return pygame.time.get_ticks() - self.button_delay_timer >= self.BUTTON_DELAY
        
    def reset_button_delay(self) -> None:
        """Reset the button click delay timer."""
        self.button_delay_timer = pygame.time.get_ticks()
        
    def handle_quit_event(self, event: pygame.event.Event, game_state: GameState) -> Tuple[GameState, bool]:
        """Handle quit event.
        Returns:
            tuple: (new game state, should continue running)
        """
        if event.type == pygame.QUIT:
            return GameState.EXIT, False
        return game_state, True
        
    def handle_keyboard_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle keyboard events.
        Returns:
            str: The key action if any, None otherwise
        """
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_actions:
                return self.key_actions[event.key]
            elif event.unicode and len(event.unicode) == 1 and event.unicode.isprintable():
                return event.unicode
        return None
        
    def handle_button_click(self, event: pygame.event.Event, button_rect: pygame.Rect, is_locked: bool) -> bool:
        """Check if a button was clicked.
        Args:
            event: The pygame event
            button_rect: The button's rectangle
            is_locked: Whether the button is locked
            
        Returns:
            bool: True if button was clicked, False otherwise
        """
        if (event.type == pygame.MOUSEBUTTONDOWN and 
            event.button == 1 and  # Left click only
            self.can_click_buttons() and
            not is_locked and
            button_rect.collidepoint(event.pos)):
            self.reset_button_delay()
            return True
        return False
        
    def handle_text_input(self, event: pygame.event.Event, text_box_rect: pygame.Rect) -> bool:
        """Handle text input events.
        Args:
            event: The pygame event
            text_box_rect: The text box's rectangle
            
        Returns:
            bool: True if text box was clicked, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            return text_box_rect.collidepoint(event.pos)
        return False
        
    def handle_mouse_motion(self, event: pygame.event.Event) -> Tuple[int, int]:
        """Handle mouse motion events.
        Returns:
            tuple: Current mouse position (x, y)
        """
        if event.type == pygame.MOUSEMOTION:
            return event.pos
        return pygame.mouse.get_pos()
        
    def handle_scroll_event(self, event: pygame.event.Event) -> int:
        """Handle scroll wheel events.
        Returns:
            int: Scroll direction (positive up, negative down)
        """
        if event.type == pygame.MOUSEWHEEL:
            return event.y
        return 0
        
    def handle_volume_slider(self, event: pygame.event.Event, volume_rect: pygame.Rect, volume_x: int) -> Optional[float]:
        """Handle volume slider events.
        Args:
            event: The pygame event
            volume_rect: The volume slider rectangle
            volume_x: The x position of the volume slider
            
        Returns:
            float: New volume value between 0 and 1, or None if no change
        """
        if event.type == pygame.MOUSEBUTTONDOWN and volume_rect.collidepoint(event.pos):
            mouse_x = event.pos[0]
            volume = (mouse_x - volume_x) / 300
            return max(0, min(1, volume))  # Clamp between 0 and 1
        elif event.type == pygame.MOUSEMOTION and volume_rect.collidepoint(event.pos):
            mouse_x = event.pos[0]
            volume = (mouse_x - volume_x) / 300
            return max(0, min(1, volume))  # Clamp between 0 and 1
        return None
        
    def handle_popup_events(self, event: pygame.event.Event) -> bool:
        """Handle popup-specific events.
        Returns:
            bool: True if popup should close, False otherwise
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True
        return False
        
    def process_events(self) -> List[pygame.event.Event]:
        """Get and process all current events.
        Returns:
            list: List of pygame events
        """
        return pygame.event.get()
        
    def get_mouse_pos(self) -> Tuple[int, int]:
        """Get current mouse position.
        Returns:
            tuple: Current mouse position (x, y)
        """
        return pygame.mouse.get_pos()
        
    def is_key_pressed(self, key: int) -> bool:
        """Check if a specific key is currently pressed.
        Args:
            key: The pygame key constant to check
            
        Returns:
            bool: True if key is pressed, False otherwise
        """
        return pygame.key.get_pressed()[key]