from typing import Protocol

from src.core.models.Action import Action


class ActionSelection(Protocol):
    def get_action_instance(self) -> Action:
        """Get the action instance."""
        ...
    def get_description(self) -> str:
        """Get the description of the action."""
        ...