import asyncio
from functools import reduce
import time
from typing import Dict, List, Tuple
from pydantic import BaseModel
from rich.console import Console

from src.actions import EmployeeAction, create_tools
from src.actions.base import ActionResult
from src.agents.RefinementAgent import RefinementAgent
from src.agents.models.Claude import Claude
from src.game_engine.gameLogger import GameLogger
from src.state.employee import Employee
from src.agents.employeeAgent import EmployeeAgentController
from rich.text import Text
from src.game_engine.location import Location
from src.state.customer import Customer
from src.state.game import GameState
from src.state.types import EmployeeTurn
from src.utils.async_reduce import async_reduce


class EmployeeUpdate(BaseModel):
    index: int

class CustomerUpdate(BaseModel):
    pass

Substate = EmployeeUpdate | CustomerUpdate
class Game:
    def __init__(self):
        self.state = GameState()
        self.employee_names = ["Alice", "Bob", "Jim"]
        self.instructions = ["Seat the customers when they arrive. If there are no customers waiting, wait at the entrance.",
            "take orders from the customers after they are seated and bring them to the kitchen",
            "cook the food and deliver it to the customers"]
        self.agent_controller = EmployeeAgentController(Claude(create_tools()))  # Create a single agent controller
        self.customer_timer = 0
        self.max_wait_time = 20  # game ticks before customers leave unhappy
        self.substate = EmployeeUpdate(index=0)
        

    async def start(self) -> GameState:
        instructions = {n:i for n, i in zip(self.employee_names, self.instructions)}

        employees = {n: Employee(name=n, instruction=i) for n, i in instructions.items()}
        customer = Customer()
        return GameState(employees=employees, customers={customer.id: customer})


    async def loop(self, gamestate: GameState) -> GameState:

        match (self.substate):
            case EmployeeUpdate(index=index):
                employees = list(gamestate.employees.keys())
                employee = employees[index % len(employees)]

                if index == len(employees) - 1:
                    self.substate = CustomerUpdate()
                else:
                    self.substate = EmployeeUpdate(index=index + 1)
                return await self.employee_turn(gamestate, employee)
            case CustomerUpdate():
                self.substate = EmployeeUpdate(index=0)
                gamestate.tick += 1
                return self.customer_update(gamestate)
            case _:
                raise Exception("Invalid substate")


    def customer_update(self, _gamestate: GameState) -> GameState:
        gamestate = _gamestate.model_copy(deep=True)
        # Check win/loss conditions
        if gamestate.tick % 5 == 0 and len(gamestate.customers) < 3:  # Add new customer every 5 ticks
            c = Customer()
            gamestate.add_customer(c)
            
        # Update customer wait times and check for unhappy customers
        customers_leaving = gamestate.update_customers()
        for customer_id, happy in customers_leaving:
            if not happy:
                gamestate.unhappy_customers += 1
            c = gamestate.grab_customer(customer_id)
        return gamestate

    async def employee_turn(self, _gamestate: GameState, name: str) -> GameState:
        gamestate = _gamestate.model_copy(deep=True)
        return await self.agent_controller.process(gamestate, name)

    
