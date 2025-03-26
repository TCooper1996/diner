from typing import Protocol

class IMoveAction(Protocol):
    """
    Protocol for move action
    """
    destination: str