
from typing import List
from pydantic import BaseModel
from src.actions import EmployeeAction
from src.actions.base import ActionResult
from src.state.game import GameState


class AgentDecision(BaseModel):
    """
    Represents the decision made by an agent, which may have been valid or invalid
    """
    action: EmployeeAction
    actionResult: ActionResult

    def current_state(self) -> GameState:
        return self.actionResult.game_state


class EmployeeTurn(BaseModel):
    
    """
    Represents the decisions made by an employee during a turn.
    All decisions except for the last one are invalid.
    Only the last item is considered the new canonical state of the employee.
    """
    employee_name: str
    decisions: List[AgentDecision]

    def current_state(self) -> GameState:
        return self.decisions[-1].actionResult.game_state

    def action(self) -> EmployeeAction:
        return self.decisions[-1].action