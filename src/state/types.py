from dataclasses import dataclass
from typing import Union

from src.common.position import Position


@dataclass
class DrawableStation:
    position: Position

@dataclass
class DrawableEntity:
    position: Position
    name: str
    last_action: str


Drawable = Union[DrawableStation, DrawableEntity]