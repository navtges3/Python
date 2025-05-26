import pygame
from spritesheet import SpriteSheet
from constants import Colors

BUTTON_DEFUALT = 0
BUTTON_CLICKED = 1
BUTTON_LOCKED  = 2

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

        self.toggled = False
        self.locked = False

    # Handle Button Locking
    def lock(self):
        if not self.locked:
            print('Button Locked')
            self.state = BUTTON_LOCKED

    def unlock(self):
        if self.locked:
            print('Button Unlocked')
            self.state = BUTTON_DEFUALT

    def is_locked(self) -> bool:
        return self.locked

    # Handle Toggle
    def toggle(self) -> None:
        if self.toggled:
            self.toggled = False
        else:
            self.toggled = True
            print('Button Toggled')
    
    def reset_toggle(self) -> None:
        self.toggled = False
        print('Button Toggle Reset')

    def is_toggled(self) -> bool:
        return self.toggled
    
    def draw(self, surface):
        image = None

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.state == BUTTON_DEFUALT:
                print('Clicked')
                self.state = BUTTON_CLICKED
        
        if not pygame.mouse.get_pressed()[0] and self.state == BUTTON_CLICKED:
            print('Unclicked')
            self.state = BUTTON_DEFUALT

        # draw button
        image = self.button_sheet.get_image(self.state, self.width, self.height, self.scale, Colors.BLACK)
        surface.blit(image, (self.rect.x, self.rect.y))

        return self.state
    
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
        button_state = super().draw(surface)

        if self.state == BUTTON_LOCKED:
            surface.blit(self.locked_surface, self.text_rect)
        else:
            surface.blit(self.text_surface, self.text_rect)

        return button_state
    
    def update_text(self, new_text:str):
        self.text = new_text
        self.text_surface = self.font.render(new_text, True, self.text_color)
        self.locked_surface = self.font.render(new_text, True, Colors.GRAY)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)