
import copy
from src.controllers.employee_controller import EmployeeAgentController
from src.state.game_state import GameState
from src.state.game_state.game_turn import GameTurn
from src.state.game_state.immutable_types.employee_turn import EmployeeTurn

async def employee_turn(gamestate: GameState, agent_controller: EmployeeAgentController, name: str) -> GameState:
    gamestate = copy.deepcopy(gamestate)
    turn = await agent_controller.process(gamestate, name)
    add_employee_turn(gamestate, turn)  # Add the turn to the game state
    return gamestate
    

def add_employee_turn(state: GameState, turn: EmployeeTurn):
    current_turn = state.turns.get(state.tick)
    if current_turn is None:
        # If there is no turn for the current tick, create a new GameTurn
        current_turn = GameTurn()
        state.turns[state.tick] = current_turn  # Store the new turn in the turns dictionary

    state.turns[state.tick].add_turn(turn)


