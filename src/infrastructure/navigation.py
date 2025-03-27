from src.game_engine.location import Location
from src.infrastructure.navigation.floor_plan import FloorPlan
from src.infrastructure.navigation.position import Position


def next_tile(floor_plan: FloorPlan, current_pos: Position, destination: Location) -> Position:
    tiles = floor_plan.get_tiles()
    return floor_plan.get_next_tile(current_pos, destination)