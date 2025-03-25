from typing import List
from textual.widgets import Markdown
from rich.text import Text

from src.agents.models.Model import *
from src.state.employee import EmployeeTurn
from src.state.types import AgentDecision

string_type = Literal["Name", "Response", "ToolCall", "ToolResult"]

class EmployeeTab:
    def __init__(self, markdown: Markdown):
        self.markdown = markdown


    def update(self, name: str,  messages: List[EmployeeTurn]) -> None:
        lines: List[str | Tuple[str,str]] = []
        lines.append((name, "bold"))
        for i, turn in enumerate(messages):
            lines.append((f"Turn {i} \n\n", "bold yellow"))
            for j, attempt in enumerate(turn.decisions):
                lines.append((f"\tAttempt {j} \n  ", "bold red"))
                lines.extend(format_attempt(attempt, name))
        content = Text.assemble(*lines)
        self.markdown.update(str(content))

def format_attempt(attempt: AgentDecision, name: str) -> List[str | Tuple[str,str]]:
    return [
    (f"Message: ", "bold green"),
    f"{attempt.response.content}  \n  ",
    ("\tInvoked: "),
    (f"{attempt.action}  \n  ", "blue"),
    ("\tResult: "),
    (f"{attempt.get_result()}", "blue"),
    ]