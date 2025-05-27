import pygame
from src.game.ui.spritesheet import SpriteSheet
from src.game.core.constants import Colors

BUTTON_DEFUALT = 0
BUTTON_CLICKED = 1
BUTTON_LOCKED  = 2
BUTTON_SELECTED = 3

BUTTON_GRAY   = 0
BUTTON_RED    = 1
BUTTON_GREEN  = 2
BUTTON_BLUE   = 3
BUTTON_YELLOW = 4


class Button():
    def __init__(self, button_sheet:SpriteSheet, x, y, width, height, scale):
        self.button_sheet = button_sheet
        self.width = width
        self.height = height
        self.scale = scale
        self.rect = pygame.rect.Rect((x, y), (width, height))
        self.state = BUTTON_DEFUALT
        self.max_state = self.button_sheet.sheet.get_width() // self.width
        self.was_pressed = False
        self.was_clicked = False
        self.toggled = False
        self.locked = False
        self.visible = True

    def lock(self):
        """Lock the button, preventing interaction."""
        if not self.locked:
            self.state = BUTTON_LOCKED
            self.locked = True
            self.toggled = False

    def unlock(self):
        """Unlock the button, allowing interaction."""
        if self.locked:
            self.state = BUTTON_DEFUALT
            self.locked = False
            self.toggled = False

    def is_locked(self) -> bool:
        """Check if the button is locked."""
        return self.locked

    def hide(self):
        """Make the button invisible."""
        self.visible = False

    def show(self):
        """Make the button visible."""
        self.visible = True

    def is_visible(self) -> bool:
        """Check if the button is visible."""
        return self.visible

    def toggle(self) -> None:
        """Toggle the button state."""
        self.toggled = not self.toggled
        if not self.locked:
            self.state = BUTTON_SELECTED if self.toggled else BUTTON_DEFUALT

    def reset_toggle(self) -> None:
        """Reset the toggle state."""
        self.toggled = False
        if not self.locked:
            self.state = BUTTON_DEFUALT

    def is_toggled(self) -> bool:
        """Check if the button is toggled."""
        return self.toggled
    
    def reset_click(self) -> None:
        """Reset the button's clicked state."""
        self.was_clicked = False
        self.was_pressed = False
        if not self.locked:
            self.state = BUTTON_DEFUALT
    
    def update_state(self) -> None:
        """Update the button's state based on mouse interaction."""
        if self.locked or not self.visible:
            return

        pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]  # Left mouse button only

        if self.rect.collidepoint(pos):
            if mouse_pressed and not self.was_pressed and (self.state == BUTTON_DEFUALT or self.state == BUTTON_SELECTED):
                self.state = BUTTON_CLICKED
                self.was_pressed = True
                self.was_clicked = False
            elif not mouse_pressed and self.was_pressed:
                if self.state == BUTTON_CLICKED:
                    self.was_clicked = True
                self.state = BUTTON_SELECTED if self.toggled else BUTTON_DEFUALT
                self.was_pressed = False
        else:
            # Reset button state when mouse leaves the button area
            if not self.toggled:
                self.state = BUTTON_DEFUALT
            self.was_pressed = False
            self.was_clicked = False
    
    def draw(self, surface:pygame.Surface) -> None:
        """Draw the button if a surface is provided and the button is visible, otherwise just update state."""
        self.update_state()
        
        if surface is not None and self.visible:
            image = self.button_sheet.get_image(self.state, self.width, self.height, self.scale, Colors.BLACK)
            surface.blit(image, (self.rect.x, self.rect.y))

class TextButton(Button):
    def __init__(self, button_sheet:SpriteSheet, x:int, y:int, width:int, height:int, scale:float,
                text:str, font:pygame.font.Font, text_color:tuple=Colors.BLACK):
        super().__init__(button_sheet, x, y, width, height, scale)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.text_surface = self.font.render(text, True, text_color)
        self.locked_surface = self.font.render(self.text, True, Colors.GRAY)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        super().draw(surface)

        if surface is not None and self.visible:
            if self.state == BUTTON_LOCKED:
                surface.blit(self.locked_surface, self.text_rect)
            else:
                surface.blit(self.text_surface, self.text_rect)

    def update_text(self, new_text:str):
        self.text = new_text
        self.text_surface = self.font.render(new_text, True, self.text_color)
        self.locked_surface = self.font.render(new_text, True, Colors.GRAY)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)