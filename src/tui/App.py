import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, RichLog
from src.game_engine.game import Game
from src.tui.InterruptEmployeeScreen import InterruptEmployeeScreen
from src.state.game import GameState
from src.tui.PauseScreen import Pause
from src.tui.gameLoggerImpl import GameLoggerImpl

class Window(App):
    def __init__(self, gameState:Game, driver_class = None, css_path = None, watch_css = False, ansi_color = False):
        super().__init__(driver_class, css_path, watch_css, ansi_color)
        self.gameState = gameState
        self.pause_event = asyncio.Event()
        self.pause_event.set()

    BINDINGS = [
        ("e", "interrupt_employee", "Interrupt Employee"),
        ("p", "pause", "Pause"),
        ]

    def compose(self) -> ComposeResult:
        yield Header()
        self.mylog =  RichLog()
        yield self.mylog
        yield Footer()

    def action_pause(self) -> None:
        if self.pause_event.is_set():
            self.pause_event.clear()
            self.pop_screen()
        else:
            self.pause_event.set()
            self.push_screen(Pause())



    def action_interrupt_employee(self) -> None:
        """Interrupt the employee's current action"""
        self.push_screen(InterruptEmployeeScreen())
        # self.console.print("Interrupting employee...")
        # self.agent_controller.interrupt()
        # self.console.print("Employee interrupted.")
        # self.pop_screen()

    def handle_message(self, message: str) -> None:
        """Handle the message from the interrupt screen"""
        self.console.print(f"Message from interrupt screen: {message}")
        self.gameState.message = message

    def on_ready(self):
        """Start the game"""
        logger = GameLoggerImpl(self.mylog)
        self.mylog.write("Starting game...")
        self.run_worker(self.gameState.start(logger, self.pause_event))