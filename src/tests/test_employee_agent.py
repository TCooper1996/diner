import sys
import os
import unittest
from typing import Dict

import pytest

from src.agents.RefinementAgent import RefinementAgent
from src.agents.models.Claude import Claude

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.actions import *
from src.state.employee.employee import Employee
from src.state.game import GameState
from src.state.order import Order, OrderStatus
from src.state.customer import Customer
from src.game_engine.location import  DINING, ENTRANCE, KITCHEN
from src.agents.employeeAgent import EmployeeAgentController

agent_controller = EmployeeAgentController(Claude(create_tools()))

@pytest.mark.asyncio
class TestEmployeeAgent:
    def setup_method(self):
        """Set up test environment before each test"""
        # Create a fresh game state for each test
        self.game_state = GameState()
        
    @pytest.mark.asyncio
    async def test_seating_host_behavior(self):
        """Test that an employee instructed to seat customers does so when there are waiting customers"""
        # Create an employee with instructions to seat customers
        host = Employee(name="Jim", instruction="Your job is to seat customers when they arrive")
        host.location = "entrance"  # Explicitly set location to entrance
        
        # Add the employee to the game state
        self.game_state.employees[host.name] = host
        
        # Add a waiting customer
        customer = Customer()
        self.game_state.add_customer(customer)
        
        # Process the host's turn
        updated_state = await agent_controller.process(self.game_state, host.name)
        
        # Check that the host tried to seat the customer
        assert SeatAction(customer_id=customer.id) == updated_state.grab_employee(host.name).last_action()
        
        # Verify customer was moved to dining area
        assert updated_state.customers[customer.id].location == DINING
        assert updated_state.customers[customer.id].status.value == "seated"
        
    async def test_seating_host_observation(self):
        """Test that a host waits when there are no customers to seat"""
        # Create an employee with instructions to seat customers
        host = Employee(name="Jim", instruction="Your job is to seat customers when they arrive")
        host.location = "entrance"  # Explicitly set location to entrance
        
        # Add the employee to the game state
        self.game_state.employees[host.name] = host
        
        # No customers added
        
        # Process the host's turn
        updated_state = await agent_controller.process(self.game_state, host.name)
        action = updated_state.employees[host.name].last_action()
        
        # Check that the host observed there are no customers
        assert action == WaitAction()
        
    async def test_waiter_takes_order(self):
        """Test that a waiter takes orders from seated customers"""
        # Create a waiter with instructions to take orders
        waiter = Employee(name="Alice", instruction="Your job is to take orders from seated customers")
        waiter.location = "dining"  # Set location to dining area
        
        # Add the waiter to the game state
        self.game_state.employees[waiter.name] = waiter
        
        # Add a seated customer
        customer = Customer()
        customer.location = DINING
        customer.status = CustomerStatus.SEATED
        self.game_state.add_customer(customer)
        
        # Process the waiter's turn
        updated_state = await agent_controller.process(self.game_state, waiter.name)
        action = updated_state.employees[waiter.name].last_action()
        
        # Check that the waiter took the customer's order
        assert action == TakeOrderAction(customer_id=customer.id)
        
        # Verify customer status was updated
        assert updated_state.customers[customer.id].status == CustomerStatus.ORDERED
        
        # Verify an order was created
        assert len(updated_state.orders) > 0
        
    async def test_waiter_moves_to_dining(self):
        """Test that a waiter moves to the dining area when not there"""
        # Create a waiter with instructions to take orders
        waiter = Employee(name="Alice", instruction="Your job is to take orders from seated customers")
        waiter.location = "entrance"  # Start at entrance
        
        # Add the waiter to the game state
        self.game_state.employees[waiter.name] = waiter
        
        # Add a seated customer
        customer = Customer()
        customer.location = DINING
        customer.status = CustomerStatus.SEATED
        self.game_state.add_customer(customer)
        
        # Process the waiter's turn
        updated_state = await agent_controller.process(self.game_state, waiter.name)
        action = updated_state.employees[waiter.name].last_action()
        
        # Check that the waiter moved to the dining area
        assert action == MoveToNewRoom(destination=DINING)
        assert updated_state.employees[waiter.name].location == DINING
        
        
    async def test_cook_prepares_food(self):
        """Test that a cook prepares food for pending orders"""
        # Create a cook with instructions to prepare food
        cook = Employee(name="Bob", instruction="Your job is to cook food. Cook any orders in the kitchen that are in the SUBMITTED state. If there are no orders, wait.")
        cook.location = "kitchen"  # Set location to kitchen
        
        # Add the cook to the game state
        self.game_state.employees[cook.name] = cook
        
        # Add a customer with an order
        customer = Customer()
        customer.status = CustomerStatus.ORDERED
        self.game_state.add_customer(customer)
        
        # Create an order for the customer
        order = Order(customer_id=customer.id, items=["burger", "fries"], status=OrderStatus.SUBMITTED)
        self.game_state.orders[order.id] = order
        self.game_state.assign_order_to_employee(order.id, cook.name)
        
        # Process the cook's turn
        updated_state = await agent_controller.process(self.game_state, cook.name)
        action = updated_state.employees[cook.name].last_action()
        
        # Check that the cook prepared the food - actual order_id will be generated dynamically
        assert action == CookAction(order_id=order.id)
        
        # Verify order status was updated
        assert updated_state.orders[order.id].status == OrderStatus.READY
        
    async def test_complex_scenario(self):
        """Test a complex scenario with multiple employees and customers"""
        # Create employees
        host = Employee(name="Jim", instruction="Your job is to seat customers when they arrive")
        host.location = "entrance"
        
        waiter = Employee(name="Alice", instruction="Your job is to take orders from seated customers, and then notify the kitchen of the order.")
        waiter.location = "dining"
        
        cook = Employee(name="Bob", instruction="Your job is to cook food and deliver it to customers")
        cook.location = "kitchen"
        
        # Add employees to game state
        self.game_state.employees = {
            host.name: host,
            waiter.name: waiter,
            cook.name: cook
        }
        
        # Add a waiting customer
        customer1 = Customer()
        self.game_state.add_customer(customer1)
        
        # First turn: host should seat the customer
        state1 = await agent_controller.process(self.game_state, host.name)
        result1 = state1.employees[host.name].last_action()
        assert SeatAction(customer_id=customer1.id) == result1
        
        # Second turn: waiter should take the customer's order
        state2 = await agent_controller.process(state1, waiter.name)
        result2 = state2.employees[waiter.name].last_action()
        assert TakeOrderAction(customer_id=customer1.id) == result2

        # Third turn: waiter should move to the kitchen
        state3 = await agent_controller.process(state2, waiter.name)
        result3 = state3.employees[waiter.name].last_action()
        assert MoveToNewRoom(destination=KITCHEN) ==  result3

        # Fourth turn: waiter should notify the kitchen of the order
        state4 = await agent_controller.process(state3, waiter.name)
        result4 = state4.employees[waiter.name].last_action()
        assert SubmitOrdersToKitchen() == result4

        # Fifth turn: cook should prepare the food
        state5 = await agent_controller.process(state4, cook.name)
        result5 = state5.employees[cook.name].last_action()
        order_id = state5.orders_taken_by_employee(waiter.name)[0].id
        assert CookAction(order_id=order_id) == result5

        # Sixth turn: cook should pick up the order
        state6 = await agent_controller.process(state5, cook.name)
        result6 = state6.employees[cook.name].last_action()
        assert result6 == PickUpOrder(order_id=order_id)

        state7 = await agent_controller.process(state6, cook.name)
        result7 = state7.employees[cook.name].last_action()
        assert result7 == MoveToNewRoom(destination=DINING)

        # Seventh turn: cook should deliver the food
        state8 = await agent_controller.process(state7, cook.name)
        result8 = state8.employees[cook.name].last_action()
        customer_id = state8.orders[order_id].customer_id
        assert HandOrderToCustomer(customer_id=customer_id, order_id=order_id) == result8
        assert state8.customers[customer1.id].status == CustomerStatus.EATING
        assert state8.orders[order_id].status == OrderStatus.DELIVERED
        # There should be no more orders

