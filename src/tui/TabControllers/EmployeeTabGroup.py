from typing import Dict
from src.state.game import GameState
from src.tui.TabControllers.EmployeeTab import EmployeeTab


class EmployeeTabGroup:
    def __init__(self, employee_tabs: Dict[str, EmployeeTab]):
        self.employee_tabs = employee_tabs

    def update(self, gamestate: GameState):
        for employee, tab in self.employee_tabs.items():
            messages = gamestate.employees[employee].get_turns()
            tab.update(employee, messages)
