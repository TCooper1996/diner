from typing import Dict, List

from src.core.entities.order import Order
from src.core.repos.EmployeeOrderRepo import EmployeeOrderRepo


class EmployeeOrderRepoImpl(EmployeeOrderRepo):
    """
    Implementation of the EmployeeOrderRepo protocol that stores the relationships
    between employees and orders using dictionaries.
    
    Since we need to track two distinct relationships (orders taken and orders carried),
    we still use two dictionaries but each tracks only one direction of the relationship.
    """

    def __init__(self):
        # Map of employee_name to a list of order_ids
        self._employee_orders_taken: Dict[str, List[str]] = {}  
        self._employee_orders_carried: Dict[str, List[str]] = {}  

    def get_orders_taken(self, employee_name: str) -> list[str]:
        """
        Get the orders taken by an employee.
        
        Args:
            employee_name: The name of the employee.
            
        Returns:
            A list of order IDs taken by the employee.
        """
        return self._employee_orders_taken.get(employee_name, [])

    def add_order_taken(self, employee_name: str, order_id: str) -> None:
        """
        Add an order to the orders taken by an employee.
        
        Args:
            employee_name: The name of the employee.
            order_id: The ID of the order.
        """
        if employee_name not in self._employee_orders_taken:
            self._employee_orders_taken[employee_name] = []
        
        if order_id not in self._employee_orders_taken[employee_name]:
            self._employee_orders_taken[employee_name].append(order_id)

    def get_orders_carried(self, employee_name: str) -> list[str]:
        """
        Get the orders carried by an employee.
        
        Args:
            employee_name: The name of the employee.
            
        Returns:
            A list of order IDs carried by the employee.
        """
        return self._employee_orders_carried.get(employee_name, [])

    def add_order_carried(self, employee_name: str, order_id: str) -> None:
        """
        Add an order to the orders carried by an employee.
        
        Args:
            employee_name: The name of the employee.
            order_id: The ID of the order.
        """
        if employee_name not in self._employee_orders_carried:
            self._employee_orders_carried[employee_name] = []
        
        if order_id not in self._employee_orders_carried[employee_name]:
            self._employee_orders_carried[employee_name].append(order_id)

    def remove_orders_carried(self, employee_name: str, order_id: str) -> None:
        """
        Remove an order from the orders carried by an employee.
        
        Args:
            employee_name: The name of the employee.
            order_id: The ID of the order.
        """
        if employee_name in self._employee_orders_carried and order_id in self._employee_orders_carried[employee_name]:
            self._employee_orders_carried[employee_name].remove(order_id)
            
    def get_employee_with_order(self, order_id: str) -> str | None:
        """
        Find which employee is carrying a specific order.
        
        Args:
            order_id: The ID of the order.
            
        Returns:
            The name of the employee carrying the order, or None if not found.
        """
        for employee_name, orders in self._employee_orders_carried.items():
            if order_id in orders:
                return employee_name
        return None