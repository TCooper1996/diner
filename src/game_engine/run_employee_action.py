import copy
from typing import Tuple
from src.actions import Action
from src.controllers.employeeActionInteractorAdapter import EmployeeActionInteractorAdapter
from src.state.game_state.restaurant_state.restaurant_state import RestaurantState


ActionResultLog = str
def run_employee_action(
        state: RestaurantState,
        employee: str,
        action: Action
) -> Tuple[RestaurantState, Action | None, ActionResultLog]:
    new_state = copy.deepcopy(state)
    interactor = EmployeeActionInteractorAdapter().from_restaurant_state(new_state, employee)
    result = action.execute(interactor)

    new_action = action if result.repeat else None
    return new_state, new_action, result.message
    