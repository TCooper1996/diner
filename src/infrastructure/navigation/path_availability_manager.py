from typing import Dict, List, Literal, Protocol, Set
from src.common.location import Location
from src.common.position import Position
from src.infrastructure.navigation.floor_plan import FloorPlan
from src.infrastructure.navigation.tiles import Tile

TileType = Literal["kitchen", "dining", "entrance"]
class ITile(Protocol):
    @property
    def pos(self) -> Position:
        ...

    @property
    def tileType(self) -> TileType:
        ...


class PathAvailabilityManager:
    def __init__(self, floor_plan: List[ITile]):
        self.floor_plan: List[ITile] = floor_plan
        self.occupied_tiles: Set[Position] = {}

    def get_path(self, tileType: TileType):
        available_tiles = [tile for tile in self.floor_plan if tile.room == tileType]
        for tile in available_tiles:
            if tile.pos not in self.occupied_tiles:
                self.occupied_tiles.add(tile.pos)

