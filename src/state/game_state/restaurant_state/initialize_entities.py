
from src.core.types import Stations
from .restaurant_state import RestaurantState


def initialize_entities(state: RestaurantState):
    # seats
    for t in Stations:
        tiles = state.location_manager.get_positions_of_tile_type(t)
        for tile in tiles:
            id = f"{t}_{str(tile)}"
            state.location_manager.add_entity(id, tile)
            state.station_manager.add_station(id, t)