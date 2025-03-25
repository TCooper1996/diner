import uuid
from typing import List, Optional
from random import sample
from hashlib import sha256

from pydantic import BaseModel, Field, computed_field

from src.game_engine.location import *
from src.state.order import OrderItem

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
    WAITING = "waiting"
    SEATED = "seated"
    ORDERED = "ordered"
    EATING = "eating"
    DONE = "done"

class Customer(BaseModel):
    name: str = Field(default_factory=nextName)  # Random name from the list
    location: Location = Field(default=ENTRANCE)
    waiting_time: int = Field(default=0)
    patience: int = Field(default=15)  # Will leave unhappy after this many ticks
    status: CustomerStatus = Field(default=CustomerStatus.WAITING)  # waiting, seated, ordered, eating, done
    order: List[OrderItem] = Field(default=["burger"])  
    eating_time: int = Field(default=0)  # Tracks how long they've been eating

    @computed_field
    @property # type: ignore
    def id(self) -> str:
        return sha256(self.name.encode('utf-8')).hexdigest()

    def to_prompt(self) -> str:
        return f"""
Customer: {self.name}
    Location: {self.location}
    Status: {self.status.value}
"""
    
    def take_order(self) -> List[OrderItem]:
        """ Returns the customers desired order"""
        return self.order
    
    def start_eating(self):
        """Customer starts eating their food"""
        self.status = "eating"
        
    def is_done(self) -> bool:
        """Check if customer is done and ready to leave"""
        return self.status == "eating" and self.eating_time >= 3