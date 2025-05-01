
from typing import List
import pygame

from src.common.position import FPosition

def render_floor(CELL_SIZE: int) -> pygame.Surface:
    # Subtract 1 to account for the border
    surface = pygame.Surface(size=(CELL_SIZE-1, CELL_SIZE-1), flags=pygame.SRCALPHA)
    pygame.draw.rect(surface, (50, 50, 50), surface.get_rect(), 1)
    return surface

def draw_station(surface: pygame.Surface, pos: FPosition, CELL_SIZE: int, img: pygame.Surface):
    (x, y) = (pos.x * CELL_SIZE, pos.y * CELL_SIZE)
    cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

    # Draw station emoji
    img_rect = img.get_rect(center=cell_rect.center)
    surface.blit(img, img_rect)

def render_crowd(CELL_SIZE: int, emoji_imgs: List[pygame.Surface]) -> pygame.Surface:
    # Draw cell border.
    surface = pygame.Surface(size=(CELL_SIZE, CELL_SIZE), flags=pygame.SRCALPHA)
    if not emoji_imgs:
        return surface

    if len(emoji_imgs) == 1:
        # Draw single emoji image centered in the cell.
        return emoji_imgs[0]
    else:
        # For multiple emojis, divide the cell into quadrants.
        quadrant_width = CELL_SIZE // 2
        quadrant_height = CELL_SIZE // 2
        positions = [
            (0, 0),  # top-left
            (0 + quadrant_width, 0),  # top-right
            (0, 0 + quadrant_height),  # bottom-left
            (0 + quadrant_width, 0 + quadrant_height)  # bottom-right
        ]
        for i, img in enumerate(emoji_imgs[:4]):
            # Scale it to fit in the quadrant.
            quad_img = pygame.transform.smoothscale(img, (quadrant_width, quadrant_height))
            quad_rect = quad_img.get_rect(center=(positions[i][0] + quadrant_width // 2,
                                                   positions[i][1] + quadrant_height // 2))
            surface.blit(quad_img, quad_rect)
    return surface