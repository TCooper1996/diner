from typing import Literal, Union
from textual.screen import Screen
from textual.widgets import Markdown

from src.state.game import GameState
from src.state.order import OrderStatus

customer_states = ["arrived", "seated", "ordered", "order_submitted", "ordered_prepared", "order_delivered", "left"]
customer_state = Literal["arrived", "seated", "ordered", "order_submitted", "ordered_prepared", "order_delivered", "left"]
class CustomerTab:
    def __init__(self, markdown: Markdown):
        self.markdown = markdown

    def update(self, gamestate: GameState):
        customers = gamestate.customers.values()
        rows = []
        for c in customers:
            state = self.get_customer_state(c.id, gamestate)
            rows.append(self.customer_row(c.name, state))

        table = "  \n".join(rows)
        self.markdown.update(table)

    def customer_row(self, name, state: customer_state):
        i = customer_states.index(state)
        fields = [f"{s}✅" if i >= j else f"{s}❌" for j, s in enumerate(customer_states)]
        line = " | ".join(fields)
        row = f"**{name}** | {line}"
        return row
    
    def get_customer_state(self, customer: str, gamestate: GameState) -> customer_state:
        c = gamestate.grab_customer(customer)
        match c.status.value:
            case "waiting":
                return "arrived"
            case "seated":
                return "seated"
            case "ordered":
                o = gamestate.grab_order(customer_id=c.id)
                match o.status:
                    case OrderStatus.PENDING:
                        return "ordered"
                    case OrderStatus.SUBMITTED:
                        return "order_submitted"
                    case OrderStatus.READY:
                        return "ordered_prepared"
                    case OrderStatus.DELIVERED:
                        return "order_delivered"
                    case _:
                        raise ValueError(f"Unknown order status: {o.status}")
            case "eating":
                return "order_delivered"
            case "left":
                return "left"
            case _:
                raise ValueError(f"Unknown state: {c.status}")
    
    def state(self, state: str):
        match state:
            case "arrived":
                return "Arrived"
            case "seated":
                return "Seated"
            case "ordered":
                return "Ordered"
            case "ordered_prepared":
                return "Prepared"
            case "order_delivered":
                return "Delivered"
            case "left":
                return "Left"
            case _:
                raise ValueError(f"Unknown state: {state}")
