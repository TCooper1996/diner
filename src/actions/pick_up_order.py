from pydantic import BaseModel, Field

from src.core.models.Action import ActionResult, ValidationResult
from src.core.models.RestaurantState import RestaurantState
from src.core.entities.order import OrderStatus


class PickUpOrder(BaseModel):
    """
    Adds a nearby order to your inventory.
    You must be in the kitchen to pick up an order.
    You can only pick up orders that are ready.
    """
    order_id: str = Field(..., description="The ID of the order to pick up. Must be in the kitchen.")

    def is_valid(self, state: RestaurantState, employee_id: str) -> ValidationResult:
        if not order_exists(state, self.order_id):
            return ValidationResult(False, f"There is no order named {self.order_id}.")
        
        if not is_order_ready(state, self.order_id):
            return ValidationResult(False, f"The order {self.order_id} is not ready for {employee_id} to pick up.")
        
        return ValidationResult(True, None)

    def execute(self, state: RestaurantState, employee_id: str) -> ActionResult:
        if not is_at_kitchen(state, employee_id):
            step_toward_kitchen(state, employee_id)
        add_order_to_inventory(state, employee_id, self.order_id)
        return ActionResult(message=f"{employee_id} picked up order {self.order_id}.", repeat=False)


# Utilities --------------------------------
def order_exists(state: RestaurantState, order_id: str) -> bool:
    """Check if order exists in the system."""
    return state.get_order(order_id) is not None

def is_order_ready(state: RestaurantState, order_id: str) -> bool:
    """Check if order is ready for pickup."""
    order = state.get_order(order_id)
    return order.status == OrderStatus.READY

def is_at_kitchen(state: RestaurantState, employee_id: str) -> bool:
    """Check if employee is at the kitchen."""
    return state.get_employee_grill(employee_id) is not None

def add_order_to_inventory(state: RestaurantState, employee_id: str, order_id: str):
    """Add an order to the employee's inventory."""
    state.add_order_carried(employee_id, order_id)

def step_toward_kitchen(state: RestaurantState, employee_id: str):
    employee = state.get_employee(employee_id)
    grill_poss = [g.position for g in state.get_all_grills()]
    nearest_index = state.get_navigation_service().get_closest_entity(employee.position, grill_poss)
    new_position = state.get_navigation_service().move_toward(employee.position, grill_poss[nearest_index])
    employee.position = new_position
    state.update_employee(employee)