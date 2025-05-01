from dataclasses import dataclass
from typing import Dict, List, Literal, Optional, Protocol, Tuple, TypedDict
import pygame

from src.common.position import FPosition
from src.core.entities.info.customer_info import CustomerInfo
from src.core.entities.info.employee_info import EmployeeInfo
from src.core.types import StationType
from src.tui.canvas.draw_tile import *



def draw_level(floor_positions: List[FPosition], stations: List[Tuple[FPosition, pygame.Surface]], npcs: List[Tuple[FPosition, pygame.Surface]],  surface: pygame.Surface, CELL_SIZE: int):
    @dataclass
    class DrawnEntity:
        position: FPosition
        image: pygame.Surface

    rows = max(p.y for p in floor_positions) + 1
    cols = max(p.x for p in floor_positions) + 1
    # Draw floors
    rendered_floors = [DrawnEntity(p, render_floor(CELL_SIZE)) for p in floor_positions]

    # Draw stations
    rendered_stations = [DrawnEntity(pos, img) for (pos, img) in stations]
    
    # Draw customers and employees

    
    # Draw entities first
    tile_groups: Dict[str, List[Tuple[FPosition, pygame.Surface]]] = {}
    for (position, image) in npcs:
        key = f"{position.x},{position.y}"
        if key not in tile_groups:
            tile_groups[key] = []
        tile_groups[key].append((position, image))

    rendered_crowds = []
    for entities_in_space in tile_groups.values():
        images = [e[1] for e in entities_in_space]
        rendered_crowds.append(DrawnEntity(entities_in_space[0][0], render_crowd(CELL_SIZE, images)))


    # Combine all drawn entities
    drawn_entities = rendered_floors + rendered_stations + rendered_crowds
    t_surface = pygame.Surface((CELL_SIZE * cols, CELL_SIZE * rows))
    t_surface.fill(pygame.Color(00, 00, 00, 255))  # Fill with transparent color
    # Draw all entities on the surface
    for entity in drawn_entities:
        t_surface.blit(entity.image, (entity.position.x * CELL_SIZE, entity.position.y * CELL_SIZE))

    t_rect = t_surface.get_rect()
    t_rect.center = surface.get_rect().center
    surface.blit(t_surface, t_rect)
