from src.core.entities.grill import Grill
from src.core.repos.EmployeeGrillRepo import EmployeeGrillRepo


class EmployeeGrillRepoImpl(EmployeeGrillRepo):
    """
    Implementation of the EmployeeGrillRepo protocol that manages the relationship
    between employees and grills using dictionaries.
    """

    def __init__(self):
        self._employee_grills: dict[str, str] = {}  # employee_id -> grill_id
        self._grill_employees: dict[str, str] = {}  # grill_id -> employee_id
        self._grills: dict[str, Grill] = {}  # grill_id -> Grill (cache)

    def add_grill(self, grill: Grill) -> None:
        """
        Add a grill to the repository.
        
        Args:
            grill: The grill to add.
        """
        self._grills[grill.id] = grill

    def get_employee_grill(self, employee_id: str) -> Grill | None:
        """
        Get the grill assigned to an employee by their ID.
        
        Args:
            employee_id: The ID of the employee.
            
        Returns:
            The grill assigned to the employee, or None if the employee has no grill assigned.
        """
        grill_id = self._employee_grills.get(employee_id)
        if not grill_id:
            return None
        
        return self._grills.get(grill_id)

    def set_employee_grill(self, employee_id: str, grill_id: str) -> None:
        """
        Set the grill assigned to an employee by their ID.
        
        Args:
            employee_id: The ID of the employee.
            grill_id: The ID of the grill to assign.
            
        Raises:
            ValueError: If the grill is already assigned to another employee.
        """
        # Check if the grill is already assigned to another employee
        if grill_id in self._grill_employees and self._grill_employees[grill_id] != employee_id:
            raise ValueError(f"Grill {grill_id} is already assigned to employee {self._grill_employees[grill_id]}")
        
        # If the employee already has a grill, remove that association
        if employee_id in self._employee_grills:
            old_grill_id = self._employee_grills[employee_id]
            if old_grill_id in self._grill_employees:
                del self._grill_employees[old_grill_id]
        
        # Set the new association
        self._employee_grills[employee_id] = grill_id
        self._grill_employees[grill_id] = employee_id

    def is_grill_occupied(self, grill_id: str) -> bool:
        """
        Check if a grill is assigned to an employee.
        
        Args:
            grill_id: The ID of the grill to check.
            
        Returns:
            True if the grill is assigned to an employee, False otherwise.
        """
        return grill_id in self._grill_employees