from constants import *
import fileIO
from items import *
from monster import Monster
from hero import Hero
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

        self.rect = pygame.Rect(pos, size,)
        self.surface = self.font.render(self.text, True, self.text_color)

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
        draw_text(f"Cooldown: {item.duration}", button.font, button.text_color, surface, button.pos[0] + 10, button.pos[1] + 100)

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

def draw_health_bar(surface, x:int, y:int, width:int, height:int, health_percentage:float) -> None:
    """Draw a health bar on the screen."""
    if health_percentage < 0:
        health_percentage = 0
    elif health_percentage > 1:
        health_percentage = 1
    health_bar_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, Colors.RED, health_bar_rect)
    health_fill_rect = pygame.Rect(x, y, width * health_percentage, height)
    pygame.draw.rect(surface, Colors.GREEN, health_fill_rect)

def draw_hero(hero:Hero, surface, font, x:int=0, y:int=Game_Constants.SCREEN_HEIGHT // 2) -> None:
    """Draw the hero's information on the surface."""

    # Border
    hero_border = pygame.Rect(x, y, Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT // 2 - 50)
    pygame.draw.rect(surface, Colors.BLUE, hero_border, width=5, border_radius=10)

    # Portrait
    hero_image = pygame.image.load(fileIO.resource_path(f"images\\{hero.image}")).convert()
    hero_image = pygame.transform.scale(hero_image, (100, 100))
    surface.blit(hero_image, (hero_border.x + 10, hero_border.y + 10))

    # Health Bar
    health_bar_width = 90
    health_bar_height = 10
    health_bar_x = hero_border.x + 15
    health_bar_y = hero_border.y + hero_image.get_height() + 15
    health_percentage = hero.health / hero.max_health
    draw_health_bar(surface, health_bar_x, health_bar_y, health_bar_width, health_bar_height, health_percentage)

    # Hero Stats
    hero_text = f"{hero.name}\nLevel: {hero.level}\nExp: {hero.experience}\nGold: {hero.gold}"
    draw_multiple_lines(hero_text, font, Colors.BLACK, surface, hero_border.x + hero_image.get_width() + 10, hero_border.y + 10)

    potion_text = f"Potion Bag:\n -Health Potion: {hero.potion_bag['Health Potion']}\n -Damage Potion: {hero.potion_bag['Damage Potion']}\n -Block Potion: {hero.potion_bag['Block Potion']}"
    draw_multiple_lines(potion_text, font, Colors.BLACK, surface, hero_border.x + hero_border.width // 2 + 10, hero_border.y + 10)

    # Draw the hero's weapon and protection
    if hero.equipment is not None:
        equipment_border = pygame.Rect(hero_border.x + 10, hero_border.y + 140, hero_border.width // 2 - 15, hero_border.height - 150)
        pygame.draw.rect(surface, Colors.LIGHT_RED, equipment_border, width=2, border_radius=10)
        equipment_text = f"{hero.equipment.name}\nDamage {hero.equipment.damage}"
        draw_multiple_lines(equipment_text, font, Colors.BLACK, surface, equipment_border.x + 5, equipment_border.y + 5)
    if hero.protection is not None:
        protection_border = pygame.Rect(hero_border.x + hero_border.width // 2 + 5, hero_border.y + 140, hero_border.width // 2 - 15, hero_border.height - 150)
        pygame.draw.rect(surface, Colors.LIGHT_BLUE, protection_border, width=2, border_radius=10)
        protection_text = f"{hero.protection.name}\nBlock: {hero.protection.block}\nDodge: {hero.protection.dodge}"
        draw_multiple_lines(protection_text, font, Colors.BLACK, surface, protection_border.x + 5, protection_border.y + 5)

def draw_monster(monster:Monster, surface, font, x:int, y:int) -> None:
    """Draw the monster's information on the screen."""
    monster_text = f"{monster.name}\nStrength: {monster.damage}"  
    # Border 
    monster_border = pygame.Rect(x, y, Game_Constants.SCREEN_WIDTH // 2, Game_Constants.SCREEN_HEIGHT // 2 - 50)
    pygame.draw.rect(surface, Colors.RED, monster_border, width=5, border_radius=10)
    # Image
    monster_image = pygame.image.load(fileIO.resource_path(f"images\\{monster.image}")).convert()
    monster_image = pygame.transform.scale(monster_image, (100, 100))
    surface.blit(monster_image, (monster_border.x + 10, monster_border.y + 10))
    
    health_bar_width = 90
    health_bar_height = 10
    health_bar_x = monster_border.x + 15
    health_bar_y = monster_border.y + monster_image.get_height() + 15
    health_percentage = monster.health / monster.start_health
    draw_health_bar(surface, health_bar_x, health_bar_y, health_bar_width, health_bar_height, health_percentage)
    draw_multiple_lines(monster_text, font, Colors.BLACK, surface, monster_border.x + monster_image.get_width() + 10, monster_border.y + 10)

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