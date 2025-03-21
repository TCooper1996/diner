import abc
from typing import Callable


class GameLogger(abc.ABC):
    @abc.abstractmethod
    def new_customer(self, customer_name: str, message: str):
        pass

    @abc.abstractmethod
    def employee_turn(self, employee_name: str, message: str):
        pass

    @abc.abstractmethod
    def customer_left(self, customer_name: str, good:bool, message: str):
        pass

    @abc.abstractmethod
    def turn_started(self):
        pass

    @abc.abstractmethod
    def game_over(self, message: str):
        pass

    @abc.abstractmethod
    def customer_status(self, customer_name: str, message: str):
        pass

    @abc.abstractmethod
    def log_message(self, message: str):
        print(message)