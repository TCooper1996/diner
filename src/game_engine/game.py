import asyncio
import copy
from functools import reduce
import time
from typing import Dict, List, Tuple
from pydantic import BaseModel
from rich.console import Console

from src.actions import EmployeeAction, create_tools
from src.actions.base import ActionResult
from src.actions.wait import WaitAction
from src.agents.RefinementAgent import RefinementAgent
from src.agents.employeeAgent import LLM
from src.agents.models.Claude import Claude
from src.controllers.employee_controller import EmployeeAgentController
from src.game_engine.AgentTalker import AgentTalker
from src.game_engine.gameLogger import GameLogger
from src.state.employee.employee import Employee
from rich.text import Text
from src.game_engine.location import Location
from src.state.customer import Customer
from src.state.game import GameState
from src.state.employee.EmployeeTurn import EmployeeTurn
from src.state.restaurant_state import RestaurantState
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
        self.agent_controller = EmployeeAgentController()  # Create a single agent controller
        self.customer_timer = 0
        self.max_wait_time = 20  # game ticks before customers leave unhappy
        self.substate = EmployeeUpdate(index=0)
        

    async def start(self) -> GameState:
        instructions = {n:i for n, i in zip(self.employee_names, self.instructions)}

        employees = {n: Employee(location="entrance", current_action=WaitAction(), name=n, instruction=i) for n, i in instructions.items()}
        customer = Customer()
        return GameState(restaurant_state=RestaurantState(employees=employees, customers={customer.id: customer}), employee_turns=[])


    async def loop(self, gamestate: GameState) -> GameState:

        match (self.substate):
            case EmployeeUpdate(index=index):
                employees = list(gamestate.restaurant_state.employees.keys())
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
        gamestate = copy.deepcopy(_gamestate)
        # Check win/loss conditions
        if gamestate.tick % 5 == 0 and len(gamestate.restaurant_state.customers) < 3:  # Add new customer every 5 ticks
            c = Customer()
            gamestate.restaurant_state.add_customer(c)
            
        # Update customer wait times and check for unhappy customers
        customers_leaving = gamestate.restaurant_state.update_customers()
        for customer_id, happy in customers_leaving:
            if not happy:
                gamestate.restaurant_state.unhappy_customers += 1
            c = gamestate.restaurant_state.grab_customer(customer_id)
        return gamestate

    async def employee_turn(self, _gamestate: GameState, name: str) -> GameState:
        gamestate = copy.deepcopy(_gamestate)
        agentTalker = AgentTalker(llm=LLM(Claude(create_tools())), messages=gamestate.employee_messages(name))
        turn = await self.agent_controller.process(agentTalker, gamestate.restaurant_state, name)
        gamestate.restaurant_state = turn.new_state
        gamestate.employee_turns.append(turn)
        gamestate.restaurant_state.employees[name].current_action = turn.next_action
        return gamestate


    
