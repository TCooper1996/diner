
from enum import Enum
from typing import List, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class OrderStatus(Enum):
    # Not yet taken to the kitchen
    PENDING = "pending"
    # At the kitchen but not started cooking
    TAKEN = "taken"
    # Currently being cooked
    COOKING = "cooking"
    # Ready to be delivered
    READY = "ready"
    # Delivered to the customer
    DELIVERED = "delivered"

OrderItem = Literal["burger", "fries", "salad", "pizza", "soda"]

counter = 0
def getId():
    global counter
    counter += 1
    return str(counter)

class Order(BaseModel):
    customer_id: str
    id: str = Field(default_factory=lambda: getId())
    items: List[OrderItem]
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    # The server that owns the order and must deliver it to the kitchen
    server: str 