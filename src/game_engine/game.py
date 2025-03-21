import asyncio
from functools import reduce
import time
from typing import Dict, List, Tuple
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


class Game:
    def __init__(self):
        self.message = ""
        self.console = Console()
        self.state = GameState()
        self.agent_controller = EmployeeAgentController(Claude(create_tools()))  # Create a single agent controller
        self.customer_timer = 0
        self.max_wait_time = 20  # game ticks before customers leave unhappy
        self.pause_event = asyncio.Event()
        
    def setup_employees(self, employeeInstructions: Dict[str, str]):
        """Get instructions from the player for each employee"""
        self.console.print("\n[bold green]Welcome to Diner Simulator![/bold green]")
        self.console.print("You need to instruct your employees on how to run the restaurant.")
        # Create employees with player-provided instructions
        for name, instructions in employeeInstructions.items():
            self.console.print(f"\n[bold]Employee: {name}[/bold]")
            print(f"{name} will {instructions}")
            
            # Create the employee and add to state
            self.state.employees[name] = Employee(name=name, instruction=instructions)
            
        self.console.print("\n[bold green]All employees have been instructed![/bold green]")
        self.console.print("The simulation will now begin...\n")

    async def start(self, writer: GameLogger, pause_event: asyncio.Event):
        self.pause_event = pause_event
        self.writer = writer
        """Start the game"""
        instructions = {
            "Alice":"Seat the customers when they arrive",
            "Bob": "take orders from the customers after they are seated and bring them to the kitchen",
            "Jim": "cook the food and deliver it to the customers"
            }
        
        async def refine_instruction(name, raw_instruction):
            return name, await RefinementAgent().refine_prompt(raw_instruction)
        start = time.perf_counter()
        refinedInstructions = await asyncio.gather(*[refine_instruction(item[0], item[1]) for item in instructions.items()])
        end = time.perf_counter()
        writer.log_message(f"Refinement time: {end - start} seconds")

        self.setup_employees({item[0]:item[1] for item in refinedInstructions})
        
        
        # Add initial customer
        self.state.add_customer(Customer())

        await self.loop(self.state, 0)

        

    async def loop(self, gamestate: GameState, tick: int):
        await self.pause_event.wait()
        writer = self.writer
        writer.turn_started()
        
        # Run each employee's turn
        updated_state = gamestate.model_copy(deep=True)
        employee_names = list(updated_state.employees.keys())

            
        stateHistory = await self.run_employee_turns(updated_state)
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
        start = time.perf_counter()
        results = EmployeeTurn(employee_name=name, decisions= await self.agent_controller.process(gamestate, name))
        end = time.perf_counter()
        self.writer.log_message(f"Employee {name} turn time: {end - start} seconds")
        employee = results.current_state().grab_employee(name)
        self.log_employee_turn(employee, results.action())
        return results

    async def run_employee_turns(self, gamestate: GameState) -> List[EmployeeTurn]:
        value = gamestate
        results: List[EmployeeTurn] = []
        for item in gamestate.employees.keys():
            results.append( await self.employee_turn(value, item))
            value = results[-1].current_state()
            await self.pause_event.wait()
        
        return results
    
    def log_employee_turn(self, employee: Employee, action: EmployeeAction):
        self.writer.employee_turn(employee.name, f"Location={employee.location}, action={repr(action)}, decision_text={employee.last_decision_text()}, decision_result={employee.last_decision_result()}")
