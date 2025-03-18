
# Persistent state for an employee that remains between ticks
from typing import Any, List
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage

from src.agents.employee_tools import EmployeeAction, WaitTool
from src.game_engine.location import ENTRANCE


class Employee(BaseModel):
    name: str
    instruction: str
    location: str = Field(default=ENTRANCE)
    messages: List[Any] = Field(default_factory=list)  # Conversation history that persists between ticks
    action: EmployeeAction = Field(default_factory= lambda: WaitTool())  # The action the employee is currently performing
    recentThoughts: List[BaseMessage] = Field(default_factory=list)  # Recent thoughts for the employee
    
    
    def add_message(self, message: Any) -> None:
        """Add a message to the employee's history"""
        self.messages.append(message)

    def add_thought(self, thought: BaseMessage) -> None:
        """Add a recent thought to the employee's memory"""
        self.recentThoughts.append(thought)

    def last_thought(self) -> str:
        """Get the most recent thought"""
        thought =  self.recentThoughts[-1]
        if self.recentThoughts:
            if isinstance(thought.content, str):
                return thought.content
            elif isinstance(thought.content, list):
                if isinstance(thought.content[0], dict):
                    return thought.content[0]["text"]
                else:
                    return thought.content[0]
            else:
                return "Unknown thought type"
        else:
            return "No thoughts"