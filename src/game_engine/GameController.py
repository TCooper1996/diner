
import asyncio
import copy
from itertools import chain
import os
from typing import Dict
from src.actions import create_tools
from src.agents.employeeAgent import LLM
from src.agents.models.Claude import Claude
from src.agents.models.Model import ResponseMessage
from src.common.event_manager import EventManager
from src.common.events import *
from src.common.events.game_events import  GameUpdateEvent
from src.common.pause_manager import PauseManager
from src.controllers.employee_controller import EmployeeAgentController
from src.game_engine.IPauseManager import IPauseManager
from src.game_engine.active_turn import ActiveTurn, EmployeeUpdate
from src.game_engine.loop import LoopResult, loop
from src.infrastructure.navigation.build_level import build_level
from src.state import game_state
from src.state.game_state.game_state import GameState
from src.state.game_state.game_turn import GameTurn
from src.state.game_state.immutable_types.employee_turn import EmployeeTurn
from src.state.game_state.new_game_state import new_game_state


class GameController:
    def __init__(self, event_manager: EventManager[GuiEvent, GameEvent]):
        self.employee_controller = EmployeeAgentController(LLM(Claude(create_tools())))
        self.event_manager = event_manager
        self.pause_manager = PauseManager()
        self.instructions = {"Alice": "You will seat customers as they come in.", "Bob": "After Alice seats customers, you will take their orders and bring the orders to the kitchen to be submitted. Once the orders are ready, bring them to their respective customers.", "Jim": "As Bob brings you orders, you must cook them. If there are no orders to cook, then wait."}

    @property
    def paused(self) -> bool:
        return self.pause_manager.is_paused()

    async def start_game_loop(self):
        init_state = self.new_game()
        current_state = LoopResult(init_state, EmployeeUpdate(0))
        queued_update = None
        while True:
            current_state = self.handle_events(current_state)

            if not self.paused:
                if queued_update is not None:
                    self.update_gui(queued_update)
                    queued_update = None
                current_state = await self.loop(current_state.gameState, current_state.nextTurn)
                queued_update = current_state.gameState
            await asyncio.sleep(0.1)

    def new_game(self):
        floor_plan = build_level("src/assets/levels/level1.txt")
        return new_game_state(self.instructions, floor_plan)

    async def loop(self, prev_state: GameState, turn: ActiveTurn) -> LoopResult:
        return await loop(turn, prev_state, self.employee_controller)



    def handle_events(self, current_state: LoopResult):
        e = self.event_manager.get_event()
        if e is None:
            return current_state

        match e:
            case ResetGame():
                if os.path.exists("responses.json"):
                    os.remove("responses.json")
                print("Reset history")
                return LoopResult(self.new_game(), EmployeeUpdate(0))

            case Pause():

                self.pause_manager.toggle()
                print(f"Paused: {self.paused}")
                return current_state

            case _:
                raise ValueError(f"Unhandled event type: {type(e)}")

    def update_gui(self, state: GameState):
        last_turn = state.last_game_turn()
        if last_turn is None:
            raise ValueError("No entity found for the last turn")
        employee_turn = last_turn.employees[-1] 
        turn_history = get_turns(state.get_game_turns())
        event = GameUpdateEvent(game_state.view_all_entities(state), 
                                turn_history,
                                last_turn.employees[-1].employee_name, 
                                state.tick, 
                                repr(employee_turn.action),
                                employee_turn.response,
                                employee_turn.action_result_message,
        )
        self.event_manager.put_event(event)


def get_turns(turns: List[GameTurn]) -> List[TurnSummary]:
    return [get_turn_info(i, turn) for i, turn in enumerate(chain.from_iterable(t.employees for t in turns))]

def get_turn_info(num: int, e: EmployeeTurn) -> TurnSummary:
    return TurnSummary(num, e.employee_name, repr(e.action), e.response, e.action_result_message)