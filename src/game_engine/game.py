import asyncio
from functools import reduce
import time
from typing import Dict, List, Tuple
from rich.console import Console

from src.actions import EmployeeAction
from src.actions.base import ActionResult
from src.agents.RefinementAgent import RefinementAgent
from src.game_engine.gameLogger import GameLogger
from src.state.employee import Employee
from src.agents.employeeAgent import EmployeeAgentController
from rich.text import Text
from src.game_engine.location import Location
from src.state.customer import Customer
from src.state.game import GameState
from src.state.types import EmployeeTurn
from src.utils.async_reduce import async_reduce


class Game:
    def __init__(self):
        self.message = ""
        self.console = Console()
        self.state = GameState()
        self.agent_controller = EmployeeAgentController()  # Create a single agent controller
        self.customer_timer = 0
        self.max_wait_time = 20  # game ticks before customers leave unhappy
        
    def setup_employees(self, employeeInstructions: List[Tuple[str, str]]):
        """Get instructions from the player for each employee"""
        self.console.print("\n[bold green]Welcome to Diner Simulator![/bold green]")
        self.console.print("You need to instruct your employees on how to run the restaurant.")
        # Create employees with player-provided instructions
        for instructions, name in employeeInstructions:
            self.console.print(f"\n[bold]Employee: {name}[/bold]")
            print(f"{name} will {instructions}")
            
            # Create the employee and add to state
            self.state.employees[name] = Employee(name=name, instruction=instructions)
            
        self.console.print("\n[bold green]All employees have been instructed![/bold green]")
        self.console.print("The simulation will now begin...\n")

    async def start(self, writer: GameLogger):
        self.writer = writer
        """Start the game"""
        instructions = ["Seat the customers when they arrive", "take orders from the customers after they are seated and bring them to the kitchen", "cook the food and deliver it to the customers"]
        start = time.perf_counter()
        refinedInstructions = await asyncio.gather(*[RefinementAgent().refine_prompt(instruction) for instruction in instructions])
        end = time.perf_counter()
        writer.log_message(f"Refinement time: {end - start} seconds")

        employee_names = ["Jim", "Alice", "Bob"]
        self.setup_employees(list(zip(refinedInstructions, employee_names)))
        
        game_over = False
        tick = 0
        
        # Add initial customer
        self.state.add_customer(Customer())

        await self.loop(self.state, tick)

        

    async def loop(self, gamestate: GameState, tick: int):
        writer = self.writer
        writer.turn_started()
        
        # Run each employee's turn
        updated_state = gamestate.model_copy(deep=True)
        employee_names = list(updated_state.employees.keys())

            
        stateHistory = await async_reduce(self.employee_turn, employee_names, updated_state)
        state2 = stateHistory[-1].current_state()

        
        # Check win/loss conditions
        if tick % 5 == 0 and len(state2.customers) < 3:  # Add new customer every 5 ticks
            c = Customer()
            state2.add_customer(c)
            writer.new_customer(c.name, "A new customer has arrived!")
            
        # Update customer wait times and check for unhappy customers
        customers_leaving = state2.update_customers()
        for customer_id, happy in customers_leaving:
            if not happy:
                state2.unhappy_customers += 1
            c = gamestate.grab_customer(customer_id)
            writer.customer_left(c.name, happy, f"left {'happy' if happy else 'unhappy'}!")
            
        if state2.unhappy_customers > 0:
            writer.game_over("Too many unhappy customers!")
            return

        # print status of customers
        for customer_id, customer in state2.customers.items():
            writer.customer_status(customer.name, f"Status: {customer.status}, Waiting Time: {customer.waiting_time}, Location: {customer.location}")
        
        # Short pause between ticks for readability
        await self.loop(state2, tick + 1)
        await asyncio.sleep(0.1)



    async def employee_turn(self, _gamestate: GameState, name: str) -> EmployeeTurn:
        gamestate = _gamestate.model_copy(deep=True)
        # Process returns both the action result and the updated state
        results = EmployeeTurn(employee_name=name, decisions= await self.agent_controller.process(gamestate, name))
        employee = results.current_state().grab_employee(name)
        self.log_employee_turn(employee, results.action())
        return results
    
    def log_employee_turn(self, employee: Employee, action: EmployeeAction):
        self.writer.employee_turn(employee.name, f"Location={employee.location}, action={repr(action)}, decision_text={employee.last_decision_text()}, decision_result={employee.last_decision_result()}")