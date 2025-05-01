
from dataclasses import dataclass
from typing import Any, Callable, Coroutine
from src.actions import Action


@dataclass
class SelectActionUsecase:
    select_action_from_agent: Callable[[], Coroutine[Any, Any, Action]]


    async def execute(self, employee_current_action: Action | None) -> Action:
        # If the employee has no current action, choose a new action
        if employee_current_action:
            return (employee_current_action)
        return await self.select_action_from_agent()

