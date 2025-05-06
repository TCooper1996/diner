from dataclasses import dataclass
from functools import partial, partialmethod
from typing import Any, List, Type
from src.actions import *
from src.agents.employeeAgent import LLM
from src.agents.models.Claude import Claude
from src.agents.models.Model import StandardMessage
from src.application.services.AgentService import AgentService




@dataclass(frozen=True) # type: ignore
class Config:
    instructions: Dict[str, str]
    allowed_actions: Dict[str, List[Type[Action]]]

    



def create_config():
        return Config(instructions, allowed_actions, AgentService(instructions, allowed_actions))
