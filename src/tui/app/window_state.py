from dataclasses import dataclass, replace
from typing import List, Optional, TypedDict

import pygame
import pygame_gui

from src.common.events.game_events import GameUpdateEvent, TurnSummary
from src.common.position import FPosition
from src.core.types import StationType

@dataclass
class HasName:
    name: str

@dataclass
class HasPosition:
    position: FPosition

@dataclass
class EmployeeInfo(HasName, HasPosition):
    pass

@dataclass
class CustomerInfo(HasName, HasPosition):
    pass

@dataclass
class StationInfo(HasPosition):
    station_type: StationType
    pass

@dataclass
class FloorInfo(HasPosition):
    pass



@dataclass
class WindowPositionRepo:
    employees: List[EmployeeInfo]
    customers: List[CustomerInfo]
    stations: List[StationInfo]
    floors: List[FloorInfo]

class WindowTurnSummary(TypedDict):
    entity_name: str
    action: str
    agent_response: str | None
    action_result: str


@dataclass(frozen=True)
class WindowGameSnapshot:
    entity_repo: WindowPositionRepo
    current_entity: str
    turn_summaries: List[WindowTurnSummary]

    @classmethod
    def default(cls):
        return cls(
            entity_repo=WindowPositionRepo(
                employees=[],
                customers=[],
                stations=[],
                floors=[]
            ),
            turn_summaries=[],
            current_entity="",
        )


@dataclass(frozen=True)
class WindowState:
    paused: bool
    current_turn_num: int
    max_turn: int
    width: int
    height: int
    game_snapshot: WindowGameSnapshot

    @classmethod
    def default(cls):
        return cls(
            paused=False,
            current_turn_num=0,
            max_turn=0,
            width=800,
            height=600,
            game_snapshot=WindowGameSnapshot.default()
        )

