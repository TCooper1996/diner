from dataclasses import dataclass
from typing import List, Protocol, TypedDict


@dataclass
class GuiTurnSummary:
    action: str
    agent_response: str | None
    action_result: str


@dataclass
class GuiState:
    paused: bool
    current_turn_num: int
    max_turn_num: int
    current_entity: str
    messages: List[str]

    