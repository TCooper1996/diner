"""Base classes and utilities for actions"""

from typing import Dict, List, Any, TYPE_CHECKING
from pydantic import BaseModel, Field

from src.game_engine.location import Location
from src.state.game import GameState


def copy_args(fn):
    def wrapper(*args, **kwargs):
        new_args = [arg.model_copy(deep=True) for arg in args]
        return fn(*new_args, **kwargs)
    return wrapper

class ActionResult(BaseModel):
    """
    Result of an action, including success status, message, and updated game state
    """
    success: bool
    message:str 
    game_state:GameState
