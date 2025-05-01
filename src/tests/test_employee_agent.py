from dataclasses import dataclass
import sys
import os
import unittest
from typing import Dict, List, Tuple

import pytest

from src.actions.base import Movement
from src.agents.employeeAgent import LLM
from src.agents.models.ChatGPT import GPT
from src.agents.models.Claude import Claude
from src.common.position import Position
from src.game_engine.choose_employee_action import EmployeeAgentController

from src.actions import *
from src.core.types import TileType
from src.infrastructure.navigation.floor_plan import FloorPlan
from src.game_engine.select_employee_action import add_employee_turn
from src.state.game_state.immutable_types.employee_turn import EmployeeTurn
from src.core.entities.customer import Customer, CustomerStatus
from src.state.game_state.restaurant_state import add_customer, add_employee, initialize_entities
from src.state.game_state.restaurant_state.managers.location_manager import LocationManager
from src.state.game_state.restaurant_state.restaurant_state import RestaurantState

tileTypes = {
    "_": "empty",
    "k": "kitchen",
    "d": "dining",
    "e": "entrance",
}

@dataclass
class CustomerView:
    position: Position
    name: str
    status: CustomerStatus

class EmployeeView:
    def __init__(self, gameState: GameState, employee: str):
        self.state: GameState = gameState
        self.name: str = employee
    
    @property
    def position(self):
        return self.state.restaurant_state.location_manager._get_entity_position(self.name)

    def _last_turn(self):
        last_turn  = self.state.last_game_turn()
        if last_turn is None:
            raise ValueError("No game turn found. Make sure to run at least one turn before accessing employee actions.")
        return last_turn.get_employee_turn(self.name)

    def last_action(self):
        employee_turn = self._last_turn()
        if employee_turn is None:
            raise ValueError(f"No turn found for employee {self.name}. Make sure they have taken an action.")
        return employee_turn.action

    def next_action(self):
        employee_turn = self._last_turn()
        if employee_turn is None:
            raise ValueError(f"No turn found for employee {self.name}. Make sure they have taken an action.")
        return employee_turn.next_action



class TController:
    def __init__(self, r_state: RestaurantState):

        self.state: RestaurantState = r_state
        initialize_entities(self.state)
        self.c = EmployeeAgentController(LLM(Claude(create_tools())))
        self.gamestate = GameState(self.state)

    async def process(self, employee) -> EmployeeTurn:
        return await self.c.process(self.gamestate, employee)

    def add_employee(self, employee_id: str, instruction:str, location: TileType):
        add_employee(self.state, employee_id, instruction, location)

    def add_customer(self, id: str, pos):
        add_customer(self.state, id, pos)

    def get_customer(self, id: str) -> CustomerView:
        base_c =  self.state.grab_customer(id)
        position = self.state.location_manager._get_entity_position(id)
        return CustomerView(position=position, name=base_c.name, status=base_c.status)

    def get_employee(self, id: str) -> EmployeeView:
        return EmployeeView(self.gamestate, id)

    async def one_turn(self, employees: List[str]):
        for employee in employees:
            turn = await self.process(employee)
            add_employee_turn(self.gamestate, turn)
            failed = [d for d in turn.decisions if not d.was_valid]
            if failed:
                print(f"Failed to process action for employee {employee} after 3 attempts. Last decision: {failed[-1].get_response()}")
        self.gamestate.tick += 1  # Increment the game tick after processing all employees

@pytest.mark.asyncio
class TestEmployeeAgent:
    def setup_method(self):
        """Set up test environment before each test"""
        # Create a fresh game state for each test
        
    @pytest.mark.asyncio
    async def test_full_scenario(self):
        floor_plan = FloorPlan(["E _ D _ K"], tileTypes)
        self.cont = TController(RestaurantState(LocationManager(floor_plan, step_size=1)))
        employees = [ "Alice", "Bob", "Jim"]
        self.cont.add_employee("Alice", "You will seat customers as they come in. Do not take their orders. You can only use the SeatCustomer() and Wait() actions.", "entrance")
        self.cont.add_employee("Bob", "You are bob. If a customer is seated and hasn't had their order taken, you will take their orders and bring the orders to the kitchen to be submitted. Once the orders are ready, bring them to their respective customers. If you have no action to take, then wait. You should only ever use the Wait(), HandOrderToCustomer(), SubmitOrdersToKitchen(), DeliverOrder(), and TakeOrder() tools. If you attempt to seat a customer, you will be shot.", "entrance")
        self.cont.add_employee("Jim", """
                               As Bob brings you orders, you must cook them. 
                               If there are no orders to cook, then wait. 
                               Do not seat customers. 
                               Once an order is in the 'submitted' status, cook it.
                               Do not attempt to use the SubmitOrdersToKitchen() tool.
                               """, "entrance")

        self.cont.add_customer("C1", "entrance")

        alice = self.cont.get_employee("Alice")
        bob = self.cont.get_employee("Bob")
        jim = self.cont.get_employee("Jim")

        # Turn 1
        await self.cont.one_turn(employees)
        assert alice.last_action() == SeatAction( customer_id="C1")
        assert bob.last_action() == WaitAction()
        assert jim.last_action() == WaitAction()
        
        # Turn 2
        # Customer reaches seat, so Alice's action resets to Wait
        await self.cont.one_turn(employees)
        assert alice.last_action() == SeatAction(customer_id="C1")
        ## Bob should be moving toward customer
        assert bob.last_action() == TakeOrderAction(customer_id="C1")
        assert bob.position == Position(1, 0), "Bob should be at the dining area where C1 is seated"
        assert jim.last_action() == WaitAction()
        assert self.cont.get_customer("C1") == CustomerView(position=Position(2, 0), name="C1", status=CustomerStatus.SEATED)


        # Turn 3
        await self.cont.one_turn(employees)
        assert alice.last_action() == WaitAction(), "Alice should be waiting after seating the customer"
        assert bob.last_action() == TakeOrderAction(customer_id="C1"), "Bob should still be taking the order from C1"
        assert bob.position == Position(2, 0), "Bob should be at the dining area where C1 is seated"
        assert jim.last_action() == WaitAction()


        # Turn 4
        await self.cont.one_turn(employees)
        assert alice.last_action() == WaitAction(), "Alice should still be waiting after seating the customer"
        assert bob.last_action() == SubmitOrdersToKitchen(), "Bob should have taken the order and must now choose the next action"
        assert jim.last_action() == WaitAction(), "Jim should still be waiting as there are no orders to cook yet"


        # Turn 5
        await self.cont.one_turn(employees)
        assert alice.last_action() == WaitAction(), "Alice should still be waiting after seating the customer"
        assert bob.last_action() == SubmitOrdersToKitchen()
        assert bob.position == Position(4,0)
        # Order should have now been submitted
        order = self.cont.state.get_orders()[0].id
        assert jim.last_action() == CookAction(order_id=order), "Jim should be cooking the new order"

        # Turn 6
        await self.cont.one_turn(employees)
        assert alice.last_action() == WaitAction(), "Alice should still be waiting after seating the customer"
        assert bob.last_action() == PickUpOrder(order_id=order), "Bob should be waiting after submitting the order to the kitchen"
        assert bob.position == Position(4, 0)
        assert jim.last_action() == WaitAction()

        # Turn 7
        await self.cont.one_turn(employees)
        assert alice.last_action() == WaitAction(), "Alice should still be waiting after seating the customer"
        assert bob.last_action() == DeliverOrderToCustomer(order_id=order, customer_id="C1"), "Bob should be delivering the order to C1"
        assert bob.position == Position(3, 0), "Bob should be at the dining area where C1 is seated"
        assert jim.last_action() == WaitAction()

        # Turn 8
        await self.cont.one_turn(employees)
        assert alice.last_action() == WaitAction(), "Alice should still be waiting after seating the customer"
        assert bob.last_action() == DeliverOrderToCustomer(order_id=order, customer_id="C1"), "Bob should finish delivering the order"
        assert jim.last_action() == WaitAction(), "Jim should still be waiting as there are no new orders to cook"

    async def test_full_scenario_2(self):
        floor_plan_data = """
        E _ _ _
        D _ _ _
        D D _ K
        """
        floor_plan = FloorPlan(floor_plan_data.splitlines(), tileTypes)
        self.cont = TController(RestaurantState(LocationManager(floor_plan, step_size=100))) # Large step size

        employees = [ "Alice", "Bob", "Jim"]
        self.cont.add_employee("Alice", "You must seat customers as they come in. Do not take their orders.", "entrance")
        self.cont.add_employee("Bob", "You are bob. If a customer is seated and hasn't had their order taken, you will take their orders and bring the orders to the kitchen to be submitted. Once the orders are ready, bring them to their respective customers. If you have no action to take, then wait. You should only ever use the Wait(), HandOrderToCustomer(), SubmitOrdersToKitchen(), DeliverOrder(), and TakeOrder() tools.", "entrance")
        self.cont.add_employee("Jim", "As Bob brings you orders, you must cook them. If there are no orders to cook, then wait. Do not seat customers. Once an order is in the 'submitted' status, cook it.", "entrance")

        self.cont.add_customer("C1", "entrance")

        alice = self.cont.get_employee("Alice")
        bob = self.cont.get_employee("Bob")
        jim = self.cont.get_employee("Jim")


        for i in range(25):
            print(f"--- Turn {i+1} ---")
            await self.cont.one_turn(employees)
            if i == 5:
                self.cont.add_customer("C2", "entrance")  # Add another customer to test multiple seating
            if i == 10:
                self.cont.add_customer("C3", "entrance")  # Add another customer to test multiple seating
            eating = [c for c in self.cont.state.customers.values() if c.status == CustomerStatus.EATING]
            if len(eating) == 3:
                return
        
        assert False, "Customer C1 did not start eating within the expected time frame."


