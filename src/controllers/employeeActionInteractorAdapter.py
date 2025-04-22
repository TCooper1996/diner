from src.controllers.EmployeeActionInteractor import EmployeeActionInteractor


class EmployeeActionInteractorAdapter:
    def to_restaurant_state(self, itr: EmployeeActionInteractor):
        return itr.restaurant_state

    def from_restaurant_state(self, restaurant_state, current_employee_id: str) -> EmployeeActionInteractor:
        return EmployeeActionInteractor(restaurant_state=restaurant_state, employee_name=current_employee_id)