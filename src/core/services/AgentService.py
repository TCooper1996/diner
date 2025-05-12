

from typing import Callable, List, Protocol, Tuple

from src.agents.models.Model import StandardMessage
from src.core.models.Action import Action, ValidationResult
from src.core.models.ActionSelection import ActionSelection
from src.core.models.AgentServiceAttempt import AgentServiceAttempt, PartialAgentServiceAttempt
from src.core.models.EmployeeMessageBatch import EmployeeMessageBatch


class AgentService(Protocol):
    async def choose_action(self, employee_name: str, state_message: str) -> ActionSelection:
        """Get the next valid action for the given employee."""
        ...