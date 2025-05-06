from dataclasses import dataclass, field
from typing import Dict, List, Optional, Protocol
from src.core.entities.order import Order, OrderStatus

class OrderRepo(Protocol):
    def create_order(self) -> Order:
        """Create a new order in the repository."""
        ...
    def get_order(self, order_id: str) -> Order:
        ...

    def get_all_orders(self) -> List[Order]:
        """Get all orders in the repository."""
        ...
        
    def update_order(self, order: Order) -> None:
        ...

    def add_order(self, order: Order) -> None:
        """Add a new order to the repository."""
        ...