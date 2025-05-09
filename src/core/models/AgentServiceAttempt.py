from dataclasses import dataclass
from typing import Protocol
from src.core.models.Action import Action
from src.core.models.EmployeeMessageBatch import EmployeeMessageBatch


class AgentServiceAttempt(EmployeeMessageBatch):
    ...


class PartialAgentServiceAttempt(Protocol):
    """Will end up representing a success, and is partial because we don't have the full response until the action is executed."""

    def resolve(self, tool_result: str) -> AgentServiceAttempt:
        """Resolve the partial message batch into a full one, by adding the tool result.
        This method will be used by the calling function.
        """
        ...

    def get_action(self) -> Action:
        """Get the action that was attempted"""
        ...



