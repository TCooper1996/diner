"""Base classes and utilities for actions"""

from __future__ import annotations  # Enables string annotations
import copy
from dataclasses import dataclass

from src.common.position import Position

# Removed ActionResult and ValidationResult import as they are not directly used here

def copy_args(fn):
    def wrapper(*args, **kwargs):
        import copy  # Local import to avoid circular dependency
        new_args = [copy.deepcopy(arg) for arg in args]
        return fn(*new_args, **kwargs)
    return wrapper

@dataclass
class Movement:
    from_location: Position
    current_location: Position
    to_location: Position

    def __str__(self):
        return f"Move(from={self.from_location}, current={self.current_location}, to={self.to_location})"
