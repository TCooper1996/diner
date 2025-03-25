from pydantic import BaseModel, Field

from src.actions.base import ActionResult, copy_args
from src.state.employee import Employee
from src.state.game import GameState


class PickUpOrder(BaseModel):
    """
    Adds a nearby order to your inventory.
    You must be in the kitchen to pick up an order.
    You can only pick up orders that are ready.
    """
    order_id: str = Field(..., description="The ID of the order to pick up. Must be in the kitchen.")


@copy_args
def pick_up_order(employee: Employee, game_state: GameState, args: PickUpOrder) -> ActionResult:
    order_id = args.order_id
    if employee.location != "kitchen":
        return ActionResult(False, f"{employee.name} cannot pick up an order from the {employee.location}. You must be in the kitchen.", game_state)

    # Find orders that are ready to be picked up
    ready_orders = {order.id:order for order in game_state.get_ready_orders()}

    if not ready_orders:
        return ActionResult(False, f"There is no order ready for {employee.name} to pick up.", game_state)

    # Check if the order is ready
    if order_id not in ready_orders:
        return ActionResult(False, f"The order {order_id} is not ready for {employee.name} to pick up.", game_state)

    # Pick up the order
    game_state.assign_order_to_employee_inventory(employee.name, order_id)

    return ActionResult(True, f"{employee.name} picked up order {order_id}.", game_state)