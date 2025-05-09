from typing import Protocol


class EmployeeGrillRepo(Protocol):
    def get_employee_grill(self, employee_id: str) -> str | None:
        """Get the grill assigned to an employee by their ID."""
        ...
        
    def set_employee_grill(self, employee_id: str, grill_id: str) -> None:
        """Set the grill assigned to an employee by their ID."""
        ...

    def is_grill_occupied(self, grill_id: str) -> bool:
        """Check if a grill is assigned to an employee."""
        ... 