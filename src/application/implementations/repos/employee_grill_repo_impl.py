from src.core.entities.grill import Grill
from src.core.repos.EmployeeGrillRepo import EmployeeGrillRepo


class EmployeeGrillRepoImpl(EmployeeGrillRepo):
    """
    Implementation of the EmployeeGrillRepo protocol that manages the relationship
    between employees and grills using a single dictionary.
    """

    def __init__(self):
        self._employee_grills: dict[str, str] = {}  # employee_id -> grill_id

    def get_employee_grill(self, employee_id: str) -> str | None:
        """
        Get the grill ID assigned to an employee by their ID.
        
        Args:
            employee_id: The ID of the employee.
            
        Returns:
            The grill ID assigned to the employee, or None if the employee has no grill assigned.
        """
        return self._employee_grills.get(employee_id)

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
        grill_employee = self.get_employee_of_grill(grill_id)
        if grill_employee and grill_employee != employee_id:
            raise ValueError(f"Grill {grill_id} is already assigned to employee {grill_employee}")
        
        # Set the new association
        self._employee_grills[employee_id] = grill_id

    def is_grill_occupied(self, grill_id: str) -> bool:
        """
        Check if a grill is assigned to an employee.
        
        Args:
            grill_id: The ID of the grill to check.
            
        Returns:
            True if the grill is assigned to an employee, False otherwise.
        """
        return self.get_employee_of_grill(grill_id) is not None
        
    def get_grill_of_employee(self, employee_id: str) -> str | None:
        """
        Get the grill ID assigned to an employee.
        
        Args:
            employee_id: The ID of the employee.
            
        Returns:
            The grill ID assigned to the employee, or None if the employee has no grill assigned.
        """
        return self._employee_grills.get(employee_id)
        
    def get_employee_of_grill(self, grill_id: str) -> str | None:
        """
        Get the employee ID assigned to a grill.
        
        Args:
            grill_id: The ID of the grill.
            
        Returns:
            The employee ID assigned to the grill, or None if the grill is not assigned.
        """
        grill_employees = {v: k for k, v in self._employee_grills.items()}
        return grill_employees.get(grill_id)