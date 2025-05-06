from typing import Protocol

from src.core.entities.grill import Grill


class EmployeeGrillService(Protocol):
    def find_closest_grill_to_employee(self, employee_id: str) -> Grill:
        """
        Get closest grill to employee
        """
        pass