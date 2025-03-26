from typing import Protocol

class IHandOrderToCustomerAction(Protocol):
    """
    Protocol for hand order to customer action
    """
    customer_id: str
    order_id: str