from dataclasses import dataclass
from typing import Dict, List, Literal, Optional
import pygame

from src.common.position import FPosition
from src.core.entities.info.customer_info import CustomerInfo
from src.core.entities.info.employee_info import EmployeeInfo
from src.tui.draw_level.draw_tile import draw_tile


@dataclass
class LevelEntityWithImage:
    position: FPosition
    image: pygame.Surface
    name: Optional[str]
    e_type: Literal["station", "customer", "employee", "floor"]


def draw_level(surface: pygame.Surface, CELL_SIZE: int, entities: List[LevelEntityWithImage]):
    _entities = [e for e in entities if e.e_type != "floor"]
    floors = [e for e in entities if e.e_type == "floor"]

    # Draw entities first
    tile_groups: Dict[str, List[LevelEntityWithImage]] = {}
    for entity in _entities:
        key = f"{entity.position.x},{entity.position.y}"
        if key not in tile_groups:
            tile_groups[key] = []
        tile_groups[key].append(entity)

    for entity in floors:
        if key not in tile_groups:
            tile_groups[key] = [entity]

    for entities_in_space in tile_groups.values():
        images = [e.image for e in entities_in_space if e.image]
        draw_tile(surface, entities_in_space[0].position, CELL_SIZE, images)
