from typing import Dict, List, Set

from src.core.entities.order import Order
from src.core.repos.EmployeeOrderRepo import EmployeeOrderRepo


class EmployeeOrderRepoImpl(EmployeeOrderRepo):
    """
    Implementation of the EmployeeOrderRepo protocol that stores the relationships
    between employees and orders in dictionaries.
    """

    def __init__(self):
        self._orders_taken: Dict[str, Set[str]] = {}  # employee_name -> set of order_ids
        self._orders_carried: Dict[str, Set[str]] = {}  # employee_name -> set of order_ids
        self._orders: Dict[str, Order] = {}  # order_id -> Order (cache)

    def add_order(self, order: Order) -> None:
        """
        Add an order to the repository cache.
        
        Args:
            order: The order to add.
        """
        self._orders[order.id] = order

    def get_orders_taken(self, employee_name: str) -> list[Order]:
        """
        Get the orders taken by an employee.
        
        Args:
            employee_name: The name of the employee.
            
        Returns:
            The list of orders taken by the employee.
        """
        order_ids = self._orders_taken.get(employee_name, set())
        return [self._orders[order_id] for order_id in order_ids if order_id in self._orders]

    def add_order_taken(self, employee_name: str, order_id: str) -> None:
        """
        Add an order to the orders taken by an employee.
        
        Args:
            employee_name: The name of the employee.
            order_id: The ID of the order.
            
        Raises:
            KeyError: If the order with the specified ID doesn't exist in the cache.
        """
        if order_id not in self._orders:
            raise KeyError(f"No order found with ID {order_id}")
        
        if employee_name not in self._orders_taken:
            self._orders_taken[employee_name] = set()
        
        self._orders_taken[employee_name].add(order_id)

    def get_orders_carried(self, employee_name: str) -> list[Order]:
        """
        Get the orders carried by an employee.
        
        Args:
            employee_name: The name of the employee.
            
        Returns:
            The list of orders carried by the employee.
        """
        order_ids = self._orders_carried.get(employee_name, set())
        return [self._orders[order_id] for order_id in order_ids if order_id in self._orders]

    def add_order_carried(self, employee_name: str, order_id: str) -> None:
        """
        Add an order to the orders carried by an employee.
        
        Args:
            employee_name: The name of the employee.
            order_id: The ID of the order.
            
        Raises:
            KeyError: If the order with the specified ID doesn't exist in the cache.
        """
        if order_id not in self._orders:
            raise KeyError(f"No order found with ID {order_id}")
        
        if employee_name not in self._orders_carried:
            self._orders_carried[employee_name] = set()
        
        self._orders_carried[employee_name].add(order_id)

    def remove_orders_carried(self, employee_name: str, order_id: str) -> None:
        """
        Remove an order from the orders carried by an employee.
        
        Args:
            employee_name: The name of the employee.
            order_id: The ID of the order.
        """
        if employee_name in self._orders_carried and order_id in self._orders_carried[employee_name]:
            self._orders_carried[employee_name].remove(order_id)