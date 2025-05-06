from dataclasses import dataclass
from typing import Literal


class CustomerOccupyingSeat:
    customer_id: str
    seat_id: str

class CustomerOccupyingExit:
    customer_id: str
    exit_id: str

RelationshipType = CustomerOccupyingSeat

@dataclass
class Relationship:
    relationship_type: RelationshipType
    