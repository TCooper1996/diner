from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal

from src.core.entities.info import EntityInfo
from src.core.entities.info import *
from src.tui.draw_level.draw_level import LevelEntityWithImage
from src.tui.emojis.get_emoji import get_emoji


@dataclass
class CanvasState:
    entities: List[LevelEntityWithImage]
    width: int 
    height: int
    
    @property
    def num_rows(self) -> int:
        return max([entity.position.y for entity in self.entities], default=0) 
    
    @property
    def num_cols(self) -> int:
        return max([entity.position.x for entity in self.entities], default=0)

    @property
    def cell_width(self) -> int:
        return self.width // (self.num_cols + 1)
    
    @property
    def cell_height(self) -> int:
        return self.height // (self.num_rows  + 1)

    @property
    def CELL_SIZE(self) -> int:
        return min(self.cell_width, self.cell_height)

def create_canvas_state(_entities: List[EntityInfo], asset_dir: Path, width: int, height: int) -> CanvasState:
    entities = []
    for entity in _entities:
        emoji = get_emoji(asset_dir=asset_dir, entity=entity)
        e_type = get_entity_type(entity)
        name = getattr(entity, "name", None)
        entities.append(LevelEntityWithImage(entity.position, emoji, name, e_type))
    return CanvasState(entities, width, height)



def get_entity_type(e: EntityInfo) -> Literal["station", "customer", "employee", "floor"]:
    if isinstance(e, EmployeeInfo):
        return "employee"
    elif isinstance(e, CustomerInfo):
        return "customer"
    elif isinstance(e, StationInfo):
        return "station"
    elif isinstance(e, FloorInfo):
        return "floor"
    else:
        raise ValueError(f"Invalid entity type: {type(e)}")