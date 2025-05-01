
import datetime
import math
from pathlib import Path
import threading
from time import time
from typing import Dict, List, Literal, Optional
import pygame
from dataclasses import field, replace
from src.common.event_manager import EventManager
from src.common.events import GameEvent, GuiEvent
from src.common.events.gui_events import ResetGame, Pause
from src.common.position import FPosition, Position
from src.core.entities import info as core
from src.core.types import StationType
from src.tui.app.intent import *
from src.tui.app.get_event import all_events
from src.tui.app.turn_manager import TurnManager
from src.tui.app.update_window import  update_window
from src.tui.gui.ui_manager import UIManager
from src.tui.app.window_state import  WindowGameSnapshot, WindowPositionRepo, WindowState, WindowTurnSummary
from src.tui.app import window_state as window

@dataclass
class AppLoopState:
    paused: bool
    height: int
    width: int
    turn_manager: TurnManager[GameUpdateEvent]
    animation_delta: float = 0.0
    previous_turn: Optional[GameUpdateEvent] = None
    await_initial_update: bool = False

    def get_current(self) -> GameUpdateEvent:
        return self.turn_manager.get_current()
    
    def get_previous(self) -> Optional[GameUpdateEvent]:
        return self.turn_manager.get_previous()

class MovingEntityInfo:
    name: str
    position: FPosition

@dataclass
class EntityRepo:
    entity_positions: Dict[str, FPosition]
    employee_names: List[str]
    customer_names: List[str]
    station_ids: List[str]
    station_types: Dict[str, StationType]
    floor_ids: List[str]

    def get_npc_position(self, name) -> FPosition:
        return self.entity_positions[name]

    @property
    def npc_names(self) -> List[str]:
        return self.employee_names + self.customer_names

LoopEndReason = Literal["Quit", "Restart"]

def loop(first_update: GameUpdateEvent,event_manager: EventManager[GameEvent, GuiEvent], widgets: UIManager, surface: pygame.Surface) -> LoopEndReason:
    clock = pygame.Clock()
    current_state = AppLoopState(paused=False, height=surface.get_height(), width=surface.get_width(), turn_manager=TurnManager(first_update))
    while True:
        time_delta = clock.tick(60)/1000
        current_state.animation_delta = min(1, current_state.animation_delta + time_delta)  # Cap animation delta to 1.0
        for event in  all_events(event_manager, widgets):
            exit = handle_event_v2(event, current_state, event_manager)

            if exit:
                return exit

        previous_turn = current_state.get_previous()
        current_turn = current_state.get_current()
        window_state = create_window_state(current_state, previous_game_state=previous_turn, current_game_state=current_turn)
        update_window(widgets, surface, window_state, time_delta)


def handle_event_v2(event: AppCommand, state: AppLoopState, event_manager: EventManager[GameEvent, GuiEvent]) -> Literal["Quit", "Restart"] | None:
    if not isinstance(event, (ResizeCommand, QuitCommand, RestartCommand, PauseCommand, GameUpdateCommand, ViewPreviousTickCommand, ViewNextTickCommand)):
        raise NotImplementedError(f"Event {event} not implemented")

    match event:
        case ResizeCommand(width, height):
            state.height = height
            state.width = width

        case QuitCommand():
            return "Quit"

        case RestartCommand():
            return "Restart"

        case PauseCommand():
            state.paused = not state.paused
            event_manager.put_event(Pause())

        case GameUpdateCommand(game_update):
            state.turn_manager.append(game_update)
            

        case ViewPreviousTickCommand():
            state.turn_manager.decrement()

        case ViewNextTickCommand():
            state.turn_manager.increment()

        case _:
            raise NotImplementedError(f"Event {event} not implemented")

    # Reset animation delta for certain events

    # If game is updated and we're focused on the latest turn, reset animation delta
    if isinstance(event, GameUpdateCommand):
        if state.turn_manager.is_latest_turn_focused():
            state.animation_delta = 0.0

    if isinstance(event, (ViewNextTickCommand, ViewPreviousTickCommand)):
        # These commands reset animations
        state.animation_delta = 0.0

    if isinstance(event, (GameUpdateCommand, ViewPreviousTickCommand, ViewNextTickCommand)):
        # If we are viewing a previous turn, reset animation delta
        if not state.turn_manager.is_latest_turn_focused():
            state.animation_delta = 0.0
    return None


def create_window_entity_repo(entities: EntityRepo) -> WindowPositionRepo:
    employees = [window.EmployeeInfo(name=emp, position=entities.entity_positions[emp]) for emp in entities.employee_names]
    customers = [window.CustomerInfo(name=customer, position=entities.entity_positions[customer]) for customer in entities.customer_names]
    stations = [window.StationInfo(position=entities.entity_positions[station], station_type=entities.station_types[station]) for station in entities.station_ids]
    floors = [window.FloorInfo(position=entities.entity_positions[floor]) for floor in entities.floor_ids]

    return WindowPositionRepo(
        employees=employees,
        customers=customers,
        stations=stations,
        floors=floors
    )

def create_window_state(state: AppLoopState, previous_game_state: Optional[GameUpdateEvent], current_game_state: GameUpdateEvent) -> WindowState:
    current_entity = current_game_state.name_of_turn_entity

    entity_repo = create_entity_repo(current_game_state)
    # Animate positions

    if previous_game_state:
        previous_entity_repo = create_entity_repo(previous_game_state)
        previous_positions = previous_entity_repo.entity_positions
        current_positions = entity_repo.entity_positions

        named_entities = entity_repo.npc_names
        changed_entities = [entity for entity in named_entities if entity in previous_positions and entity in current_positions and previous_positions[entity] != current_positions[entity]]
        for entity in changed_entities:
            animated_position = interpolate_positions(
                start=previous_positions[entity],
                end=current_positions[entity],
                delta=state.animation_delta
            )
            entity_repo.entity_positions[entity] = animated_position

    window_entity_repo = create_window_entity_repo(entity_repo)
    turn_summaries: List[WindowTurnSummary] = [WindowTurnSummary(entity_name=t.entity_name, action=t.action, agent_response= t.response, action_result= t.result) for t in current_game_state.turn_history]
    game_snapshot = WindowGameSnapshot(window_entity_repo, current_entity, turn_summaries)
    return WindowState(
        paused=state.paused,
        current_turn_num=state.turn_manager.ordinal_turn,
        max_turn=state.turn_manager.num_turns,
        width=state.width,
        height=state.height,
        game_snapshot=game_snapshot
    )

def create_entity_repo(game_update: GameUpdateEvent) -> EntityRepo:
    def entity_id(e: core.EntityInfo):
        match e:
            case core.EmployeeInfo(name=name):
                return name
            case core.CustomerInfo(name=name):
                return name
            case core.StationInfo(station_id=station_id):
                return station_id
            case core.FloorInfo(position=position):
                return f"{position.x},{position.y}"
            case _:
                raise ValueError(f"Unknown entity type: {type(e)}")

    entity_positions = {entity_id(e): FPosition.from_position(e.position) for e in game_update.entities}
    employee_names = [e.name for e in game_update.entities if isinstance(e, core.EmployeeInfo)]
    customer_names = [e.name for e in game_update.entities if isinstance(e, core.CustomerInfo)]

    station_ids = [s.station_id for s in game_update.entities if isinstance(s, core.StationInfo)]
    station_types = {s.station_id: s.station_type for s in game_update.entities if isinstance(s, core.StationInfo)}
    floor_ids = [f"{f.position.x},{f.position.y}" for f in game_update.entities if isinstance(f, core.FloorInfo)]

    return EntityRepo(
        entity_positions=entity_positions,
        employee_names=employee_names,
        customer_names=customer_names,
        station_ids=station_ids,
        station_types=station_types,
        floor_ids=floor_ids
    )



def interpolate_positions(start: FPosition, end: FPosition, delta: float) -> FPosition:
    return FPosition(
        x=start.x + (end.x - start.x) * delta,
        y=start.y + (end.y - start.y) * delta
    )
