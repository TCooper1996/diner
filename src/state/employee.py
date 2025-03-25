
# Persistent state for an employee that remains between ticks
from dataclasses import dataclass
from typing import Any, List, TYPE_CHECKING, Tuple
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage


from src.agents.models.Model import ResponseMessage, StandardMessage, ToolInvocationMessage, ToolResultMessage
from src.game_engine.location import ENTRANCE
from src.state.types import AgentDecision, EmployeeTurn


class Employee(BaseModel):
    name: str
    instruction: str
    location: str = Field(default=ENTRANCE)
    action: Any = Field(default_factory=any)  # The action the employee is currently performing (typed as Any to avoid circular import)
    recentThoughts: List[BaseMessage] = Field(default_factory=list)  # Recent thoughts for the employee
    messages: List[StandardMessage] = Field(default_factory=list)  # List of messages the employee has received
    turns: List[EmployeeTurn] = Field(default_factory=list)  # List of turns the employee has taken
    
    def to_prompt(self) -> str:
        return f"""
Employee: {self.name}
    Location: {self.location}
"""
    def last_action(self) -> AgentDecision:
        return self.turns[-1].decisions[-1].action

    def new_turn(self, decision: AgentDecision) -> None:
        self.turns.append(EmployeeTurn(employee_name=self.name, decisions=[decision]))

    def add_to_current_turn(self, decision: AgentDecision) -> None:
        self.turns[-1].decisions.append(decision)

    def get_messages(self) -> List[StandardMessage]:
        messages: List[StandardMessage] = []
        for turn in self.turns:
            for d in turn.decisions:
                messages.append(d.response)
                messages.append(d.invocation)
                messages.append(d.result)
        return messages

    def add_message(self, message: StandardMessage) -> None:
        self.messages.append(message)

    def add_turn(self, turn: EmployeeTurn):
        self.turns.append(turn)

    def get_turns(self) -> List[EmployeeTurn]:
        return self.turns


    def add_thought(self, thought: BaseMessage) -> None:
        """Add a recent thought to the employee's memory"""
        self.recentThoughts.append(thought)
