import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, RichLog, TabbedContent, TabPane, Markdown, Label
from src.game_engine.game import Game
from src.tui.CustomerTab import CustomerTab
from src.tui.TabControllers.EmployeeTab import EmployeeTab
from src.tui.InterruptEmployeeScreen import InterruptEmployeeScreen
from src.state.game import GameState
from src.tui.PauseScreen import Pause
from src.tui.TabControllers.EmployeeTabGroup import EmployeeTabGroup
from src.tui.gameController import GameController
from src.tui.gameLoggerImpl import GameLoggerImpl
from rich.text import Text
from src.agents.models.Model import *
from src.tui.gameInfoTab import GameInfoTab

class Window(App):
    def __init__(self, gameState:Game, driver_class = None, css_path = None, watch_css = False, ansi_color = False):
        super().__init__(driver_class, css_path, watch_css, ansi_color)
        self.gameState = gameState
        self.pause_event = asyncio.Event()
        self.pause_event.set()
        self.customer_screen: CustomerTab | None = None

    BINDINGS = [
        ("l", "show_tab('log')", "Show Log"),
        ("c", "show_tab('customers')", "Show Customers"),
        ("e", "interrupt_employee", "Interrupt Employee"),
        ("p", "pause", "Pause"),
        ]

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(initial="log"):
            with TabPane("log", id="log"):
                yield RichLog()
            with TabPane("customers", id="customers"):
                yield Markdown(id="customer_markdown")
            with TabPane("employees", id="employees"):
                with TabbedContent():
                    for name in self.gameState.employee_names:
                        with TabPane(name, id=f"--content-tab-{name}", classes="employee_tab"):
                            yield Markdown(f"Employee {name}", id=f"employee_{name}")
            with TabPane("info", id="info"):
                yield Markdown(id="info_markdown")
        yield Label("running", name="pause_label", id="pause_label")
        yield Footer()

    def action_pause(self) -> None:
        if self.pause_event.is_set():
            self.pause_event.clear()
            self.query_one("#pause_label", Label).update("paused")
        else:
            self.pause_event.set()
            self.query_one("#pause_label", Label).update("running")

    def action_show_tab(self, tab: str) -> None:
        self.query_one(TabbedContent).active = tab


    def action_interrupt_employee(self) -> None:
        """Interrupt the employee's current action"""
        self.push_screen(InterruptEmployeeScreen())

    def handle_message(self, message: str) -> None:
        """Handle the message from the interrupt screen"""
        self.console.print(f"Message from interrupt screen: {message}")
        self.gameState.message = message

    async def on_ready(self):
        """Start the game"""
        asyncio.get_running_loop().set_debug(True)
        self.mylog = self.query_one(RichLog)
        self.customer_screen = CustomerTab(self.query_one("#customer_markdown", Markdown))
        self.info_tab = GameInfoTab(self.query_one("#info_markdown", Markdown))
        employeeTabs = [n.children[0] for n in self.query(""".employee_tab""").nodes]
        self.employee_tabs = {name: EmployeeTab(employeeTabs[i]) for i, name in enumerate(self.gameState.employee_names)}
        self.employee_tab_group = EmployeeTabGroup(self.employee_tabs)
        controller = GameController(employee_tab_group=self.employee_tab_group, gameInfoTab=self.info_tab, customerTab=self.customer_screen, logTab=self.mylog)
        self.run_worker(controller.start(self.gameState, self.pause_event))
