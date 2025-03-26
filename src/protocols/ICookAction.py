from typing import Protocol

class ICookAction(Protocol):
    """
    Protocol for cook action
    """
    order_id: str