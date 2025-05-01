from typing import TypeVar


T = TypeVar('T')
class TurnManager[T]:
    def __init__(self, initial_turn: T):
        self.initial_turn = initial_turn
        self.history: list[T] = [initial_turn]
        self.index = 0

    

    def clear(self):
        self.history = [self.initial_turn]
        self.index = 0

    def increment(self):
        if self.index + 1 < len(self.history):
            self.index += 1

    def decrement(self):
        if self.index > 0:
            self.index -= 1

    def append(self, item: T):
        increment = self.is_latest_turn_focused()
        self.history.append(item)
        # Increment the focus only if we were previously focused on the latest turn
        if increment:
            self.increment()


    def get_current(self) -> T:
        if not self.history:
            raise IndexError("No turns available")
        return self.history[self.index]
    
    def get_previous(self) -> T | None:
        if self.index == 0:
            return None
        return self.history[self.index - 1]

    def is_latest_turn_focused(self) -> bool:
        return self.index == len(self.history) - 1

    @property
    def num_turns(self) -> int:
        return len(self.history)

    @property
    def ordinal_turn(self) -> int:
        return self.index + 1