
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class OrderStatus(Enum):
    # Not yet taken to the kitchen
    PENDING = "PENDING"
    # At the kitchen but not started cooking
    SUBMITTED = "SUBMITTED"
    # Currently being cooked
    COOKING = "COOKING"
    # Ready to be delivered
    READY = "READY"
    # Delivered to the customer
    DELIVERED = "DELIVERED"

OrderItem = Literal["burger", "fries", "salad", "pizza", "soda"]

counter = 0
def getId():
    global counter
    counter += 1
    return str(f"order_id_{counter}")

@dataclass
class Order:
    id: str = field(default_factory=lambda: getId())
    status: OrderStatus = field(default=OrderStatus.PENDING)

    def to_prompt(self) -> str:
        return f"""
Order ID: {self.id}
    Status: {self.status.value}
"""