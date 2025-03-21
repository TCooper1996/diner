"""Move action implementation"""

from typing import ClassVar, List, Literal
from pydantic import BaseModel, Field

from src.actions.base import ActionResult, copy_args
from src.state.game import GameState
from src.state.employee import Employee


class MoveToNewRoom(BaseModel):
    """
    Tool for moving an employee to a different location
    """
    destination: str = Field(
        description="The location to move to (entrance, dining, or kitchen)"
    )

@copy_args
def validate_move_to_location(employee: Employee, game_state: GameState, args: MoveToNewRoom) -> ActionResult:
    current_location = employee.location
    destination = args.destination
    if current_location == destination:
        return ActionResult(False, f"{employee.name} is already at the {destination}.", game_state)
    
    valid_locations = ["entrance", "dining", "kitchen"]
    if destination.lower() not in valid_locations:
        return ActionResult(False, f"Cannot move to {destination}. Valid locations are: {', '.join(valid_locations)}", game_state)
    
    # Update the employee's location in the game_state
    if employee.name in game_state.employees:
        game_state.employees[employee.name].location = destination
    
    return ActionResult(True, f"{employee.name} moved from the {current_location} to the {destination}.", game_state)