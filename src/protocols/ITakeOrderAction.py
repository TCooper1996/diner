from typing import Protocol

class ITakeOrderAction(Protocol):
    """
    Protocol for take order action
    """
    customer_id: str