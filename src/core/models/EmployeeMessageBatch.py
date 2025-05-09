from dataclasses import dataclass
from typing import List, Protocol

from src.agents.models.Model import StandardMessage


@dataclass
class EmployeeMessageBatch(Protocol):
    """
    Each instances represents the messages that arise from a single agent attempt.
    Specifically, the agents response, and the result of their action (which may be a successful action execution or a failed validation result)
    """    
    ...

    def get_standard_messages(self) -> List[StandardMessage]:
        """Can be fed into the LLM"""
        ...

    def get_agent_response_string(self) -> str | None:
        """The agent's response to the action"""
        ...
        
    def get_action_result_string(self) -> str:
        """The result of the action"""
        ...

@dataclass
class EmployeeMessageBatchSet:
    failures: List[EmployeeMessageBatch]
    value: EmployeeMessageBatch

@dataclass
class EmployeeMessageEntry(Protocol):
    def _get_standard_messages(self) -> List[StandardMessage]:
        """Can be fed into the LLM"""
        ...
    def get_action_result_string(self) -> str:
        """The result of the action"""
        ...
