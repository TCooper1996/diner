from src.core.entities.employee import Employee
from src.core.repos.EmployeeRepo import EmployeeRepo


class EmployeeRepoImpl(EmployeeRepo):
    """
    Implementation of the EmployeeRepo protocol that stores employees in a dictionary.
    """

    def __init__(self):
        self._employees: dict[str, Employee] = {}

    def get_all_employees(self) -> list[Employee]:
        """
        Get all employees.
        
        Returns:
            A list of all employees.
        """
        return list(self._employees.values())

    def get_employee(self, employee_id: str) -> Employee:
        """
        Get an employee by ID.
        
        Args:
            employee_id: The ID of the employee to get.
            
        Returns:
            The employee with the specified ID.
            
        Raises:
            KeyError: If no employee exists with the specified ID.
        """
        if employee_id not in self._employees:
            raise KeyError(f"No employee found with ID {employee_id}")
        
        return self._employees[employee_id]

    def update_employee(self, employee: Employee) -> None:
        """
        Update an employee or add if not exists.
        
        Args:
            employee: The employee to update.
        """
        self._employees[employee.id] = employee
    
    def add_employee(self, employee: Employee) -> None:
        """
        Add a new employee.
        
        Args:
            employee: The employee to add.
            
        Raises:
            ValueError: If an employee with the same ID already exists.
        """
        if employee.id in self._employees:
            raise ValueError(f"Employee with ID {employee.id} already exists")
        
        self._employees[employee.id] = employee