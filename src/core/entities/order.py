
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class OrderStatus(Enum):
    # Not yet taken to the kitchen
    PENDING = "PENDING: Has been taken by a server but not yet submitted to the kitchen"
    # At the kitchen but not started cooking
    SUBMITTED = "SUBMITTED: Has been taken to the kitchen but not yet started cooking."
    # Currently being cooked
    COOKING = "COOKING: Is currently being cooked"
    # Ready to be delivered
    READY = "READY: Is ready to be delivered"
    # Delivered to the customer
    DELIVERED = "DELIVERED: delivered"

OrderItem = Literal["burger", "fries", "salad", "pizza", "soda"]

counter = 0
def getId():
    global counter
    counter += 1
    return str(f"order_id_{counter}")

@dataclass
class Order:
    customer_id: str
    id: str = field(default_factory=lambda: getId())
    status: OrderStatus = field(default=OrderStatus.PENDING)

    def to_prompt(self) -> str:
        return f"""
Order ID: {self.id}
    Status: {self.status.value}
"""