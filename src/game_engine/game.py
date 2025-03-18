import time
from typing import Dict, List
from rich.console import Console

from src.state.employee import Employee
from src.agents.employeeAgent import EmployeeAgentController
from src.game_engine.location import Location
from src.state.customer import Customer
from src.state.game import GameState

class Game:
    def __init__(self):
        self.console = Console()
        self.state = GameState()
        self.employees: Dict[str, Employee] = {}
        self.agent_controller = EmployeeAgentController()  # Create a single agent controller
        self.customer_timer = 0
        self.max_wait_time = 20  # game ticks before customers leave unhappy
        
    def setup_employees(self):
        """Get instructions from the player for each employee"""
        self.console.print("\n[bold green]Welcome to Diner Simulator![/bold green]")
        self.console.print("You need to instruct your employees on how to run the restaurant.")
        
        # Create employees with player-provided instructions
        instructions = ["Seat the customers when they arrive", "take orders from the customers after they are seated and bring them to the kitchen", "cook the food and deliver it to the customers"]
        employee_names = ["Jim", "Alice", "Bob"]
        for i, name in enumerate(employee_names):
            self.console.print(f"\n[bold]Employee: {name}[/bold]")
            instruction = instructions[i]  # input(f"What instructions would you like to give {name}? ")
            print(f"{name} will {instruction}")
            
            # Create the employee and add to state
            self.employees[name] = Employee(name=name, instruction=instruction)
            self.state.employees[name] = self.employees[name]
            
        self.console.print("\n[bold green]All employees have been instructed![/bold green]")
        self.console.print("The simulation will now begin...\n")
        time.sleep(2)

    def start(self):
        """Start the game"""
        self.setup_employees()
        
        game_over = False
        tick = 0
        
        # Add initial customer
        self.state.add_customer(Customer())
        
        while not game_over:
            tick += 1
            self.console.print(f"\n[bold blue]===== Tick {tick} =====[/bold blue]")
            
            # Run each employee's turn
            for name, employee in self.employees.items():
                # Process returns both the action result and the updated state
                action_result, updated_state = self.agent_controller.process(self.state, employee.name)
                self.console.print(f"[bold green][{employee.name}[/bold green]] Location: {employee.location}; {action_result}")
                self.console.print(f"[bold green][{employee.name}[/bold green]] '{employee.last_thought()}'")
                
                # Set the game state to the updated state returned by the agent
                self.state = updated_state

            
            # Check win/loss conditions
            if tick % 5 == 0 and len(self.state.customers) < 3:  # Add new customer every 5 ticks
                self.state.add_customer(Customer())
                self.console.print("[bold yellow]A new customer has arrived![/bold yellow]")
                
            # Update customer wait times and check for unhappy customers
            unhappy_customers = self.state.update_customers()
            if unhappy_customers > 0:
                self.console.print(f"[bold red]{unhappy_customers} customer(s) left unhappy![/bold red]")
                
            if self.state.unhappy_customers >= 3:
                game_over = True
                self.console.print("\n[bold red]GAME OVER![/bold red] Too many unhappy customers.")
                retry = input("\nWould you like to try again with new instructions? (y/n): ")
                if retry.lower() == 'y':
                    self.__init__()  # Reset game state
                    self.start()
                    return

            # print status of customers
            for customer_id, customer in self.state.customers.items():
                self.console.print(f"[[bold yellow]{customer.name}[/bold yellow]] Status: {customer.status}, Waiting Time: {customer.waiting_time}, Location: {customer.location}")
            
            # Short pause between ticks for readability
            time.sleep(0.6)