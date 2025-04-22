
from dataclasses import dataclass
from typing import List

from src.agents.models.Model import ResponseMessage
from src.common.position import Position
from src.core.entities.info import EntityInfo
from src.core.entities.info.employee_info import EmployeeInfo, EmployeeTurnInfo
from src.core.entities.info.floor_info import FloorInfo
from src.state.game_state.game_state import GameState
from src.state.game_state.immutable_types.employee_turn import EmployeeTurn
from src.state.game_state.restaurant_state.restaurant_viewer import RestaurantViewer




def view_all_entities(state: GameState) -> List[EntityInfo]:
    r_employees = RestaurantViewer.view_employees(state.restaurant_state)
    customers: List[EntityInfo] = list(RestaurantViewer.view_customers(state.restaurant_state))
    stations: List[EntityInfo] = list(RestaurantViewer.view_stations(state.restaurant_state))
    employees: List[EntityInfo] = [EmployeeInfo(e.name, e.position, e.e.instruction, [get_turn_info(t) for t in state.get_employee_turns(e.name)]) for e in r_employees]
    floors: List[EntityInfo] = [FloorInfo(f) for f in state.restaurant_state.get_floors()]
    return employees + customers + stations + floors


def get_turn_info(e: EmployeeTurn) -> EmployeeTurnInfo:
    messages = [m.content for m in e.get_messages() if isinstance(m, ResponseMessage)]
    return EmployeeTurnInfo(e.employee_name, repr(e.action), messages, e.action_result_message)