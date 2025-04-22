from src.infrastructure.navigation.floor_plan import FloorPlan
from .restaurant_state import RestaurantState
from .managers import LocationManager


def new_restaurant_state(floor_plan: FloorPlan):
    return RestaurantState(LocationManager(floor_plan))