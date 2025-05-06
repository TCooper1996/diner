from typing import List, Protocol

from src.agents.models.Model import StandardMessage



class EmployeeMessageRepo(Protocol):
    def get_employee_messages(self, employee_name) -> List[StandardMessage]:
        """Get the memory of an employee"""
        ...

    def add_employee_messages(self, employee_name, message: List[StandardMessage]):
        ...

    def add_action_result(self, result: str):
        ...