"""Take order action implementation"""

from dataclasses import dataclass
from typing import List
from pydantic import BaseModel, Field

from src.core.entities.customer import CustomerStatus
from src.core.entities.order import Order
from src.core.models.Action import ActionResult, ValidationResult
from src.core.models.RestaurantState import RestaurantState


class TakeOrderAction(BaseModel):
    """
    Take a customers order.
    """
    customer_id: str = Field(..., description="The ID of the customer to take order from")

    def is_valid(self, state: RestaurantState, employee_name: str) -> ValidationResult:
        if not customer_exists(state, self.customer_id):
            return ValidationResult(False, f"Customer {self.customer_id} not found.")
        
        return ValidationResult(True, None)

    def execute(self, state: RestaurantState, employee_name: str) -> ActionResult:
        step_toward_customer(state, employee_name, self.customer_id)
        if reached_customer(state, employee_name, self.customer_id):
            add_order(state, employee_name, self.customer_id)
            return ActionResult(message=f"{employee_name} took an order from customer {self.customer_id}", repeat=False)
        else:
            return ActionResult(message=f"{employee_name} is moving toward customer: {self.customer_id} to take order.",  repeat=True)


# Utilities --------------------------------
def customer_exists(state: RestaurantState, customer_id: str) -> bool:
    """Check if a customer exists in the system."""
    return state.get_customer(customer_id) is not None

def reached_customer(state: RestaurantState, employee_name: str, customer_id: str) -> bool:
    """Check if the employee has reached the customer."""
    customer = state.get_customer(customer_id)
    employee = state.get_employee(employee_name)
    return employee.position == customer.position

def step_toward_customer(state: RestaurantState, employee_name: str, customer_id: str):
    customer = state.get_customer(customer_id)
    employee = state.get_employee(employee_name)
    """Move the employee toward the customer."""
    path = state.get_navigation_service().get_path_between_positions(employee.position, customer.position)
    employee.position = path[1]
    state.update_employee(employee)
    

def add_order(state: RestaurantState, employee_name: str, customer_id: str):
    """Creates a new order, creates employee_order record, and updates customer status."""
    order = state.create_order()
    state.add_order(order)

    state.add_order_taken(employee_name, order.id)
    customer = state.get_customer(customer_id)
    customer.status = CustomerStatus.ORDERED
    state.update_customer(customer)