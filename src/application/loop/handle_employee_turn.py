
from typing import List, Tuple
from src.core.models.GameState import GameState


async def handle_employee_turn(state: GameState, employee_id: str):
    current_action = state.get_employee_action(employee_id)
    if current_action is None:
        failures, partial_success = await get_next_action(state, employee_id)
        current_action = partial_success.get_action()
        state_result = current_action.execute(state, employee_id)
        whole_attempt = partial_success.resolve(state_result.message)
        batchset = EmployeeMessageBatchSet([f for f in failures], whole_attempt)
        state.add_employee_message_batch(employee_id, batchset)
        
    else:
        # If the action is None, it means that the action was repeated
        # and we need to add the message to the memory
        state_result = current_action.execute(state, employee_id)
        state.add_single_message(employee_id, state_result.message)

    # Determine whether to continue with the action next time
    state.set_employee_action(employee_id, current_action if state_result.repeat else None)

# Utilities ------------------------------------------
async def get_next_action(state: GameState, employee_id: str) -> Tuple[List[AgentServiceAttempt], PartialAgentServiceAttempt]:
    return await state.get_next_valid_action(employee_id, to_prompt(state), state.get_employee_messages(employee_id), lambda action: action.verify(state, employee_id))