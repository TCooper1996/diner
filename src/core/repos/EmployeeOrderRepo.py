from typing import Protocol

from src.core.entities.order import Order


class EmployeeOrderRepo(Protocol):
    """
    Relationship repo that tracks which employees have taken which orders, and what orders an employee is carrying
    """
    def get_orders_taken(self, employee_name: str) -> list[Order]:
        """Get the orders taken by an employee"""
        ...

    def add_order_taken(self, employee_name: str, order_id: str) -> None:
        """Add an order to the orders taken by an employee"""
        ...

    def get_orders_carried(self, employee_name: str) -> list[Order]:
        """Get the orders carried by an employee"""
        ...

    def add_order_carried(self, employee_name: str, order_id: str) -> None:
        """Add an order to the orders carried by an employee"""
        ...

    def remove_orders_carried(self, employee_name: str, order_id: str) -> None:
        """Remove an order from the orders carried by an employee"""
        ...