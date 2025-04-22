
from dataclasses import dataclass
from typing import List, Optional
from pydantic import BaseModel
from src.agents.models.Model import ResponseMessage, StandardMessage, ToolInvocationMessage, ToolResultMessage
from src.protocols import IAction
from src.state.game_state.restaurant_state.restaurant_state import RestaurantState
from .employee_decision import EmployeeDecision


@dataclass
class EmployeeTurn:
    
    """
    Represents the decisions made by an employee during a turn.
    All decisions except for the last one are invalid.
    Only the last item is considered the new canonical state of the employee.
    """
    employee_name: str
    decisions: List[EmployeeDecision]
    action_result_message: str
    action: IAction
    next_action: IAction | None
    new_state: RestaurantState

    def get_messages(self) -> List[StandardMessage]:
        return [message for decision in self.decisions for message in decision.get_messages()]

    @property
    def response(self)-> Optional[str]:
        if self.decisions:
            return self.decisions[-1].response.content
        return None

        
    @property
    def result(self)->str:
        return self.action_result_message

