from dataclasses import dataclass, replace
from typing import List, Optional, TypedDict

import pygame
import pygame_gui

from src.common.position import FPosition
from src.core.models.GameState import GameState
from src.core.types import StationType



@dataclass(frozen=True)
class WindowState:
    paused: bool
    current_turn_num: int
    max_turn: int
    width: int
    height: int
    game_snapshot:GameState 

    @classmethod
    def default(cls, game_snapshot: GameState) -> "WindowState":
        return cls(
            paused=False,
            current_turn_num=0,
            max_turn=0,
            width=800,
            height=600,
            game_snapshot=game_snapshot,
        )

