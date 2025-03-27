
from dataclasses import dataclass
from typing import ClassVar, Protocol

from src.game_engine.location import Location
from src.infrastructure.navigation.position import Position

@dataclass
class Tile:
    room: Location
    pos: Position
