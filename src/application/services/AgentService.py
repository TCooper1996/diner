from dataclasses import dataclass
from typing import Callable, Dict, List, Protocol, Tuple, Type

from src.actions import  parse_tool
from src.agents.employeeAgent import LLM
from src.agents.models.Claude import Claude
from src.agents.models.Model import ResponseMessage, StandardMessage, ToolInvocationMessage, ToolResultMessage
from src.core.models.Action import Action, ValidationResult
from src.core.models.ActionSelection import ActionSelection
from src.core.models.AgentServiceAttempt import AgentServiceAttempt, PartialAgentServiceAttempt
from src.core.models.EmployeeMessageBatch import EmployeeMessageBatch, PartialEmployeeMessageBatch
from src.core.repos.GameLogRepo import GameLogRepo
from src.core.services.AgentService import AgentService
from langchain_core.messages import HumanMessage





ActionVerifier = Callable[[Action], ValidationResult]


class AgentServiceImpl(AgentService):
    def __init__(self, instructions: Dict[str, str], allowed_actions: Dict[str, List[Type[Action]]], gameLogRepo: GameLogRepo):
        self.instructions = instructions
        self.agent_cache: Dict[str, LLM] = {}
        self.gameLogRepo = gameLogRepo
        for employee_name, _ in instructions.items():
            self.agent_cache[employee_name] = LLM(Claude(allowed_actions[employee_name]))

    async def choose_action(self, employee_name: str, state_message: str) -> ActionSelection:

        messages = self._get_message_history(employee_name)
        agent = self.agent_cache[employee_name]
        response = await agent.invoke_cached(self.instructions[employee_name], state_message, messages)
        action = parse_tool(response.tool_name, response.tool_args)
        response_message = response.original_response.content
        return ActionSelection(action, response_message)

    def _get_message_history(self, employee_name: str) -> List[StandardMessage]:
        agent = self.agent_cache[employee_name]
        # Get all logs related to the employee
        logs = self.gameLogRepo.get_game_logs()
        employee_logs = [log for log in logs if log.get_employee_id() == employee_name]
        messages: List[StandardMessage] = []
        tool_id_counter = 0
        for log in employee_logs:
            if log.is_continued_action():
                messages.append(HumanMessage(content=log.get_execution_results()))

            else:
                for action_log in log.get_action_selection_logs():
                    messages.append(ResponseMessage(content=action_log.agent_response()))
                    action = action_log.get_action()
                    action_name_index = repr(action).find("(")
                    action_name = repr(action)[:action_name_index]
                    action_args = {field: getattr(action, field) for field in vars(action)}
                    messages.append(ToolInvocationMessage(
                        tool=action_name,
                        tool_input=action_args,
                        tool_id=str(tool_id_counter)
                    ))
                    # This represents whether the action was valid or not, NOT the execution result
                    messages.append(ToolResultMessage(
                        tool=action_name,
                        tool_output=action_log.get_verification_error() or "Successful",
                        tool_id=str(tool_id_counter),
                        is_error=action_log.get_verification_error() is not None
                    ))
                    tool_id_counter += 1


        return messages