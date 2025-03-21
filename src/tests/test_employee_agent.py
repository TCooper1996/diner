import sys
import os
import unittest
from typing import Dict

import pytest

from src.agents.RefinementAgent import RefinementAgent

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.actions import *
from src.state.employee import Employee
from src.state.game import GameState
from src.state.order import Order, OrderStatus
from src.state.customer import Customer
from src.game_engine.location import  DINING, ENTRANCE, KITCHEN
from src.agents.employeeAgent import EmployeeAgentController

@pytest.mark.asyncio
class TestEmployeeAgent(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test case"""
        # Create an agent controller
        self.agent_controller = EmployeeAgentController()
        
        # Create a game state
        self.game_state = GameState()
        
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
        result, updated_state = await self.agent_controller.process(self.game_state, host.name)
        
        # Check that the host tried to seat the customer
        self.assertEqual(SeatAction(), result.action)
        
        # Verify customer was moved to dining area
        self.assertEqual(updated_state.customers[customer.id].location, DINING)
        self.assertEqual(updated_state.customers[customer.id].status, "seated")
        
    async def test_seating_host_observation(self):
        """Test that a host waits when there are no customers to seat"""
        # Create an employee with instructions to seat customers
        host = Employee(name="Jim", instruction="Your job is to seat customers when they arrive")
        host.location = "entrance"  # Explicitly set location to entrance
        
        # Add the employee to the game state
        self.game_state.employees[host.name] = host
        
        # No customers added
        
        # Process the host's turn
        result, updated_state = await self.agent_controller.process(self.game_state, host.name)
        employeeState = updated_state.employees[host.name].action
        
        # Check that the host observed there are no customers
        self.assertEqual(WaitAction(), employeeState)
        
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
        customer.status = "seated"
        self.game_state.add_customer(customer)
        
        # Process the waiter's turn
        result, updated_state = await self.agent_controller.process(self.game_state, waiter.name)
        
        # Check that the waiter took the customer's order
        self.assertEqual(TakeOrderAction(), result.action)
        
        # Verify customer status was updated
        self.assertEqual(updated_state.customers[customer.id].status, "ordered")
        
        # Verify an order was created
        self.assertTrue(len(updated_state.orders) > 0)
        
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
        customer.status = "seated"
        self.game_state.add_customer(customer)
        
        # Process the waiter's turn
        result, updated_state = await self.agent_controller.process(self.game_state, waiter.name)
        
        # Check that the waiter moved to the dining area
        self.assertEqual(MoveToNewRoom(destination=DINING), result.action)
        self.assertEqual(updated_state.employees[waiter.name].location, DINING)
        
        
    async def test_cook_prepares_food(self):
        """Test that a cook prepares food for pending orders"""
        # Create a cook with instructions to prepare food
        cook = Employee(name="Bob", instruction="Your job is to cook food")
        cook.location = "kitchen"  # Set location to kitchen
        
        # Add the cook to the game state
        self.game_state.employees[cook.name] = cook
        
        # Add a customer with an order
        customer = Customer()
        customer.status = "ordered"
        self.game_state.add_customer(customer)
        
        # Create an order for the customer
        order = Order(customer_id=customer.id, items=["burger", "fries"], server=cook.name, status=OrderStatus.TAKEN)
        self.game_state.orders[order.id] = order
        
        # Process the cook's turn
        result, updated_state = await self.agent_controller.process(self.game_state, cook.name)
        
        # Check that the cook prepared the food - actual order_id will be generated dynamically
        self.assertEqual(result.action, CookAction(order_id=order.id))
        
        # Verify order status was updated
        self.assertEqual(updated_state.orders[order.id].status, OrderStatus.READY)
        
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
        result1, state1 = await self.agent_controller.process(self.game_state, host.name)
        self.assertEqual(SeatAction(), result1.action)
        
        # Second turn: waiter should take the customer's order
        result2, state2 = await self.agent_controller.process(state1, waiter.name)
        self.assertEqual(TakeOrderAction(), result2.action)

        # Third turn: waiter should move to the kitchen
        result3, state3 = await self.agent_controller.process(state2, waiter.name)
        self.assertEqual(MoveToNewRoom(destination=KITCHEN), result3.action)

        # Fourth turn: waiter should notify the kitchen of the order
        result4, state4 = await self.agent_controller.process(state3, waiter.name)
        self.assertEqual(SubmitOrdersToKitchen(), result4.action)

        # Fifth turn: cook should prepare the food
        result5, state5 = await self.agent_controller.process(state4, cook.name)
        self.assertIsInstance(result5.action, CookAction)

        # Sixth turn: cook should move to the dining area
        result6, state6 = await self.agent_controller.process(state5, cook.name)
        self.assertEqual(MoveToNewRoom(destination=DINING), result6.action)

        # Seventh turn: cook should deliver the food
        result7, state7 = await self.agent_controller.process(state6, cook.name)
        self.assertEqual(HandOrderToCustomer(), result7.action)
        self.assertEqual(state7.customers[customer1.id].status, "eating")
        # There should be no more orders
        self.assertEqual(len(state7.orders), 0)

