from dataclasses import dataclass
from typing import Callable, Dict, List, Protocol, Tuple, Type

from src.actions import  parse_tool
from src.agents.employeeAgent import LLM
from src.agents.models.Claude import Claude
from src.agents.models.Model import ResponseMessage, StandardMessage, ToolInvocationMessage, ToolResultMessage
from src.core.models.Action import Action, ValidationResult
from src.core.models.AgentServiceAttempt import AgentServiceAttempt, PartialAgentServiceAttempt
from src.core.models.EmployeeMessageBatch import EmployeeMessageBatch, PartialEmployeeMessageBatch
from src.core.repos.GameLogRepo import GameLogRepo
from src.core.services.AgentService import AgentService





ActionVerifier = Callable[[Action], ValidationResult]


class AgentServiceImpl(AgentService):
    def __init__(self, instructions: Dict[str, str], allowed_actions: Dict[str, List[Type[Action]]], gameLogRepo: GameLogRepo):
        self.instructions = instructions
        self.agent_cache: Dict[str, LLM] = {}
        for employee_name, _ in instructions.items():
            self.agent_cache[employee_name] = LLM(Claude(allowed_actions[employee_name]))

    async def choose_action(self, employee_name: str, state_message: str) -> PartialEmployeeMessageBatch:
        agent = self.agent_cache[employee_name]
        response = await agent.invoke_cached(self.instructions[employee_name], state_message, messages)
        action = parse_tool(response.tool_name, response.tool_args)
        response_message = ResponseMessage(content=response.original_response.content)
        tool_invocation = ToolInvocationMessage(tool=response.tool_name, tool_input=response.tool_args, tool_id=response.tool_id)
        return PartialEmployeeMessageBatch(response_message, tool_invocation, action)

    def _get_message_history(self, employee_name: str) -> List[StandardMessage]:
        agent = self.agent_cache[employee_name]
        return agent.get_message_history()