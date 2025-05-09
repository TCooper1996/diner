from typing import List, Protocol

from src.agents.models.Model import StandardMessage
from src.core.models.EmployeeMessageBatch import EmployeeMessageBatch, EmployeeMessageBatchSet



class EmployeeMessageRepo(Protocol):
    def get_employee_messages(self, employee_name) -> List[StandardMessage]:
        """Get the memory of an employee"""
        ...

    def add_employee_message_batch(self, employee_name: str, message: EmployeeMessageBatchSet):
        ...

    def add_single_message(self, employee_name: str, message: str):
        """Use when an action is repeated, since you wont be interacting with the agent and getting a response"""
        ...
