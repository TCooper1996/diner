from typing import Dict, List

from src.agents.models.Model import StandardMessage
from src.core.models.EmployeeMessageBatch import EmployeeMessageBatch, EmployeeMessageBatchSet
from src.core.repos.EmployeeMessageRepo import EmployeeMessageRepo


class EmployeeMessageRepoImpl(EmployeeMessageRepo):
    """
    Implementation of the EmployeeMessageRepo protocol that stores employee messages
    in a dictionary.
    """

    def __init__(self):
        self._employee_messages: Dict[str, List[EmployeeMessageBatchSet]] = {}

    def get_employee_messages(self, employee_name: str) -> List[StandardMessage]:
        messages = self._employee_messages.get(employee_name, [])
        return [m for mset in messages for batch in mset.failures + [mset.value] for m in batch.get_standard_messages()]


    def add_employee_messages(self, employee_name: str, messages: EmployeeMessageBatchSet) -> None:
        if employee_name not in self._employee_messages:
            self._employee_messages[employee_name] = []
        
        self._employee_messages[employee_name].append(messages)

    def get_last_message_batch(self, employee_name: str) -> EmployeeMessageBatchSet:
        if employee_name in self._employee_messages and self._employee_messages[employee_name]:
            return self._employee_messages[employee_name][-1]
        raise ValueError(f"No messages found for employee: {employee_name}")
