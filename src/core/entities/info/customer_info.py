
from src.common.position import Position
from src.core.entities import CustomerStatus


class CustomerInfo:
    def __init__(self, name: str, status: CustomerStatus, eating_time: int, position: Position):
        self.position = position
        self.name = name
        self.status = status 
        self.eating_time = eating_time