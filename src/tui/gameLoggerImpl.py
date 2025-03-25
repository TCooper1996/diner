from src.game_engine.gameLogger import GameLogger
from textual.widgets import Footer, Header, RichLog
from rich.text import Text

free_colors = ["blue", "green",  "yellow"]
employee_color_map = {}

def employee_color(employee_name: str) -> str:
    if employee_name not in employee_color_map:
        color = free_colors.pop()
        employee_color_map[employee_name] = color
    return employee_color_map[employee_name]

class GameLoggerImpl(GameLogger):
    def __init__(self, log: RichLog):
        self.log = log
    
    def new_customer(self, customer_name: str, message: str):
        color = "yellow"
        self.log.write(Text.assemble((f"New customer {customer_name} arrived: {message}", color)))

    def employee_turn(self, employee_name: str, message: str):
        color = employee_color(employee_name)
        self.log.write(Text.assemble((f"{employee_name}", color), (f" {message}")))

    def customer_left(self, customer_name: str, good: bool, message: str):
        self.log.write(f"Customer {customer_name} left {'happy' if good else 'unhappy'}: {message}")

    def turn_started(self):
        self.log.write(
            Text.assemble((("="*5)+"Turn started"+("="*5), "bold blue")))

    def game_over(self, message: str):
        self.log.write(Text.assemble((f"Game over: {message}", "bold red")))

    def customer_status(self, customer_name: str, message: str):
        self.log.write(Text.assemble((f"Customer {customer_name}: {message}", "bold yellow")))

    def log_message(self, message: str):
        self.log.write(message)

    