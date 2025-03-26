"""Seat customer action implementation"""

from pydantic import BaseModel, Field
from langchain_core.tools import tool

from src.actions.base import ActionResult, copy_args
from src.state.customer import CustomerStatus
from src.state.game import GameState
from src.state.employee.employee import Employee
from src.game_engine.location import DINING


class SeatAction(BaseModel):
    """Take a seat"""
    customer_id: str = Field(description="The ID of the customer to seat")

@copy_args
def seat_customer(employee: Employee, game_state: GameState, args: SeatAction) -> ActionResult:
    if employee.location != "entrance":
        return ActionResult(False, f"{employee.name} cannot seat customers from the {employee.location}. You need to be at the entrance.", game_state)
    
    # Find waiting customers at the entrance
    cust = game_state.get_customer(args.customer_id)
    if cust is None:
        return ActionResult(False, f"Customer {args.customer_id} does not exist", game_state)
    if cust.status != CustomerStatus.WAITING:
        return ActionResult(False, f"Customer {args.customer_id} is not waiting", game_state)
    
    cust.location = DINING
    cust.status = CustomerStatus.SEATED
    return ActionResult(True, f"{employee.name} seated customer {cust.name} at a table in the dining area.", game_state)