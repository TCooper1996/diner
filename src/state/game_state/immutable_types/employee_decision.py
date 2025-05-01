
from dataclasses import dataclass
from typing import List

from src.actions import Action
from src.agents.models.Model import ResponseMessage, ToolInvocationMessage, ToolResultMessage


@dataclass
class EmployeeDecision:
    """
    Represents the decision made by an agent, which may have been valid or invalid
    """
    response: ResponseMessage
    invocation: ToolInvocationMessage
    result: ToolResultMessage
    action: Action
    validation_error: str | None
    state_message: str
    messages: List[str]

    @property
    def was_valid(self) -> bool:
        return not self.result.is_error

    def get_action(self) -> Action:
        return self.action
    
    def get_result(self) -> str:
        return self.result.tool_output
    
    def get_response(self) -> str:
        return self.response.content

    def get_messages(self):
        return [self.response, self.invocation, self.result]
