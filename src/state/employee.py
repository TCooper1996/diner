
# Persistent state for an employee that remains between ticks
from typing import Any, List, TYPE_CHECKING
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage


from src.game_engine.location import ENTRANCE


class Employee(BaseModel):
    name: str
    instruction: str
    location: str = Field(default=ENTRANCE)
    messages: List[Any] = Field(default_factory=list)  # Conversation history that persists between ticks
    action: Any = Field(default_factory=any)  # The action the employee is currently performing (typed as Any to avoid circular import)
    recentThoughts: List[BaseMessage] = Field(default_factory=list)  # Recent thoughts for the employee
    
    def to_prompt(self) -> str:
        return f"""
Employee: {self.name}
    Location: {self.location}
"""
    
    def add_message(self, message: Any) -> None:
        """Add a message to the employee's history"""
        self.messages.append(message)

    def add_thought(self, thought: BaseMessage) -> None:
        """Add a recent thought to the employee's memory"""
        self.recentThoughts.append(thought)

    def last_thought(self) -> str:
        """Get the most recent thought"""
        if len(self.messages) > 0:
            return self.messages[-1].content
        else:
            return "No thoughts"

    def last_decision_text(self) -> str:
        """Get the most recent decision """
        invocation = self.messages[-2]
        return invocation.content[0]["text"]

    def last_decision_result(self) -> str:
        """Get the most recent decision result"""
        invocation = self.messages[-1]
        return invocation.content