
from typing import List

import pygame
from src.tui.canvas.canvas_state import CanvasState
from src.tui.draw_level.draw_level import LevelEntityWithImage, draw_level


def update_canvas(state: CanvasState, surface: pygame.Surface):
    resize_images_if_necessary(state.CELL_SIZE, state.entities)
    surface.fill((90, 90, 90))  # Clear the screen with black
    draw_level(surface, state.CELL_SIZE, state.entities) 

def resize_images_if_necessary(CELL_SIZE: int, entities: List[LevelEntityWithImage]):
    if not entities:
        return
    
    for entity in entities:
        if entity.image.get_size() != (CELL_SIZE, CELL_SIZE):
            entity.image = pygame.transform.smoothscale(entity.image, (CELL_SIZE, CELL_SIZE))