from dataclasses import dataclass
from typing import Callable, Dict, List, Protocol, Tuple, Type

from src.actions import  parse_tool
from src.agents.employeeAgent import LLM
from src.agents.models.Claude import Claude
from src.agents.models.Model import ResponseMessage, StandardMessage, ToolInvocationMessage, ToolResultMessage
from src.core.models.Action import Action, ValidationResult

@dataclass
class EmployeeAgentAttempt:
    """Represents an attempt made by the AI agent to perform an action, which may or may not have been valid."""
    selected_action: Action
    # These come from the agents response
    text_response: ResponseMessage
    tool_invocation: ToolInvocationMessage
    result: ValidationResult

@dataclass
class SuccessfulEmployeeAgentAttempt:
    attempt: EmployeeAgentAttempt

@dataclass
class FailedEmployeeAgentAttempt:
    attempt: EmployeeAgentAttempt
    tool_result: ToolResultMessage


ActionVerifier = Callable[[Action], ValidationResult]


class AgentService:
    def __init__(self, instructions: Dict[str, str], allowed_actions: Dict[str, List[Type[Action]]]):
        self.instructions = instructions
        self.agent_cache: Dict[str, LLM] = {}
        for employee_name, _ in instructions.items():
            self.agent_cache[employee_name] = LLM(Claude(allowed_actions[employee_name]))

    async def get_next_valid_action(self, employee_name: str, state_message: str, messages: List[StandardMessage], verify: ActionVerifier) -> Tuple[Action, List[StandardMessage]]:
        agent = self.agent_cache[employee_name]
        attempts = []
        current_messages: List[StandardMessage] = []
        for i in range(3):
            result = await self.get_next_action(agent, employee_name, state_message, messages + current_messages, verify)
            attempts.append(result)
            current_messages.append(result.attempt.text_response)
            current_messages.append(result.attempt.tool_invocation)
            if isinstance(result, SuccessfulEmployeeAgentAttempt):
                return result.attempt.selected_action, current_messages
            else:
                current_messages.append(result.tool_result)
        raise Exception(f"Failed to get a valid action for {employee_name} after 3 attempts. Attempts: {attempts}")


    async def get_next_action(self, agent: LLM, employee_name: str, state_message: str, messages: List[StandardMessage], verify: ActionVerifier) -> SuccessfulEmployeeAgentAttempt| FailedEmployeeAgentAttempt:
        response = await agent.invoke_cached(self.instructions[employee_name], state_message, messages)
        action = parse_tool(response.tool_name, response.tool_args)
        result = verify(action)
        attempt = EmployeeAgentAttempt(action,
                                    ResponseMessage(content=response.original_response.content),
                                    ToolInvocationMessage(tool=response.tool_name, tool_input=response.tool_args, tool_id=response.tool_id),
                                    result
                                    )
        if result.success:
            return SuccessfulEmployeeAgentAttempt(attempt)
        else:
            # If the action is not valid, we need to get the tool result
            # This is a bit of a hack, but we can use the tool invocation message to get the tool result
            # and then return it as a failed attempt
            tool_result = ToolResultMessage(tool=response.tool_name, tool_output=result.error_msg or "no error message!!", tool_id=response.tool_id, is_error=True)
            return FailedEmployeeAgentAttempt(attempt, tool_result)