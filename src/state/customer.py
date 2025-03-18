import uuid
from typing import List, Optional
from random import sample

from pydantic import BaseModel, Field

from src.game_engine.location import *
from src.state.order import OrderItem

customerNames = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi",
    "Ivan", "Judy", "Karl", "Leo", "Mallory", "Nina", "Oscar", "Peggy",
    "Quentin", "Rupert", "Sybil", "Trent", "Uma", "Victor", "Walter"]

customerLastnames = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller",
    "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White",
    "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"]

def randomName():
    """Generate a random name for a customer"""
    first_name = sample(customerNames, 1)[0]
    last_name = sample(customerLastnames, 1)[0]
    return f"{first_name} {last_name}"

class Customer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])  # Short ID for the customer
    name: str = Field(default_factory=randomName)  # Random name from the list
    location: Location = Field(default=ENTRANCE)
    waiting_time: int = Field(default=0)
    patience: int = Field(default=15)  # Will leave unhappy after this many ticks
    status: str = Field(default="waiting")  # waiting, seated, ordered, eating, done
    order: List[OrderItem] = Field(default=["burger"])  
    eating_time: int = Field(default=0)  # Tracks how long they've been eating
    
    def take_order(self) -> List[OrderItem]:
        """ Returns the customers desired order"""
        return self.order
    
    def start_eating(self):
        """Customer starts eating their food"""
        self.status = "eating"
        
    def is_done(self) -> bool:
        """Check if customer is done and ready to leave"""
        return self.status == "eating" and self.eating_time >= 3