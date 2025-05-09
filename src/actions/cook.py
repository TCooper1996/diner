"""Cook food action implementation"""

from pydantic import Field, BaseModel
from langchain_core.tools import tool

from src.core.entities.order import OrderStatus
from src.core.models.Action import ActionResult, ValidationResult
from src.core.models.RestaurantState import RestaurantState
from src.core.entities.grill import Grill


class CookAction(BaseModel):
    """Cook food for a 'SUBMITTED' order.
    """
    order_id: str = Field(
        description="The ID of the order to cook"
    )

    def is_valid(self, state: RestaurantState, employee_id: str) -> ValidationResult:
        
        if not order_exists(state, self.order_id):
            return ValidationResult(False, f"Order #{self.order_id} not found.")
        
        status = get_order_status(state, self.order_id)
        if status != OrderStatus.SUBMITTED:
            return ValidationResult(False, f"Order #{self.order_id} is not ready to be cooked. Current status: {status.value}")
        
        return ValidationResult(True, None)

    def execute(self, state: RestaurantState, employee_id: str) -> ActionResult:
        grill_id = state.get_employee_grill(employee_id)
        if grill_id is None:
            grill = find_nearest_unoccupied_grill(state, employee_id)
            state.set_employee_grill(employee_id, grill.grill_id)
        else:
            grill = state.get_grill(grill_id)

        step_toward_grill(state, employee_id, grill)
        
        if grill_reached(state, employee_id, grill):
            # Change order status to ready
            order = state.get_order(self.order_id)
            order.status = OrderStatus.READY
            state.update_order(order)
            return ActionResult(f"{employee_id} prepared order #{self.order_id}.", repeat=False)
        else:
            return ActionResult(f"{employee_id} is moving toward the kitchen to cook order #{self.order_id}.", repeat=True)


# Utilities --------------------------------
def order_exists(state: RestaurantState, order_id: str) -> bool:
    return state.get_order(order_id) is not None

def get_order_status(state: RestaurantState, order_id: str) -> OrderStatus:
    return state.get_order(order_id).status

def find_nearest_unoccupied_grill(state: RestaurantState, employee_id: str) -> Grill:
    all_grills = state.get_all_grills()
    unoccupied_grills = [g for g in all_grills if not state.is_grill_occupied(g.grill_id)]
    if not unoccupied_grills:
        raise ValueError("No unoccupied grills available.")
    
    # Find closest one
    employee_position = state.get_employee(employee_id).position
    grill_positions = [g.position for g in unoccupied_grills]
    nearest_index = state.get_navigation_service().get_closest_entity(employee_position, grill_positions)
    
    return unoccupied_grills[nearest_index]

def step_toward_grill(state: RestaurantState, employee_id: str, grill: Grill):
    employee = state.get_employee(employee_id)
    path = state.get_navigation_service().get_path_between_positions(employee.position, grill.position)
    
    if path is None or len(path) <= 1:
        return
    
    # Move the employee
    employee.position = path[1]
    state.update_employee(employee)

def grill_reached(state: RestaurantState, employee_id: str, grill: Grill) -> bool:
    employee = state.get_employee(employee_id)
    return employee.position == grill.position

