
from dataclasses import dataclass
from src.controllers.employee_controller import EmployeeAgentController
from src.game_engine.employee_turn import employee_turn
from src.state.game_state.game_state import GameState
from .active_turn import EmployeeUpdate, CustomerUpdate, ActiveTurn
from src.state.game_state import  update_customers

@dataclass
class LoopResult:
    gameState: GameState
    nextTurn: ActiveTurn

async def loop(active_turn: ActiveTurn, gamestate: GameState, controller: EmployeeAgentController) -> LoopResult:
    match (active_turn):
        case EmployeeUpdate(index=index):
            employees = list(gamestate.restaurant_state.employee_names)
            employee = employees[index % len(employees)]
            new_state = await employee_turn(gamestate, controller, employee)
            next_turn = CustomerUpdate() if index == len(employees) - 1 else EmployeeUpdate(index=index + 1)

            return LoopResult(gameState=new_state, nextTurn=next_turn)
        case CustomerUpdate():
            gamestate.tick += 1
            return LoopResult(gameState=update_customers(gamestate), nextTurn=EmployeeUpdate(index=0))
        case _:
            raise Exception("Invalid substate")