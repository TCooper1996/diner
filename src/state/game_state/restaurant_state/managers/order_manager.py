
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from src.core.entities.order import Order, OrderStatus

@dataclass
class OrderManager:
    orders: Dict[str, Order] = field( default_factory=dict)

    def add_order(self, order: Order) -> None:
        """Add an order to the manager"""
        self.orders[order.id] = order

    def get_order(self, order_id: str) -> Optional[Order]:
        return self.orders.get(order_id)

    def get_orders(self) -> List[Order]:
        return list(self.orders.values())

    def grab_order(self, /, order_id: str | None = None, customer_id: str | None = None) -> Order:
        if order_id:
            return self.orders[order_id]
        if customer_id:
            return [o for o in self.orders.values() if o.customer_id == customer_id][0]
        raise ValueError("Must provide either order_id or customer_id")

    def get_pending_orders(self):
        """Get orders that need to be cooked"""
        return [o for o in self.orders.values()
                if o.status == OrderStatus.PENDING]

    def get_ready_orders(self):
        """Get orders that are ready to be delivered"""
        return [o for o in self.orders.values()
                if o.status == OrderStatus.READY]
