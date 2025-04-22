from dataclasses import dataclass

from src.common.events.game_events import TurnSummary


@dataclass
class GuiState:
    paused: bool
    current_turn_num: int
    max_turn_num: int
    current_entity: str
    messages: list[TurnSummary]

    