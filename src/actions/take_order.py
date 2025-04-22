"""Take order action implementation"""

from dataclasses import dataclass
from typing import List
from pydantic import BaseModel, Field

from src.actions.EmployeeActionInteractor import EmployeeActionInteractor
from src.common.results import ActionResult, ActionResult, ValidationResult  # Updated import
from src.core.entities.customer import CustomerStatus


class TakeOrderAction(BaseModel):
    """
    Take a customers order.
    """
    customer_id: str = Field(..., description="The ID of the customer to take order from")

    def is_valid(self, itr: EmployeeActionInteractor) -> ValidationResult:
        if not itr.customer_exists(self.customer_id):
            return ValidationResult(False, f"Customer {self.customer_id} not found.")
        
        return ValidationResult(True, None)

    def execute(self, itr: EmployeeActionInteractor) -> ActionResult:
        reached = itr.approach_entity(itr.employee_name, self.customer_id)
        if reached:
            itr.set_customer_status(self.customer_id, CustomerStatus.ORDERED)  # Update the customer's status to ORDERED
            order_id = itr.get_order_from_customer(self.customer_id)
            return ActionResult(message=f"{itr.employee_name} took an order from customer {self.customer_id}", repeat=False)
        else:
            return ActionResult(message=f"{itr.employee_name} is moving toward customer: {self.customer_id} to take order.", repeat=True)
