from dataclasses import dataclass
from typing import TypedDict


class GuiTurnSummary(TypedDict):
    entity_name: str
    action: str
    agent_response: str | None
    action_result: str


@dataclass
class GuiState:
    paused: bool
    current_turn_num: int
    max_turn_num: int
    current_entity: str
    messages: list[GuiTurnSummary]

    