
from dataclasses import dataclass
from typing import TypeVar

from src.common.position import Position

T = TypeVar("T", bound=str) 
@dataclass
class Tile[T]:
    tileType: T
    pos: Position
