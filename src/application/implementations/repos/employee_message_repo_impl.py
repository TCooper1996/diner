from typing import Dict, List

from src.agents.models.Model import StandardMessage
from src.core.repos.EmployeeMessageRepo import EmployeeMessageRepo


class EmployeeMessageRepoImpl(EmployeeMessageRepo):
    """
    Implementation of the EmployeeMessageRepo protocol that stores employee messages
    in a dictionary.
    """

    def __init__(self):
        self._employee_messages: Dict[str, List[StandardMessage]] = {}
        self._action_results: List[str] = []

    def get_employee_messages(self, employee_name: str) -> List[StandardMessage]:
        """
        Get the memory of an employee.
        
        Args:
            employee_name: The name of the employee.
            
        Returns:
            The list of messages for the employee, or an empty list if none exist.
        """
        return self._employee_messages.get(employee_name, [])

    def add_employee_messages(self, employee_name: str, messages: List[StandardMessage]) -> None:
        """
        Add messages to an employee's memory.
        
        Args:
            employee_name: The name of the employee.
            messages: The messages to add.
        """
        if employee_name not in self._employee_messages:
            self._employee_messages[employee_name] = []
        
        self._employee_messages[employee_name].extend(messages)

    def add_action_result(self, result: str) -> None:
        """
        Add an action result to the repository.
        
        Args:
            result: The action result to add.
        """
        self._action_results.append(result)
    
    def get_action_results(self) -> List[str]:
        """
        Get all action results.
        
        Returns:
            The list of all action results.
        """
        return self._action_results.copy()