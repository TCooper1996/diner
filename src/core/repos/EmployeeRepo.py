from typing import Protocol

from src.core.entities.employee import Employee


class EmployeeRepo(Protocol):
    def get_all_employees(self) -> list[Employee]:
        """Get all employees"""
        ...

    def get_employee(self, employee_id: str) -> Employee:
        """Get an employee by ID"""
        ...

    def update_employee(self, employee: Employee) -> None:
        """Update an employee"""
        ...