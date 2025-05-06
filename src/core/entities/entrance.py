from dataclasses import dataclass

from src.common.position import Position


@dataclass
class Entrance:
    entrance_id: str
    position: Position
