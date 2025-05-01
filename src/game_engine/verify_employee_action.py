from src.actions import Action
from src.common.results import ValidationResult
from src.controllers.employeeActionInteractorAdapter import EmployeeActionInteractorAdapter
from src.state.game_state.restaurant_state.restaurant_state import RestaurantState


def verify_employee_action(
    action: Action,
    state: RestaurantState,
    employee_id: str
) -> ValidationResult:
    interactor = EmployeeActionInteractorAdapter().from_restaurant_state(state, employee_id)
    return action.is_valid(interactor)
