
from dataclasses import dataclass
from functools import cache
import io
from pathlib import Path
from typing import Dict, List, Tuple

import cairosvg
import pygame
from src.common.position import FPosition
from src.core.types import StationType
from src.tui.canvas.canvas_state import CanvasState
from src.tui.canvas.draw_level import  draw_level
from src.tui.emojis import *

asset_dir = Path("/Users/taylercooper/Dev/openmoji-svg-color")
font = None

def update_canvas(
    surface: pygame.Surface,
    positions: Dict[str, FPosition],
    customer_names: List[str],
    employee_names: List[str],
    station_ids: List[str],
    station_types: Dict[str, StationType],
    floor_plan: List[FPosition],
        ) -> None:

    cell_size = compute_cell_size(surface.width, surface.height, floor_plan)

    surface.fill((90, 90, 90))  # Clear the screen with black
    inner_cell_size = cell_size - 5  # Adjust for borders

    stations: List[Tuple[FPosition, pygame.Surface]] = []
    for station in station_ids:
        stations.append((
            positions[station],
            render_image(get_station_emoji(station_types[station], asset_dir), inner_cell_size, inner_cell_size),
        ))

    npcs: List[Tuple[FPosition, pygame.Surface]] = []
    for name in customer_names + employee_names:
        pos = positions[name]
        image = render_npc(inner_cell_size, get_face_emoji(name, asset_dir), name)
        npcs.append((pos, image))
    draw_level(floor_plan, stations, npcs, surface, inner_cell_size)

@cache
def render_npc(
    cell_size: int,
    image: Path,
    name: str, 
) -> pygame.Surface:
    global font
    if font is None:
        font = pygame.font.Font(None, 32)  # Default font and size, can be customized
    original_image = image
    text = font.render(name, True, (255, 255, 255))

    width, height = cell_size, cell_size
    available_height = height - text.get_height()
    if available_height <= 0:
        # If there's no space for the name, return the original NPC without modification
        return render_image(original_image, cell_size, cell_size)
    scale_factor = available_height / height
    scaled_w = int(width * scale_factor)
    scaled_h = int(height * scale_factor)

    image_x = (width - scaled_w) // 2
    image_y = 0
    result = pygame.Surface((width, height), flags=pygame.SRCALPHA)
    result.fill((0, 0, 0, 0))  # Fill with transparent background
    scaled_image = render_image(original_image, scaled_w, scaled_h)
    result.blit(scaled_image, (image_x, image_y))
    text_x = (width - text.get_width()) // 2
    result.blit(text, (text_x, scaled_h))
    return result



@cache
def render_image(image: Path, width: int, height: int) -> pygame.Surface:
    surface = cairosvg.svg2png(url=image.as_posix(), output_width= width, output_height=height)
    img_io = io.BytesIO(surface)
    return pygame.image.load(img_io).convert_alpha()

def compute_cell_size(width: int, height: int, floor_plan: List[FPosition]) -> int:
    num_rows = max(int(pos.y) for pos in floor_plan)
    num_cols = max(int(pos.x) for pos in floor_plan)
    cell_width = width // (num_cols + 1)
    cell_height = height // (num_rows + 1)
    return min(cell_width, cell_height)