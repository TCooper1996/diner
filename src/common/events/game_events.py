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
    action_name: str
    agent_response: str | None
    response_result: str
    


