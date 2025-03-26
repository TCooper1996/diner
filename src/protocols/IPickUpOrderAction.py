from typing import Protocol

class IPickUpOrderAction(Protocol):
    """
    Protocol for pick up order action
    """
    order_id: str