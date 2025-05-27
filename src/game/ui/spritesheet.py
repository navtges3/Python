import pygame
from typing import Tuple

class SpriteSheet:
    """A class to handle sprite sheets and extract individual sprites."""
    
    def __init__(self, image: pygame.Surface) -> None:
        """Initialize the sprite sheet.
        
        Args:
            image: The sprite sheet surface containing all sprites
        """
        self.sheet = image

    def get_image(self, frame: int, width: int, height: int, scale: float, color: Tuple[int, int, int]) -> pygame.Surface:
        """Extract a single sprite from the sprite sheet.
        
        Args:
            frame: The frame number to extract (0-based index)
            width: The width of each sprite in pixels
            height: The height of each sprite in pixels
            scale: Scale factor to resize the sprite
            color: RGB color tuple to use as transparency key
            
        Returns:
            A new Surface containing the extracted and processed sprite
        """
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image