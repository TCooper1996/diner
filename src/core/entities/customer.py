from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from src.common.position import Position

def not_implemented_error():
    raise NotImplementedError("This method is not implemented in the current context. Please override it in the subclass or provide an implementation.")

customerNames = [
    "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi",
    "Ivan", "Judy", "Karl", "Leo", "Mallory", "Nina", "Oscar", "Peggy",
    "Quentin", "Rupert", "Sybil", "Trent", "Uma", "Victor", "Walter"]

customerLastnames = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller",
    "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White",
    "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"]

names = [f"{f} {l}" for f, l in zip(customerNames, customerLastnames)]
index = 0
def nextName():
    """Generate a random name for a customer"""
    global index
    name= names[index]
    index += 1
    return name

class CustomerStatus(Enum):
    WAITING = "waiting: Customer is waiting to be seated"
    BEING_SEATED = "being_seated: Customer is currently being seated" 
    SEATED = "seated: Customer is seated at a table and waiting to have their order taken"
    ORDERED = "ordered: Customer has placed an order and is waiting for their food"
    EATING = "eating"
    LEAVING = "leaving"  # Customer is leaving the restaurant
    DONE = "done"

@dataclass
class Customer:
    position: Position
    name: str = field(default_factory=nextName)  # Random name from the list
    waiting_time: int = field(default=0)
    patience: int = field(default=50)  # Will leave unhappy after this many ticks
    status: CustomerStatus = field(default=CustomerStatus.WAITING)  # waiting, seated, ordered, eating, done
    eating_time: int = field(default=0)  # Tracks how long they've been eating
    received_order: bool = field(default=False)

    @property # type: ignore
    def id(self) -> str:
        return self.name #sha256(self.name.encode('utf-8')).hexdigest()

    def to_prompt(self) -> str:
        return f"""
Customer: {self.name}
    Location: {not_implemented_error()}
    Status: {self.status.value}
"""
    
    def start_eating(self):
        """Customer starts eating their food"""
        self.status = "eating"
        
    def is_done(self) -> bool:
        """Check if customer is done and ready to leave"""
        return self.status == "eating" and self.eating_time >= 3
