
from dataclasses import dataclass
from typing import List
from pydantic import BaseModel
from src.agents.models.Model import ResponseMessage, StandardMessage, ToolInvocationMessage, ToolResultMessage


class AgentDecision(BaseModel):
    """
    Represents the decision made by an agent, which may have been valid or invalid
    """
    response: ResponseMessage
    invocation: ToolInvocationMessage
    result: ToolResultMessage
    action: str


    def get_action(self) -> str:
        return repr(self.action)
    
    def get_result(self) -> str:
        return self.result.tool_output
    
    def get_response(self) -> str:
        return self.response.content


class EmployeeTurn(BaseModel):
    
    """
    Represents the decisions made by an employee during a turn.
    All decisions except for the last one are invalid.
    Only the last item is considered the new canonical state of the employee.
    """
    employee_name: str
    decisions: List[AgentDecision]

    def action(self) -> str:
        return self.decisions[-1].action


class GameTurn(BaseModel):
    employees: List[EmployeeTurn]