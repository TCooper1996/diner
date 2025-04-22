from dataclasses import dataclass, replace
from typing import List, Optional

import pygame
import pygame_gui

from src.common.events.game_events import GameUpdateEvent, TurnSummary
from src.core.entities.info import EntityInfo
from src.core.entities.info.employee_info import EmployeeInfo, EmployeeTurnInfo
from src.tui.canvas.canvas_state import CanvasState
from src.tui.draw_level.draw_level import LevelEntityWithImage
from src.tui.gui.gui_state import GuiState
from src.tui.gui.ui_manager import UIManager


@dataclass(frozen=True)
class GameSnapshot:
    entities: List[EntityInfo]
    turn_summaries: List[TurnSummary]
    turn_num: int
    current_entity: str
    action: str
    agent_response: str | None
    action_result: str

    @classmethod
    def default(cls) -> 'GameSnapshot':
        return cls(
            entities=[],
            turn_summaries=[],
            turn_num=0,
            current_entity="",
            action="",
            agent_response=None,
            action_result=""
        )

@dataclass(frozen=True)
class WindowState:
    paused: bool
    current_turn_num: int
    width: int
    height: int
    initial_snapshot: GameSnapshot
    game_snapshots: List[GameSnapshot]

    @classmethod
    def default(cls):
        return cls(
            paused=False,
            current_turn_num=0,
            width=800,
            height=600,
            initial_snapshot=GameSnapshot.default(),
            game_snapshots=[]
        )


    @property
    def number_of_turns(self) -> int:
        return len(self.game_snapshots)

    @property
    def max_turn_num(self):
        return len(self.game_snapshots)-1

    @property
    def current_entity(self) -> str:
        if self.game_snapshots:
            return self.game_snapshots[self.current_turn_num].current_entity
        else:
            return "Turn hasn't started"

    @property
    def focused_snapshot(self) -> GameSnapshot:
        if self.game_snapshots:
            return self.game_snapshots[self.current_turn_num]
        return self.initial_snapshot


    def update(self, **kwargs) -> 'WindowState':
        return replace(self, **kwargs)

    def pause(self):
        return self.update(paused=not self.paused)

    def is_paused(self) -> bool:
        return not self.paused

    def restart(self) -> 'WindowState':
        return self.update(
            paused=False,
            current_turn_num=0,
            game_snapshots=[]
        )
