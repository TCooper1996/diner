from src.common.location import Location, DINING
from src.infrastructure.navigation.floor_plan import FloorPlan
from src.infrastructure.navigation.tiles import Tile

class Navigator:
    def __init__(self, floor_plan: FloorPlan):
        self.floor_plan = floor_plan

    def next_tile(self, current_pos: Tile, destination: Location, steps:int =1) -> Tile:
        return self.floor_plan.get_next_tile(current_pos.pos, destination, steps=steps)
