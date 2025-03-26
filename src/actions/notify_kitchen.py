"""Notify kitchen of orders action implementation"""

from typing import List
from pydantic import BaseModel, Field
from langchain_core.tools import tool

from src.actions.base import ActionResult, copy_args
from src.state.game import GameState, OrderStatus
from src.state.employee.employee import Employee


class SubmitOrdersToKitchen(BaseModel):
    """
    Notify kitchen of new orders
    """
    pass

@copy_args
def validate_submit_orders_to_kitchen(employee: Employee, game_state: GameState) -> ActionResult:
    if employee.location != "kitchen":
        return ActionResult(False, f"{employee.name} cannot notify the kitchen from the {employee.location}. You need to be in the kitchen.", game_state)
    
        
    orders = [o for o in game_state.orders_taken_by_employee(employee.name) if o.status == OrderStatus.PENDING]
    for order in orders:
        order.status = OrderStatus.SUBMITTED
    return ActionResult(True, f"Submitted {len(orders)} orders to kitchen", game_state)

