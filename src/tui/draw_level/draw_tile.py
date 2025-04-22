
from typing import List
import pygame

from src.common.position import FPosition


def draw_tile(surface: pygame.Surface, pos: FPosition, CELL_SIZE: int, emoji_imgs: List[pygame.Surface]):
    (x, y) = (pos.x * CELL_SIZE, pos.y * CELL_SIZE + 50)
    cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    # Draw cell border.
    pygame.draw.rect(surface, (50, 50, 50), cell_rect, 10)
    
    if not emoji_imgs:
        return

    if len(emoji_imgs) == 1:
        # Draw single emoji image centered in the cell.
        img = emoji_imgs[0]
        img_rect = img.get_rect(center=cell_rect.center)
        surface.blit(img, img_rect)
    else:
        # For multiple emojis, divide the cell into quadrants.
        quadrant_width = CELL_SIZE // 2
        quadrant_height = CELL_SIZE // 2
        positions = [
            (x, y),  # top-left
            (x + quadrant_width, y),  # top-right
            (x, y + quadrant_height),  # bottom-left
            (x + quadrant_width, y + quadrant_height)  # bottom-right
        ]
        for i, img in enumerate(emoji_imgs[:4]):
            # Scale it to fit in the quadrant.
            quad_img = pygame.transform.smoothscale(img, (quadrant_width, quadrant_height))
            quad_rect = quad_img.get_rect(center=(positions[i][0] + quadrant_width // 2,
                                                   positions[i][1] + quadrant_height // 2))
            surface.blit(quad_img, quad_rect)