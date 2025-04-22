from dataclasses import dataclass
from typing import List, Literal

from src.common.position import Position


StationType = Literal["entrance", "dining", "kitchen"]
Stations: List[StationType] = ["entrance", "dining", "kitchen"]
TileType = Literal["floor"] | StationType
TileTypes: List[TileType] = ["floor", "entrance", "dining", "kitchen"]
