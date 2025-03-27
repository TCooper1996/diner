"""Base classes and utilities for actions"""

import copy
from dataclasses import dataclass
from typing import Dict, List, Any, TYPE_CHECKING
from pydantic import BaseModel, Field

from src.game_engine.location import Location
from src.state.game import GameState
from src.state.restaurant_state import RestaurantState


def copy_args(fn):
    def wrapper(*args, **kwargs):
        new_args = [copy.deepcopy(arg) for arg in args]
        return fn(*new_args, **kwargs)
    return wrapper

@dataclass
class ActionResult:
    """
    Result of an action, including success status, message, and updated game state
    """
    success: bool
    message: str
    game_state: GameState

    def __init__(self, message: str, r_state: RestaurantState):
        self.message=message
        self.r_state = r_state

@dataclass
class ValidationResult:
    success: bool
    error_msg: str | None

