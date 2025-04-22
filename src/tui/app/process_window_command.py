
from src.tui.app.intent import *
from src.tui.app.window_state import GameSnapshot, WindowState


def process_window_command(state: WindowState, command: AppCommand) -> WindowState:

    match command.command:
        case GameUpdateCommand(GameUpdateEvent(entities, turn_history, name_of_turn_entity, turn_number, action, agent_response, response_result)):
            current_turn = state.max_turn_num + 1 if latest_turn_focused(state) else state.current_turn_num
            return state.update(
                game_snapshots=[*state.game_snapshots, GameSnapshot(entities, turn_history, turn_number, name_of_turn_entity, action, agent_response, response_result)],
                current_turn_num=current_turn,
            )
        case ResizeCommand(width, height):
            return state.update(width=width, height=height)
        case ViewNextTickCommand():
            current_turn=min(state.current_turn_num+1, state.max_turn_num)
            return state.update(current_turn_num=current_turn)
        case ViewPreviousTickCommand():
            new_turn = max(state.current_turn_num-1, 0)
            return state.update(current_turn_num=new_turn)
        case _:
            raise NotImplementedError(f"Command {command} not implemented")



def latest_turn_focused(state: WindowState) -> bool:
    return state.current_turn_num == state.max_turn_num or state.number_of_turns == 0