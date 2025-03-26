"""Wait action implementation"""

from pydantic import BaseModel, Field
from langchain_core.tools import tool

from src.actions.base import ActionResult
from src.state.game import GameState
from src.state.employee.employee import Employee


class WaitAction(BaseModel):
    """
    Tool for waiting (taking no action)
    """
    


def validate_wait(employee: Employee, game_state: GameState) -> ActionResult:
    """
    Validate wait action (always succeeds)
    
    Args:
        employee: The employee performing the action
        game_state: The current game state
        
    Returns:
        ActionResult with success status, message, and updated game state
    """
    return ActionResult(True, f"{employee.name} is waiting for the next instruction.", game_state)