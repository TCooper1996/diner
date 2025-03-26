"""Deliver food action implementation"""

from pydantic import BaseModel, Field

from src.actions.base import ActionResult, copy_args
from src.state.customer import CustomerStatus
from src.state.game import GameState, OrderStatus
from src.state.employee.employee import Employee


class HandOrderToCustomer(BaseModel):
    """
    Moves a prepared order from your inventory to a customer.
    If a customer recieves food that they did not order, they will be upset.
    """
    customer_id: str = Field(..., description="The ID of the customer to deliver food to")
    order_id: str = Field(..., description="The ID of the order to deliver. Must be in your inventory.")

@copy_args
def hand_food_to_customer(employee: Employee, game_state: GameState, args: HandOrderToCustomer) -> ActionResult:
    if employee.location != "dining":
        return ActionResult(False, f"{employee.name} cannot deliver food from the {employee.location}. You must be in the dining room.", game_state)
    
    # Find orders that are ready to be delivered
    orders = {o.id: o for o in game_state.orders_carried_by_employee(employee.name)}
    order = orders.get(args.order_id)
    if order is None:
        return ActionResult(False, f"{employee.name} does not have order {args.order_id} in their inventory.", game_state)

    customer = game_state.customers.get(args.customer_id)
    if not customer:
        return ActionResult(False, f"Customer {args.customer_id} does not exist.", game_state)
    
    game_state.remove_order_from_employee_inventory(employee.name, args.order_id)
    customer.status = CustomerStatus.EATING
    order.status = OrderStatus.DELIVERED

    
    return ActionResult(True, f"{employee.name} delivered order #{order.id} to customer {customer.name}. The customer is now eating.", game_state)
