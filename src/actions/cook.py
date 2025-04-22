"""Cook food action implementation"""

from pydantic import Field, BaseModel
from langchain_core.tools import tool

from src.actions.EmployeeActionInteractor import EmployeeActionInteractor
from src.common.results import ActionResult, ActionResult, ValidationResult  # Updated import
from src.core.entities.order import OrderStatus


class CookAction(BaseModel):
    """Cook food for a 'SUBMITTED' order.
    """
    order_id: str = Field(
        description="The ID of the order to cook"
    )

    def is_valid(self, itr: EmployeeActionInteractor) -> ValidationResult:
        
        if not itr.order_exists(self.order_id):
            return ValidationResult(False, f"Order #{self.order_id} not found.")
        
        status = itr.get_order_status(self.order_id)
        if status != OrderStatus.SUBMITTED:
            return ValidationResult(False, f"Order #{self.order_id} is not ready to be cooked. Current status: {status.value}")
        
        return ValidationResult(True, None)

    def execute(self, itr: EmployeeActionInteractor) -> ActionResult:
        kitchen_id = itr.get_station_locked_by("kitchen", itr.employee_name)
        if kitchen_id is None:
            kitchen_id = itr.find_nearest_station("kitchen", itr.employee_name)
            itr.lock_station(kitchen_id, itr.employee_name)
        
        done = itr.cook_order(self.order_id)
        if done:
            itr.set_order_status(self.order_id, OrderStatus.READY)
            return ActionResult(f"{itr.employee_name} prepared order #{self.order_id}.", repeat=False)
        else:
            return ActionResult(f"{itr.employee_name} is cooking order #{self.order_id}.", repeat=True)

