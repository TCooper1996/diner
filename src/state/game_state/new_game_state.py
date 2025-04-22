from typing import Dict

from src.actions.wait import WaitAction
from src.core.types import TileType
from src.infrastructure.navigation.floor_plan import FloorPlan
from src.core.entities.customer import Customer
from src.state.game_state.restaurant_state.managers import LocationManager
from src.state.game_state import restaurant_state as restaurant
from .game_state import GameState
from .restaurant_state.entities import Employee


def new_game_state(employee_instructions: Dict[str, str], level: FloorPlan) -> GameState:
    employees = {n: Employee(name=n, instruction=i, current_action=WaitAction()) for n, i in employee_instructions.items()}
    location_manager = LocationManager(level)
    customer = Customer()
    restaurant_state = restaurant.RestaurantState(
        location_manager=location_manager,
    )
    restaurant.add_customer(restaurant_state, customer, "entrance")  # Ensure the first customer is added
    for e in employees.values():
        restaurant.add_employee(restaurant_state, e.name, e.instruction, "entrance")

    restaurant.initialize_entities(restaurant_state)
    return GameState(restaurant_state=restaurant_state)