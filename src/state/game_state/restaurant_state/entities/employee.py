# Persistent state for an employee that remains between ticks


from src.protocols import IAction

class Employee:
    def __init__(self, name: str, instruction: str, current_action: IAction | None = None):
        self.name = name
        self.instruction = instruction
        self.current_action = current_action
