from src.core.types import TileType
from .restaurant_state import RestaurantState
from .entities.employee import Employee


def add_employee(state: RestaurantState, employee: str, instruction: str, location: TileType):
    state.location_manager.add_entity(employee, location) 
    state.entities[employee] = "employee"
    state.employee_instructions[employee] = instruction
    state.employees[employee] = Employee(employee, instruction)