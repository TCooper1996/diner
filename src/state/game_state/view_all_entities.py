
from dataclasses import dataclass
from typing import Dict, List

from src.agents.models.Model import ResponseMessage
from src.common.position import Position
from src.core.entities.info import EntityInfo
from src.core.entities.info.employee_info import EmployeeInfo, EmployeeTurnInfo
from src.core.entities.info.floor_info import FloorInfo
from src.game_engine.GameTurnUsecase import EmployeeTurn, GameState
from src.state.game_state.restaurant_state.restaurant_viewer import RestaurantViewer


def view_all_entities(state: GameState) -> List[EntityInfo]:
    r_employees = RestaurantViewer.view_employees(state.restaurant_state)
    state.get_employee_turns()

    customers: List[EntityInfo] = list(RestaurantViewer.view_customers(state.restaurant_state))
    stations: List[EntityInfo] = list(RestaurantViewer.view_stations(state.restaurant_state))
    employees: List[EntityInfo] = [EmployeeInfo(e.name, e.position, e.e.instruction, [get_turn_info(t) for t in state.get_employee_turns() if t.name == e]) for e in r_employees]
    floors: List[EntityInfo] = [FloorInfo(f) for f in state.restaurant_state.get_floors()]
    return employees + customers + stations + floors


def get_turn_info(e: EmployeeTurn) -> EmployeeTurnInfo:
    messages = [a.text_response.content for a in e.attempts]
    return EmployeeTurnInfo(e.name, repr(e.get_action()), messages, messages[-1] if messages else "No result")