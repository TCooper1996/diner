"""Deliver food action implementation"""

from pydantic import BaseModel, Field

from src.core.entities.customer import CustomerStatus
from src.core.entities.order import OrderStatus
from src.core.models.Action import ActionResult, ValidationResult
from src.core.models.RestaurantState import RestaurantState


class DeliverOrderToCustomer(BaseModel):
    """
    Moves a prepared order from your inventory to a customer.
    If a customer recieves food that they did not order, they will be upset.
    """
    customer_id: str = Field(..., description="The ID of the customer to deliver food to")
    order_id: str = Field(..., description="The ID of the order to deliver. Must be in your inventory.")

    def is_valid(self, state: RestaurantState, employee_id: str) -> ValidationResult:
        if not has_order_in_inventory(state, employee_id, self.order_id):
            return ValidationResult(False, f"{employee_id} does not have order {self.order_id} in their inventory.")
        
        if not customer_exists(state, self.customer_id):
            return ValidationResult(False, f"Customer {self.customer_id} does not exist.")
        
        return ValidationResult(True, None)

    def execute(self, state: RestaurantState, employee_id: str) -> ActionResult:
        step_toward_customer(state, employee_id, self.customer_id)
        
        if reached_customer(state, employee_id, self.customer_id):
            # Update order status
            order = state.get_order_repo().get_order(self.order_id)
            order.status = OrderStatus.DELIVERED
            state.get_order_repo().update_order(order)
            
            # Update customer status
            customer = state.get_customer_repo().get_customer(self.customer_id)
            customer.status = CustomerStatus.EATING
            state.get_customer_repo().update_customer(customer)
            
            return ActionResult(f"{employee_id} delivered order #{self.order_id} to customer {self.customer_id}. The customer is now eating.", repeat=False)
        else:
            return ActionResult(f"{employee_id} is moving toward customer: {self.customer_id} to deliver order #{self.order_id}.", repeat=True)


# Utilities --------------------------------
def has_order_in_inventory(state: RestaurantState, employee_id: str, order_id: str) -> bool:
    """Check if the employee has the specified order in their inventory."""
    orders_carried = state.get_employee_order_repo().get_orders_carried(employee_id)
    return order_id in [order.id for order in orders_carried]

def customer_exists(state: RestaurantState, customer_id: str) -> bool:
    """Check if a customer exists in the system."""
    return state.get_customer_repo().get_customer(customer_id) is not None

def reached_customer(state: RestaurantState, employee_id: str, customer_id: str) -> bool:
    """Check if the employee has reached the customer."""
    customer = state.get_customer_repo().get_customer(customer_id)
    employee = state.get_employee_repo().get_employee(employee_id)
    return employee.position == customer.position

def step_toward_customer(state: RestaurantState, employee_id: str, customer_id: str):
    """Move the employee toward the customer."""
    customer = state.get_customer_repo().get_customer(customer_id)
    employee = state.get_employee_repo().get_employee(employee_id)
    
    path = state.get_navigation_service().get_path_between_positions(employee.position, customer.position)
    
    if path is None or len(path) <= 1:
        return
    
    employee.position = path[1]
    state.get_employee_repo().update_employee(employee)

