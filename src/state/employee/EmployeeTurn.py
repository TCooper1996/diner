
from dataclasses import dataclass
from typing import List
from pydantic import BaseModel
from src.agents.models.Model import ResponseMessage, StandardMessage, ToolInvocationMessage, ToolResultMessage
from src.protocols import IAction
from src.state.employee.EmployeeDecision import EmployeeDecision
from src.state.restaurant_state import RestaurantState



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
    next_action: IAction
    new_state: RestaurantState

    def get_messages(self) -> List[StandardMessage]:
        return [message for decision in self.decisions for message in decision.get_messages()]


