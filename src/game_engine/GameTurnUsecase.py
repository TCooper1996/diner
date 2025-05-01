
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine, Dict, List, Tuple
from src.actions import Action
from src.game_engine.customer_turn import CustomerTurn, run_customer_update
from src.game_engine.select_employee_action import  Env, SelectActionUsecase
from src.state.game_state.restaurant_state.restaurant_state import RestaurantState
from .active_turn import EmployeeUpdate, CustomerUpdate, ActiveTurn





@dataclass
class GameState:
    restaurant_state: RestaurantState
    employees_current_actions: Dict[str, Action | None]
    active_turn: ActiveTurn
    tick: int


EmployeeName = str
StateMessageStr = str

class GameTurnUsecase:

    async def execute(self, gamestate: GameState, get_action_from_agent: Callable[[str, RestaurantState], Coroutine[Any, Any, Action]], run_employee_action: Callable[[RestaurantState, EmployeeName, Action], Tuple[RestaurantState, Action | None]]):
        gamestate.tick += 1
        match (gamestate.active_turn):
            case EmployeeUpdate(index=index):
                await self.employee_turn(gamestate, get_action_from_agent, run_employee_action, list(gamestate.restaurant_state.employees.keys())[index])
                gamestate.active_turn = CustomerUpdate() if index == len(gamestate.restaurant_state.employees) - 1 else EmployeeUpdate(index=index + 1)
            case CustomerUpdate():
                customer_turn_record = run_customer_update(gamestate.restaurant_state, gamestate.tick)
                gamestate.active_turn = EmployeeUpdate(index=0)
            case _:
                raise Exception("Invalid substate")



    async def employee_turn(self, gamestate: GameState,
        get_action_from_agent: Callable[[str, RestaurantState], Coroutine[Any, Any, Action]],
        run_employee_action: Callable[[RestaurantState, str, Action], Tuple[RestaurantState, Action | None]],
        employee: str):

        current_action = gamestate.employees_current_actions[employee]
        action = await SelectActionUsecase(lambda: get_action_from_agent(employee, gamestate.restaurant_state)).execute(current_action)

        # run action
        new_state, next_action = run_employee_action(gamestate.restaurant_state, employee, action)
        gamestate.restaurant_state = new_state
        gamestate.employees_current_actions[employee] = next_action
