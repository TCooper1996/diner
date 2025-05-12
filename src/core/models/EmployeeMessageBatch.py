from dataclasses import dataclass
from typing import List, Protocol

from src.agents.models.Model import ResponseMessage, StandardMessage, ToolInvocationMessage, ToolResultMessage
from src.core.models.Action import Action


@dataclass
class EmployeeMessageBatch:
    response: ResponseMessage
    tool_invocation: ToolInvocationMessage
    tool_result: ToolResultMessage

    def get_agent_response_string(self) -> List[StandardMessage]:
        return [self.response, self.tool_invocation, self.tool_result]


class PartialEmployeeMessageBatch:
    """Will end up representing a success, and is partial because we don't have the full response until the action is executed."""
    def __init__(self, response: ResponseMessage, tool_invocation: ToolInvocationMessage, action: Action):
        self.response = response
        self.tool_invocation = tool_invocation
        self.action = action

    def resolve(self, tool_result: str, was_successful: bool) -> EmployeeMessageBatch:
        """Resolve the partial message batch into a full one, by adding the tool result.
        This method will be used by the calling function.
        """
        result = ToolResultMessage(tool=self.tool_invocation.tool, tool_output=tool_result, tool_id=self.tool_invocation.tool_id, is_error=not was_successful)
        return EmployeeMessageBatch(self.response, self.tool_invocation, result)