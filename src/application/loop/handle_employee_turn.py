
from dataclasses import dataclass
from typing import List, Tuple
from src.application.misc.prompt_from_state import to_prompt
from src.core.models.Action import Action
from src.core.models.ActionSelection import ActionSelection
from src.core.models.GameState import GameState


@dataclass
class ActionSelectionLogImpl:
    _continued_action: bool
    _action: Action
    _verification_error: str | None
    _agent_response: str
    def agent_response(self) -> str :
        return self._agent_response
    def is_continued_action(self) -> bool:
        return self._continued_action
    def get_action(self) -> Action:
        return self._action
    def get_verification_error(self) -> str | None:
        return self._verification_error


async def handle_employee_turn(state: GameState, employee_id: str):
    action = await get_next_action(state, employee_id)

    state_result = action.execute(state, employee_id)
    state.add_turn_effect(state.get_tick(), state_result.message)
    # Determine whether to continue with the action next time
    state.set_employee_action(employee_id, action if state_result.repeat else None)

# Utilities ------------------------------------------
async def get_next_action(state: GameState, employee_id: str) -> Action:
    existing_action = state.get_employee_action(employee_id)
    if existing_action:
        return existing_action

    for i in range (3):
        selection = await state.choose_action(employee_id, to_prompt(state))
        result = selection.action.verify(state, employee_id)
        log = ActionSelectionLogImpl(False, selection.action, result.error_msg, selection.description)
        state.add_turn_log(False, state.get_tick(), employee_id, log)
        if result.success:
            return selection.action

    raise Exception("No valid action selected after 3 attempts.")