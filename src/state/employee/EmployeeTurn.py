
from dataclasses import dataclass
from typing import List
from pydantic import BaseModel
from src.agents.models.Model import ResponseMessage, StandardMessage, ToolInvocationMessage, ToolResultMessage
from src.protocols import IAction
from src.state.employee.EmployeeDecision import EmployeeDecision



@dataclass
class EmployeeTurn:
    
    """
    Represents the decisions made by an employee during a turn.
    All decisions except for the last one are invalid.
    Only the last item is considered the new canonical state of the employee.
    """
    employee_name: str
    decisions: List[EmployeeDecision]

    def action(self) -> IAction:
        return self.decisions[-1].action

