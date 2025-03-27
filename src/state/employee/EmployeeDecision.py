
from dataclasses import dataclass

from src.agents.models.Model import ResponseMessage, ToolInvocationMessage, ToolResultMessage
from src.protocols import IAction


@dataclass
class EmployeeDecision:
    """
    Represents the decision made by an agent, which may have been valid or invalid
    """
    response: ResponseMessage
    invocation: ToolInvocationMessage
    result: ToolResultMessage
    action: IAction

    @property
    def was_valid(self) -> bool:
        return self.result.is_error

    def get_action(self) -> IAction:
        return self.action
    
    def get_result(self) -> str:
        return self.result.tool_output
    
    def get_response(self) -> str:
        return self.response.content

    def get_messages(self):
        return [self.response, self.invocation, self.result]
