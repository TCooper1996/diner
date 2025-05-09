from dataclasses import dataclass
from typing import Callable, Dict, List, Protocol, Tuple, Type

from src.actions import  parse_tool
from src.agents.employeeAgent import LLM
from src.agents.models.Claude import Claude
from src.agents.models.Model import ResponseMessage, StandardMessage, ToolInvocationMessage, ToolResultMessage
from src.core.models.Action import Action, ValidationResult
from src.core.models.AgentServiceAttempt import AgentServiceAttempt, PartialAgentServiceAttempt
from src.core.models.EmployeeMessageBatch import EmployeeMessageBatch


class AgentServiceAttemptImpl(AgentServiceAttempt):
    """Will end up representing a failure, since after a failure we have the full response."""
    def __init__(self, response: ResponseMessage, tool_invocation: ToolInvocationMessage, tool_result: ToolResultMessage, action: Action):
        self.response = response
        self.tool_invocation = tool_invocation
        self.tool_result = tool_result
        self.action = action

    def get_standard_messages(self) -> List[StandardMessage]:
        return [self.response, self.tool_invocation, self.tool_result]

    def get_agent_response_string(self):
        return self.response.content

    def get_action_result_string(self):
        return self.tool_result.tool_output

    def get_action(self) -> Action:
        return self.action

class PartialAgentServiceAttemptImpl(PartialAgentServiceAttempt):
    """Will end up representing a success, and is partial because we don't have the full response until the action is executed."""
    def __init__(self, response: ResponseMessage, tool_invocation: ToolInvocationMessage, action: Action):
        self.response = response
        self.tool_invocation = tool_invocation
        self.action = action
    
    def get_action(self) -> Action:
        return self.action

    def resolve(self, tool_result: str) -> AgentServiceAttemptImpl:
        """Resolve the partial message batch into a full one, by adding the tool result.
        This method will be used by the calling function.
        """
        result = ToolResultMessage(tool=self.tool_invocation.tool, tool_output=tool_result, tool_id=self.tool_invocation.tool_id, is_error=False)
        return AgentServiceAttemptImpl(self.response, self.tool_invocation, result, self.action)


ActionVerifier = Callable[[Action], ValidationResult]


class AgentServiceImpl:
    def __init__(self, instructions: Dict[str, str], allowed_actions: Dict[str, List[Type[Action]]]):
        self.instructions = instructions
        self.agent_cache: Dict[str, LLM] = {}
        for employee_name, _ in instructions.items():
            self.agent_cache[employee_name] = LLM(Claude(allowed_actions[employee_name]))

    async def get_next_valid_action(self, employee_name: str, state_message: str, messages: List[StandardMessage], verify: ActionVerifier) -> Tuple[List[AgentServiceAttemptImpl], PartialAgentServiceAttemptImpl]:
        agent = self.agent_cache[employee_name]
        failed_attempts: List[AgentServiceAttemptImpl] = []
        for i in range(3):
            current_messages = messages + [m for a in failed_attempts for m in a.get_standard_messages()]
            batch = await self.get_next_action(agent, employee_name, state_message, messages + current_messages, verify)
            if isinstance(batch, PartialAgentServiceAttemptImpl):
                # We have a valid action, so we can return it
                return failed_attempts, batch
            failed_attempts.append(batch)
        raise Exception(f"Failed to get a valid action for {employee_name} after 3 attempts")


    async def get_next_action(self, agent: LLM, employee_name: str, state_message: str, messages: List[StandardMessage], verify: ActionVerifier) -> AgentServiceAttemptImpl | PartialAgentServiceAttemptImpl:
        response = await agent.invoke_cached(self.instructions[employee_name], state_message, messages)
        action = parse_tool(response.tool_name, response.tool_args)
        result = verify(action)
        response_message = ResponseMessage(content=response.original_response.content)
        tool_invocation = ToolInvocationMessage(tool=response.tool_name, tool_input=response.tool_args, tool_id=response.tool_id)
        if result.success:
            return PartialAgentServiceAttemptImpl(response_message, tool_invocation, action)
        else:
            # If the action is not valid, we need to get the tool result
            # This is a bit of a hack, but we can use the tool invocation message to get the tool result
            # and then return it as a failed attempt
            tool_result = ToolResultMessage(tool=response.tool_name, tool_output=result.error_msg or "no error message!!", tool_id=response.tool_id, is_error=True)
            return AgentServiceAttemptImpl(response_message, tool_invocation, tool_result, action)