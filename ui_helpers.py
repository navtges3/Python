from constants import *
from items import *
import pygame

class Button:
    def __init__(self, text, pos, size, font:pygame.font, text_color, button_color, hover_color):
        self.text = text
        self.pos = pos
        self.size = size
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.default_color = button_color
        self.default_hover_color = hover_color
        self.selected = False
        self.locked = False

        self.rect = pygame.Rect(pos, size,)
        self.surface = self.font.render(self.text, True, self.text_color)

    def update_text(self, text:str) -> None:
        """Update the button text."""
        self.text = text
        self.surface = self.font.render(self.text, True, self.text_color)

    def lock(self) -> None:
        """Lock the button."""
        self.locked = True
        self.button_color = Colors.GRAY
        self.hover_color = Colors.LIGHT_GRAY

    def unlock(self) -> None:
        """Unlock the button."""
        self.locked = False
        self.button_color = self.default_color
        self.hover_color = self.default_hover_color

    def is_locked(self) -> bool:
        """Check if the button is locked."""
        return self.locked
    
    def select(self) -> None:
        """Select the button."""
        self.selected = True

    def deselect(self) -> None:
        """Deselect the button."""
        self.selected = False

    def get_selected(self) -> bool:
        """Get the selected state of the button."""
        return self.selected
    
    def draw(self, screen, draw_text=True, border_color=Colors.BLACK) -> None:
        # Change color on hover
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect, border_radius=5)
        else:
            pygame.draw.rect(screen, self.button_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, border_color, self.rect, width=2, border_radius=5)

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

def draw_item(item:Item, button:Button, surface, border_color) -> None:
    """Draw an item on the screen."""
    button.draw(surface, False, border_color)
    draw_text(item.name, button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 10)
    if isinstance(item, Weapon):
        draw_text(f"Damage: {item.damage}", button.font, button.text_color,surface, button.pos[0] + 10, button.pos[1] + 40)
    elif isinstance(item, Armor):
        draw_text(f"Block: {item.block}", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 40)
        draw_text(f"Dodge: {item.dodge}", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 70)
        draw_text(f"Duration: {item.duration}", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 100)

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