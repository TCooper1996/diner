import copy
from typing import Dict
from src.actions.customer.customer_action import GeneralCustomerAction
from src.application.misc.prompt_from_state import to_prompt
from src.core.models.GameState import GameState
from src.core.models.RestaurantState import RestaurantState
from src.application.services.TrunSelectionService import *
from src.game_engine.config import AgentService

"""
This class should only be referenced in this module
"""
@dataclass
class GameLoopState:
    game_state: GameState
    turn_selector: TurnSelectionService

async def game_loop(agent: AgentService, init_state: GameState, employee_ordering: List[str]):
    state = GameLoopState(game_state=init_state, turn_selector=TurnSelectionService(employee_ordering))
    while True:
        whose_turn = state.turn_selector.choose_turn()
        match whose_turn:
            case EmployeeTurn(employee_id=employee_id):
                await handle_employee_turn(state.game_state, agent, employee_id)
            case _:
                handle_customer_turn(state.game_state)
        yield copy.deepcopy(state.game_state)

async def handle_employee_turn(state: GameState, agent: AgentService, employee_id: str):
    current_action = state.action_repo.get_employee_action(employee_id)
    if current_action is None:
        state_message = to_prompt(state.restaurant_state)
        messages = state.message_repo.get_employee_messages(employee_id)
        current_action, new_messages = await agent.get_next_valid_action(employee_id, state_message, messages)
        state.message_repo.add_employee_messages(employee_id, new_messages)

    state_result = current_action.execute(state.restaurant_state, employee_id)
    state.message_repo.add_action_result(state_result.message)

    # Determine whether to continue with the action next time
    state.action_repo.set_employee_action(employee_id, current_action if state_result.repeat else None)


def handle_customer_turn(state: GameState):
    # Todo, this code should be similar to handle_employee_turn, in which every customer has an action
    GeneralCustomerAction().execute(state.restaurant_state, state.tick)