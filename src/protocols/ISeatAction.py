from typing import Protocol

class ISeatAction(Protocol):
    """
    Protocol for seat action
    """
    customer_id: str