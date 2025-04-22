from dataclasses import dataclass

from src.common.position import Position


@dataclass
class FloorInfo:
    position: Position