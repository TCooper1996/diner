from textual.app import ComposeResult, Screen
from textual.widgets import Static
class Pause(Screen):
    BINDINGS = [("p", "pop_screen()", "Resume")]
    def compose(self) -> ComposeResult:
        yield Static("Game is paused. Press 'p' to resume.")
