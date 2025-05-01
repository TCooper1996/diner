from dataclasses import dataclass
from functools import partial, partialmethod
from typing import Any, List, Type
from src.actions import *
from src.agents.employeeAgent import LLM
from src.agents.models.Claude import Claude
from src.agents.models.Model import StandardMessage
from src.game_engine.choose_employee_action import ChooseActionFromAgentUsecase


class AgentService:
    def __init__(self, instructions: Dict[str, str], allowed_actions: Dict[str, List[Type[Action]]]):
        self.instructions = instructions
        self.agent_cache: Dict[str, LLM] = {}
        for employee_name, _ in instructions.items():
            self.agent_cache[employee_name] = LLM(Claude(allowed_actions[employee_name]))

    async def invoke_agent(self, employee_name: str, state_message: str, messages: List[StandardMessage]):
        agent = self.agent_cache[employee_name]
        invoke = lambda: agent.invoke_cached(self.instructions[employee_name], state_message, messages)
        return await ChooseActionFromAgentUsecase(invoke).choose_next_action()


@dataclass(frozen=True) # type: ignore
class Config:
    instructions: Dict[str, str]
    allowed_actions: Dict[str, List[Type[Action]]]
    agent_service: AgentService

    



def create_config():
        instructions = {
            "Alice": "You will seat customers as they come in.", 
            "Bob": "After Alice seats customers, you will take their orders and bring the orders to the kitchen to be submitted. "
                   "Once the orders are ready, bring them to their respective customers.", 
            "Jim": "As Bob brings you orders, you must cook them. "
                   "If there are no orders to cook, then wait."}
        allowed_actions: Dict[str, Any] = {
            "Alice": [WaitAction, SeatAction],
            "Bob": [WaitAction, TakeOrderAction, SubmitOrdersToKitchen, PickUpOrder, DeliverOrderToCustomer],
            "Jim": [WaitAction, CookAction]
        }
        AgentService(instructions, allowed_actions)
        return Config(instructions, allowed_actions, AgentService(instructions, allowed_actions))
