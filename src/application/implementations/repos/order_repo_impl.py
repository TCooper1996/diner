import uuid
from typing import Dict, List

from src.core.entities.order import Order, OrderStatus
from src.core.repos.OrderRepo import OrderRepo


class OrderRepoImpl(OrderRepo):
    """
    Implementation of the OrderRepo protocol that stores orders in a dictionary.
    """

    def __init__(self):
        self._orders: Dict[str, Order] = {}
        self._next_order_id = 1

    def create_order(self) -> Order:
        """
        Create a new order in the repository.
        
        Returns:
            A new Order object with a unique ID.
        """
        order_id = f"order_{self._next_order_id}"
        self._next_order_id += 1
        
        order = Order(
            id=order_id,
            food_item="",
            status=OrderStatus.NOT_STARTED
        )
        
        self._orders[order_id] = order
        return order

    def get_order(self, order_id: str) -> Order:
        """
        Get an order by ID.
        
        Args:
            order_id: The ID of the order to get.
            
        Returns:
            The order with the specified ID.
            
        Raises:
            KeyError: If no order exists with the specified ID.
        """
        if order_id not in self._orders:
            raise KeyError(f"No order found with ID {order_id}")
        
        return self._orders[order_id]

    def get_all_orders(self) -> List[Order]:
        """
        Get all orders in the repository.
        
        Returns:
            A list of all orders.
        """
        return list(self._orders.values())

    def update_order(self, order: Order) -> None:
        """
        Update an existing order.
        
        Args:
            order: The order to update.
            
        Raises:
            KeyError: If no order exists with the specified ID.
        """
        if order.id not in self._orders:
            raise KeyError(f"No order found with ID {order.id} to update")
        
        self._orders[order.id] = order

    def add_order(self, order: Order) -> None:
        """
        Add a new order to the repository.
        
        Args:
            order: The order to add.
            
        Raises:
            ValueError: If an order with the same ID already exists.
        """
        if order.id in self._orders:
            raise ValueError(f"Order with ID {order.id} already exists")
        
        self._orders[order.id] = order