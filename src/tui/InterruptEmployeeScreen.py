from textual.screen import Screen
from textual.widgets import Input, Button, Static
from textual.app import ComposeResult

class InterruptEmployeeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Type your message and press Enter:")
        yield Input(placeholder="Enter your message here...", id="message_input")
        yield Button("Submit", id="submit_button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit_button":
            message_input = self.query_one("#message_input", Input)
            self.app.handle_message(message_input.value)
            self.app.pop_screen()