from constants import *
from items import *
import fileIO
import pygame
import random

class Tooltip:
    def __init__(self, text: str, font: pygame.font.Font):
        self.text = text
        self.font = font
        self.padding = 5
        self.background_color = Colors.LIGHT_GRAY
        self.text_color = Colors.BLACK
        
    def draw(self, surface: pygame.Surface, x: int, y: int):
        lines = self.text.split('\n')
        width = max(self.font.size(line)[0] for line in lines)
        height = self.font.get_linesize() * len(lines)
        
        # Draw background
        pygame.draw.rect(surface, self.background_color,
                        (x, y, width + self.padding * 2,
                         height + self.padding * 2))
        draw_multiple_lines(self.text, self.font, self.text_color, surface, x + 5, y + 5)

class Button:
    def __init__(self, text, pos, size, font:pygame.font, text_color, color:Colors=None, background_image_path=None, hover_image_path=None):
        self.text = text
        self.pos = pos
        self.size = size
        self.font = font
        self.text_color = text_color
        self.selected = False
        self.locked = False
        self.background_image = None
        self.hover_image = None
        self.locked_image = None
        

        random_num = random.choice(range(0, 5))
        color_text = "gray"
        if color:
            if color == Colors.BLUE:
                color_text = "blue"
            elif color == Colors.GREEN:
                color_text = "green"
            elif color == Colors.RED:
                color_text = "red"
            elif color == Colors.YELLOW:
                color_text = "yellow"                
            
        if background_image_path is None:
            background_image_path  = f"images\\buttons\\{color_text}\\button_{random_num}_background.png"
        if hover_image_path is None:
            hover_image_path = f"images\\buttons\\{color_text}\\button_{random_num}_hover.png"
        self.background_image_path = background_image_path
        self.hover_image_path = hover_image_path
        self.locked_image_path = f"images\\buttons\\gray\\button_{random_num}_hover.png"

        self.rect = pygame.Rect(pos, size)
        self.surface = self.font.render(self.text, True, self.text_color)

    def update_text(self, text:str) -> None:
        """Update the button text."""
        self.text = text
        self.surface = self.font.render(self.text, True, self.text_color)

    def update_pos(self, pos) -> None:
        self.rect = pygame.Rect(pos, self.size)

    def lock(self) -> None:
        """Lock the button."""
        if not self.locked:
            print(f"{self.text} Locked")
            self.locked = True

    def unlock(self) -> None:
        """Unlock the button."""
        if self.locked:
            print(f"{self.text} Unlocked")
            self.locked = False

    def is_locked(self) -> bool:
        """Check if the button is locked."""
        return self.locked
    
    def select(self) -> None:
        """Select the button."""
        if not self.selected:
            print(f"{self.text} selected")
            self.selected = True

    def deselect(self) -> None:
        """Deselect the button."""
        if self.selected:
            print(f"{self.text} deselected")
            self.selected = False

    def is_selected(self) -> bool:
        """Get the selected state of the button."""
        return self.selected
    
    def load_background(self) -> None:
        if self.background_image_path and not self.background_image:
            try:
                self.background_image = pygame.image.load(fileIO.resource_path(self.background_image_path)).convert_alpha()
                self.background_image = pygame.transform.scale(self.background_image, self.size)
            except Exception as e:
                print(f"Failed to load button image: {e}")
                self.background_image = None
        if self.hover_image_path and not self.hover_image:
            try:
                self.hover_image = pygame.image.load(fileIO.resource_path(self.hover_image_path)).convert_alpha()
                self.hover_image = pygame.transform.scale(self.hover_image, self.size)
            except Exception as e:
                print(f"Failed to load button image: {e}")
                self.hover_image = None
        if self.locked_image_path and not self.locked_image:
            try:
                self.locked_image = pygame.image.load(fileIO.resource_path(self.locked_image_path)).convert_alpha()
                self.locked_image = pygame.transform.scale(self.locked_image, self.size)
            except Exception as e:
                print(f"Failed to load locked button image: {e}")
                self.locked_image = None
    
    def draw(self, screen, draw_text=True, border_color=Colors.BLACK) -> None:
        # Change color on hover
        mouse_pos = pygame.mouse.get_pos()
        if self.locked:
            screen.blit(self.locked_image, self.rect)
        elif self.background_image and self.hover_image:
            if self.rect.collidepoint(mouse_pos):
                screen.blit(self.hover_image, self.rect)
            else:
                screen.blit(self.background_image, self.rect)
        else:
            if self.rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, Colors.LIGHT_GRAY, self.rect, border_radius=5)
            else:
                pygame.draw.rect(screen, Colors.GRAY, self.rect, border_radius=5)
            pygame.draw.rect(screen, border_color, self.rect, width=2, border_radius=5)

        if self.selected:
            pygame.draw.rect(screen, Colors.GREEN, self.rect, width=5, border_radius=5)

        # Center text on button
        if draw_text:
            text_rect = self.surface.get_rect(center=self.rect.center)
            screen.blit(self.surface, text_rect)

    def is_clicked(self, event):
        # Check if button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
class ScrollableArea:
    def __init__(self, x, y, width, height, button_height, font, text_color, button_spacing=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.scroll_offset = 0
        self.button_height = button_height
        self.button_spacing = button_spacing
        self.buttons: list[Button] = []
        self.font = font
        self.text_color = text_color
        self.selected = None

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
            50 # Initial height, will be adjusted in draw
        )
        self.dragging_scrollbar = False

    def handle_event(self, event):
        """Handle mouse wheel and scrollbar events."""
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset += event.y * 20
            self._clamp_scroll_offset()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.scrollbar_handle_rect.collidepoint(event.pos):
                self.dragging_scrollbar = True
            elif self.rect.collidepoint(event.pos):
                for button in self.buttons:
                    if button.is_clicked(event):
                        if self.selected is None:
                            self.selected = self.buttons.index(button)
                            button.select()
                        elif button.is_selected():
                            self.selected = None
                            button.deselect()
                        else:
                            self.buttons[self.selected].deselect()
                            self.selected = self.buttons.index(button)
                            button.select()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_scrollbar = False
        elif event.type == pygame.MOUSEMOTION and self.dragging_scrollbar:
            # Calculate scroll position based on mouse movement
            content_height = len(self.buttons) * (self.button_height + self.button_spacing)
            if content_height > self.rect.height:
                movement_ratio = (event.pos[1] - self.rect.top) / self.rect.height
                self.scroll_offset = -movement_ratio * (content_height - self.rect.height)
                self._clamp_scroll_offset()

    def _clamp_scroll_offset(self):
        content_height = len(self.buttons) * (self.button_height + self.button_spacing)
        min_offset = -max(0, content_height - self.rect.height)
        self.scroll_offset = max(min_offset, min(0, self.scroll_offset))

    def draw(self, surface):
        """Draw the scrollable area, its buttons, and the scrollbar."""
        # Create a clipping surface for the content
        surface.set_clip(self.rect)

        # Draw buttons
        for button in self.buttons:
            button.rect.y = self.rect.y + self.buttons.index(button) * (self.button_height + self.button_spacing) + self.scroll_offset
            if self.rect.colliderect(button.rect):
                button.draw(surface)
        
        surface.set_clip(None) # Reset clipping

        # Draw scrollbar background
        pygame.draw.rect(surface, Colors.LIGHT_GRAY, self.scrollbar_handle_rect)

        # Calculate and draw scrollbar handle
        content_height = len(self.buttons) * (self.button_height + self.button_spacing)
        if content_height > self.rect.height:
            # Calculate handle size and position
            handle_height = max(30, (self.rect.height / content_height) * self.rect.height)
            handle_pos = self.rect.top + (-self.scroll_offset / content_height) * self.rect.height

            self.scrollbar_handle_rect.height = handle_height
            self.scrollbar_handle_rect.top = handle_pos

            # Clamp handle position
            self.scrollbar_handle_rect.clamp_ip(self.scrollbar_rect)

            # Draw handle
            pygame.draw.rect(surface, Colors.GRAY, self.scrollbar_handle_rect)

    def add_button(self, text:str=""):
        """Add a button to the scrollable area."""
        button_y = len(self.buttons) * (self.button_height + self.button_spacing)
        button = Button(
            text,
            (self.rect.x, self.rect.y + button_y),
            (self.rect.width, self.button_height),
            self.font,
            self.text_color,
        )
        self.buttons.append(button)
    
    def add_button(self, button:Button):
        button_y = len(self.buttons) * (self.button_height + self.button_spacing)
        button.pos = (self.rect.x, self.rect.y + button_y)
        self.buttons.append(button)
        
    def remove_button(self, button_index: int) -> None:
        """Remove a button from the scrollable area by index."""
        if 0 <= button_index < len(self.buttons):
            # Remove the button
            self.buttons.pop(button_index)
            
            # Reset selected button if needed
            if self.selected == button_index:
                self.selected = None
            elif self.selected and self.selected > button_index:
                self.selected -= 1
            
            # Reposition remaining buttons
            for i, button in enumerate(self.buttons):
                button_y = i * (self.button_height + self.button_spacing)
                button.pos = (self.rect.x, self.rect.y + button_y)
                button.rect = pygame.Rect(button.pos, button.size)

def draw_item(item:Item, button:Button, surface, border_color) -> None:
    """Draw an item on the screen."""
    button.draw(surface, False, border_color)
    draw_text(item.name, button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 10)
    if isinstance(item, Weapon):
        draw_text(f"Damage: {item.damage}", button.font, button.text_color,surface, button.pos[0] + 10, button.pos[1] + 40)
    elif isinstance(item, Armor):
        draw_text(f"Block: {item.block}", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 40)
        draw_text(f"Block %: {item.block_chance:.1%}", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 70)
        draw_text(f"Dodge %: {item.dodge_chance:.1%}", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 100)

    draw_text(f"Cost: {item.value}G", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 130)

def draw_text(text:str, font:pygame.font, color:tuple, surface, x:int, y:int) -> None:
    """Draw text on the screen at the specified position."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)

def draw_text_centered(text:str, font:pygame.font, color:tuple, surface, x:int, y:int) -> None:
    """Draw centered text on the screen at the specified position."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def draw_wrapped_text(text:str, font:pygame.font, color:tuple, surface, x:int, y:int, max_width:int) -> int:
    """Draw wrapped text on the screen at the specified position."""
    words = text.split(' ')
    wrapped_lines = []
    current_line = ""

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
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y + i * font.get_linesize()))
    return i

def draw_multiple_lines(text:str, font:pygame.font, color:tuple, surface, x:int, y:int) -> None:
    """Draw multiple lines of text on the screen at the specified position."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        draw_text(line, font, color, surface, x, y + i * 30)

def draw_health_bar(surface, font:pygame.font, x:int, y:int, width:int, height:int, health_low:int, health_high:int) -> None:
    """Draw a health bar on the screen."""
    health_percentage = health_low / health_high if health_high > 0 else 0
    if health_percentage < 0:
        health_percentage = 0
    elif health_percentage > 1:
        health_percentage = 1
    health_bar_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, Colors.RED, health_bar_rect)
    health_fill_rect = pygame.Rect(x, y, width * health_percentage, height)
    pygame.draw.rect(surface, Colors.GREEN, health_fill_rect)
    draw_text_centered(f"{health_low}/{health_high}", font, Colors.BLACK, surface, x + width // 2, y + height // 2 + 2)

def draw_popup(title:str, buttons:dict[str, callable], surface, font) -> None:
    """Draw a popup window with a title and buttons."""
    popup_x = (Game_Constants.SCREEN_WIDTH - Game_Constants.POPUP_WIDTH) // 2
    popup_y = (Game_Constants.SCREEN_HEIGHT - Game_Constants.POPUP_HEIGHT) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, Game_Constants.POPUP_WIDTH, Game_Constants.POPUP_HEIGHT)

    pygame.draw.rect(surface, Colors.WHITE, popup_rect, border_radius=10)
    pygame.draw.rect(surface, Colors.BLACK, popup_rect, width=5, border_radius=10)
    draw_text_centered(title, font, Colors.BLACK, surface, Game_Constants.SCREEN_WIDTH // 2, popup_y + 20)

    for button in buttons.values():
        button.draw(surface)