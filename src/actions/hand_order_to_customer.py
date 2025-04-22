"""Deliver food action implementation"""

from pydantic import BaseModel, Field

from src.actions.EmployeeActionInteractor import EmployeeActionInteractor
from src.common.results import ActionResult, ActionResult, ValidationResult  # Updated import
from src.core.entities import *


class DeliverOrderToCustomer(BaseModel):
    """
    Moves a prepared order from your inventory to a customer.
    If a customer recieves food that they did not order, they will be upset.
    """
    customer_id: str = Field(..., description="The ID of the customer to deliver food to")
    order_id: str = Field(..., description="The ID of the order to deliver. Must be in your inventory.")

    def is_valid(self, itr: EmployeeActionInteractor) -> ValidationResult:
        if self.order_id not in itr.get_orders_carried():
            return ValidationResult(False, f"{itr.employee_name} does not have order {self.order_id} in their inventory.")
        
        if not itr.customer_exists(self.customer_id):
            return ValidationResult(False, f"Customer {self.customer_id} does not exist.")
        
        return ValidationResult(True, None)

    def execute(self, itr: EmployeeActionInteractor) -> ActionResult:
        reached = itr.approach_entity(itr.employee_name, self.customer_id)  # Ensure the employee approaches the customer
        if reached:
            itr.set_order_status(self.order_id, OrderStatus.DELIVERED)
            itr.set_customer_status(self.customer_id, CustomerStatus.EATING)
            return ActionResult(f"{itr.employee_name} delivered order #{self.order_id} to customer {self.customer_id}. The customer is now eating.", repeat=False)
        else:
            return ActionResult(f"{itr.employee_name} is moving toward customer: {self.customer_id} to deliver order #{self.order_id}.", repeat=True)

