from dataclasses import dataclass
from typing import List

from src.common.position import Position
from src.core.entities.info import EntityInfo
from src.core.entities.info.employee_info import EmployeeTurnInfo

@dataclass
class TurnSummary:
    turn_number: int
    entity_name: str
    action: str
    response: str
    result: str

@dataclass
class GameUpdateEvent:
    entities: List[EntityInfo]  # Mapping of entity ID to their new position
    turn_history: List[TurnSummary]
    name_of_turn_entity: str # Entity that just went
    turn_number: int

    @classmethod
    def default(cls) -> 'GameUpdateEvent':
        return cls(
            entities=[],
            turn_history=[],
            name_of_turn_entity="First turn",
            turn_number=0,
        )

    def get_action_name(self) -> str:
        return self.turn_history[-1].action 
    def get_agent_response(self) -> str:
        return self.turn_history[-1].response
    def get_response_result(self) -> str:
        return self.turn_history[-1].result
    
@dataclass
class NewGameEvent:
    update: GameUpdateEvent
