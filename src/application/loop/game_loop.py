import copy
from typing import Dict, Sequence, Tuple
from src.actions.customer.customer_action import GeneralCustomerAction
from src.agents.models.Model import StandardMessage
from src.application.implementations.models.GameStateImpl import GameStateImpl
from src.application.loop.handle_employee_turn import handle_employee_turn
from src.application.misc.prompt_from_state import to_prompt
from src.core.models.AgentServiceAttempt import AgentServiceAttempt, PartialAgentServiceAttempt
from src.core.models.EmployeeMessageBatch import EmployeeMessageBatch, EmployeeMessageBatchSet
from src.core.models.GameState import GameState
from src.core.models.RestaurantState import RestaurantState
from src.application.services.TrunSelectionService import *

"""
This class should only be referenced in this module
"""
@dataclass
class GameLoopState:
    game_state: GameStateImpl
    turn_selector: TurnSelectionService

async def game_loop(init_state: GameStateImpl, employee_ordering: List[str]):
    state = GameLoopState(game_state=init_state, turn_selector=TurnSelectionService(employee_ordering))
    while True:
        whose_turn = state.game_state.get_whose_turn()
        match whose_turn:
            case EmployeeUpdate(name):
                await handle_employee_turn(state.game_state, name)
            case _:
                handle_customer_turn(state.game_state)
        state.game_state.set_whose_turn(state.turn_selector.choose_turn(whose_turn))
        yield copy.deepcopy(state.game_state)




def handle_customer_turn(state: GameStateImpl):
    # Todo, this code should be similar to handle_employee_turn, in which every customer has an action
    GeneralCustomerAction().execute(state, state.tick)


# Utilities ------------------------------------------