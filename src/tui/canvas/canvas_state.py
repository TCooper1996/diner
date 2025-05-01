from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Literal, Protocol

import pygame

from src.common.position import FPosition, Position
from src.core.types import StationType


@dataclass
class CanvasState:
    positions: Dict[str, FPosition]  # Maps entity names to their positions
    images: Dict[str, Path]
    customer_names: List[str]
    employee_names: List[str]
    station_ids: List[str]  # List of station IDs
    station_types: Dict[str, StationType]  # Maps station IDs to their types
    floor_plan: List[FPosition]
    width: int 
    height: int
    
    @property
    def num_rows(self) -> int:
        return max([int(s.y) for s in self.floor_plan], default=0) 
    
    @property
    def num_cols(self) -> int:
        return max([int(s.x) for s in self.floor_plan], default=0)

    @property
    def cell_width(self) -> int:
        return self.width // (self.num_cols + 1)
    
    @property
    def cell_height(self) -> int:
        return self.height // (self.num_rows  + 1)

    @property
    def CELL_SIZE(self) -> int:
        return min(self.cell_width, self.cell_height)
