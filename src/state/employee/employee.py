
# Persistent state for an employee that remains between ticks
from dataclasses import dataclass, field
from typing import Any, List, TYPE_CHECKING, Tuple
from langchain_core.messages import BaseMessage


from src.agents.models.Model import ResponseMessage, StandardMessage, ToolInvocationMessage, ToolResultMessage
from src.game_engine.location import ENTRANCE
from src.protocols import IAction
from src.state.employee.EmployeeTurn import EmployeeTurn
from src.state.employee.EmployeeDecision import EmployeeDecision

@dataclass
class Employee:
    name: str
    instruction: str
    location: str = field(default=ENTRANCE)
    turns: List[EmployeeTurn] = field(default_factory=list)  # List of turns the employee has taken
    
    def to_prompt(self) -> str:
        return f"""
Employee: {self.name}
    Location: {self.location}
"""
    def last_action(self) -> IAction:
        return self.turns[-1].decisions[-1].get_action()

    def new_turn(self, decision: EmployeeDecision) -> None:
        self.turns.append(EmployeeTurn(employee_name=self.name, decisions=[decision]))

    def add_to_current_turn(self, decision: EmployeeDecision) -> None:
        self.turns[-1].decisions.append(decision)

    def get_messages(self) -> List[StandardMessage]:
        messages: List[StandardMessage] = []
        for turn in self.turns:
            for d in turn.decisions:
                messages.append(d.response)
                messages.append(d.invocation)
                messages.append(d.result)
        return messages


    def add_turn(self, turn: EmployeeTurn):
        self.turns.append(turn)

    def get_turns(self) -> List[EmployeeTurn]:
        return self.turns


