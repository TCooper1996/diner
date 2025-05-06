from src.actions import Action
from src.core.repos.ActionRepo import ActionRepo


class ActionRepoImpl(ActionRepo):
    """
    Implementation of the ActionRepo protocol that stores actions in a dictionary.
    """

    def __init__(self):
        self._employee_actions: dict[str, Action | None] = {}

    def set_employee_action(self, employee_id: str, action: Action | None) -> None:
        """
        Set the action of an employee.
        
        Args:
            employee_id: The ID of the employee.
            action: The action to set for the employee, or None to clear it.
        """
        self._employee_actions[employee_id] = action

    def get_employee_action(self, employee_id: str) -> Action | None:
        """
        Get the action of an employee.
        
        Args:
            employee_id: The ID of the employee.
            
        Returns:
            The action of the employee, or None if the employee has no action.
        """
        return self._employee_actions.get(employee_id)