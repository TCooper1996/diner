from dataclasses import dataclass
from typing import List

from src.state.game import GameState

@dataclass
class OrderView:
    id: int
    customerId: int


@dataclass
class CustomerView:
    id: int

@dataclass
class TurnView:
    response: str
    tool_invocation: str
    tool_result: str

@dataclass
class EmployeeView:
    name: str
    turns: List[TurnView]

    def get_orders_taken(self, gamestate: GameState) -> List[OrderView]:
        return [order for order in gamestate.orders.values() if order.customer_id == self.name]

    def get_orders_carried(self, gamestate: GameState) -> List[OrderView]:
        return [order for order in gamestate.orders_carried_by_employee]