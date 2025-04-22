from pydantic import BaseModel, Field

from src.actions.EmployeeActionInteractor import EmployeeActionInteractor
from src.common.results import ActionResult, ActionResult, ValidationResult  # Updated import


class PickUpOrder(BaseModel):
    """
    Adds a nearby order to your inventory.
    You must be in the kitchen to pick up an order.
    You can only pick up orders that are ready.
    """
    order_id: str = Field(..., description="The ID of the order to pick up. Must be in the kitchen.")

    def is_valid(self, itr: EmployeeActionInteractor) -> ValidationResult:
        if itr.is_at_station("kitchen") is False:
            return ValidationResult(False, f"{itr.employee_name} cannot pick up an order from the {itr.current_location()}. You must be in the kitchen.")
        
        if itr.order_exists(self.order_id) is False:
            return ValidationResult(False, f"There is no order named {self.order_id}.")
        
        if self.order_id not in itr.get_ready_orders():
            return ValidationResult(False, f"The order {self.order_id} is not ready for {itr.employee_name} to pick up.")
        
        return ValidationResult(True, None)

    def execute(self, itr: EmployeeActionInteractor) -> ActionResult:
        itr.add_order_to_inventory(self.order_id)
        return ActionResult(message=f"{itr.employee_name} picked up order {self.order_id}.")