"""Take order action implementation"""

from typing import List
from pydantic import BaseModel, Field
from langchain_core.tools import tool

from src.actions.base import ActionResult
from src.state.customer import CustomerStatus
from src.state.game import GameState, OrderStatus
from src.state.employee import Employee
from src.state.order import Order, OrderItem


class TakeOrderAction(BaseModel):
    """
    Take a customers order.
    """
    customer_id: str = Field(..., description="The ID of the customer to take order from")

def take_order(employee: Employee, game_state: GameState, args: TakeOrderAction) -> ActionResult:
    if employee.location != "dining":
        return ActionResult(False, f"{employee.name} cannot take orders from the {employee.location}. You need to be in the dining area.", game_state)
    
    # Find seated customers in the dining area
    cust = game_state.get_customer(args.customer_id)
    if not cust:
        return ActionResult(False, f"Customer {args.customer_id} not found.", game_state)

    # Use the extracted take_customer_order function
    cust.status = CustomerStatus.ORDERED
    items = cust.take_order()
    order = Order(customer_id=cust.id, items=items, status=OrderStatus.PENDING)
    game_state.orders[order.id] = order
    game_state.assign_order_to_employee(employee.name, order.id)

    return ActionResult(True, f"{employee.name} took an order from customer {cust.name} for {', '.join(items)}.", game_state)
