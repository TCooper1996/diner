import asyncio
import copy
import datetime
from email import message
from itertools import chain
import os
import functools
from types import CoroutineType
from typing import Any, Callable, Coroutine, Dict, Tuple, TypedDict
from src.actions import *
from src.agents.employeeAgent import LLM, LLMResult
from src.agents.models.Claude import Claude
from src.agents.models.Model import ResponseMessage, StandardMessage, ToolInvocationMessage, ToolResultMessage
from src.common.event_manager import EventManager
from src.common.events import *
from src.common.events.game_events import  GameUpdateEvent
from src.common.pause_manager import PauseManager
from src.game_engine.IPauseManager import IPauseManager
from src.application.game_loop import CustomerTurn
from src.game_engine.verify_employee_action import verify_employee_action
from src.infrastructure.navigation.build_level import build_level
from langchain_core.messages import HumanMessage

class GameControllerDependencies(TypedDict):
    invoke_llm: Callable[[str, str, List[StandardMessage]], Coroutine[Any, Any, LLMResult]]

InvokeLLM = Callable[[str, str, List[StandardMessage]], Coroutine[Any, Any, LLMResult]]
class GameController:
    def __init__(self, event_manager: EventManager[GuiEvent, GameEvent]):
        self.event_manager = event_manager
        self.pause_manager = PauseManager()
        cache = {}
        async def invoke_llm(employee_name: str, state_message: str, extra_messages: List[StandardMessage]) -> LLMResult:
            if employee_name in cache:
                # If we have a cached LLM for this employee, use it
                llm = cache[employee_name]
            else:
                llm = LLM(Claude(allowed_actions[employee_name]))
                cache[employee_name] = llm
            return await llm.invoke_cached(self.instructions[employee_name], HumanMessage(state_message), extra_messages)

        self.invoke_llm: InvokeLLM = invoke_llm


    @property
    def paused(self) -> bool:
        return self.pause_manager.is_paused()

    async def start_game_loop(self):
        # Immediately notify the GUI of the initial game state
        reset_event = asyncio.Event()
        reset_event.clear()
        asyncio.create_task(self.handle_events(reset_event))
        create_game_loop = lambda: asyncio.create_task(game_control_loop(self.pause_manager, self.instructions, self.invoke_llm, self.event_manager))
        while True:
            game_loop_task = create_game_loop()
            await reset_event.wait()
            game_loop_task.cancel()
            reset_event.clear()
            await asyncio.sleep(0.1)




    async def handle_events(self, cancel_event: asyncio.Event):
        while True:
            await asyncio.sleep(0.1)  # Polling interval for events
            e = self.event_manager.get_event()

            match e:
                case ResetGame():
                    if os.path.exists("responses.json"):
                        os.remove("responses.json")
                    print("Reset history")
                    cancel_event.set()

                case Pause():
                    self.pause_manager.toggle()
                    print(f"Paused: {self.paused}")

                case None:
                    pass

                case _:
                    raise ValueError(f"Unhandled event type: {type(e)}")

def update_gui(state: GameLoopState, event_manager: EventManager):
    last_turn = state.turns[-1] if state.turns else None

    match last_turn:
        case None:
            event_manager.put_event(NewGameEvent(GameUpdateEvent(view_all_entities(state), [], "No entity",
                                    state.tick
                                                                )))
        case EmployeeTurn(name, attempts):
            turn_history = get_turns(state.turns)
            event_manager.put_event(GameUpdateEvent(view_all_entities(state), 
                                    turn_history,
                                    name,
                                    state.tick, 
            ))
        case CustomerTurn():
            turn_history = get_turns(state.turns)
            event_manager.put_event(GameUpdateEvent(view_all_entities(state), 
                                    turn_history,
                                    "custo",
                                    state.tick, 
            ))


def get_turns(turns: List[GameTurn]) -> List[TurnSummary]:
    return [get_turn_info(i, turn) for i, turn in enumerate(t for t in turns)]

def get_turn_info(num: int, e: GameTurn) -> TurnSummary:
    match e:
        case EmployeeTurn(employee_name, attempts, action_result_message):
            return TurnSummary(num, employee_name, repr(e.get_action()), e.get_response() or "no response", action_result_message)
        case CustomerTurn():
            return TurnSummary(num, "customer name", "customer action", "customer response", "customer action result message")
        case _:
            raise ValueError(f"Unknown turn type: {type(e)}")


# Each invocation is one new game
async def game_control_loop(pause_event: PauseManager, instructions: Dict[str,str], invoke_llm: InvokeLLM, event_manager: EventManager):
    try:
        init_state = new_game(instructions)
        current_state = init_state
        update_gui(init_state, event_manager)
        while True:
            if not pause_event.is_paused():
                GameTurnUsecase()
                current_state = await loop(current_state.nextTurn, current_state.gameState, invoke_llm)
                if not pause_event.is_paused():
                    update_gui(current_state.gameState, event_manager)
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        print("Game loop cancelled.")



def new_game(instructions: Dict[str,str]):
    floor_plan = build_level("src/assets/levels/level1.txt")
    return new_game_state(instructions, floor_plan)