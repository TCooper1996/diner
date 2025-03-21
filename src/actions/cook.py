"""Cook food action implementation"""

from pydantic import Field, BaseModel
from langchain_core.tools import tool

from src.actions.base import ActionResult, copy_args
from src.state.game import GameState, OrderStatus
from src.state.employee import Employee



class CookAction(BaseModel):
    """Cook food for a 'SUBMITTED' order (must be at kitchen.)
    """
    order_id: str = Field(
        description="The ID of the order to cook"
    )

@copy_args
def cook_food(employee: Employee, game_state: GameState, args: CookAction) -> ActionResult:
    if employee.location != "kitchen":
        return ActionResult(False, f"{employee.name} cannot cook food from the {employee.location}. You need to be in the kitchen.", game_state)
    
    order_id = args.order_id
    if order_id not in game_state.orders:
        return ActionResult(False, f"Order #{order_id} not found.", game_state)
    
    order = game_state.orders[order_id]
    if order.status != OrderStatus.SUBMITTED:
        return ActionResult(False, f"Order #{order_id} is not ready to be cooked. Current status: {order.status.value}", game_state)
    
    game_state.orders[order_id].status = OrderStatus.READY
    return ActionResult(True, f"{employee.name} prepared order #{order_id}: {order.items}.", game_state)
