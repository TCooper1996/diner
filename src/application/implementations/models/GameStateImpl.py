from copy import deepcopy
from dataclasses import dataclass

from src.actions import Action
from src.agents.models.Model import StandardMessage
from src.application.implementations.repos import *
from src.application.implementations.services.NavigationServiceImpl import NavigationServiceImpl
from src.application.services.AgentService import AgentServiceImpl
from src.core.models.ActiveTurn import ActiveTurn, EmployeeUpdate
from src.core.models.GameState import GameState


class GameStateImpl(ActionRepoImpl, EmployeeMessageRepoImpl, CustomerRepoImpl, OrderRepoImpl, 
                   EmployeeRepoImpl, SeatRepoImpl, EntranceRepoImpl, GrillRepoImpl,
                   CustomerSeatRepoImpl, CustomerOrderRepoImpl, EmployeeGrillRepoImpl, 
                   EmployeeOrderRepoImpl, GameState):
    def __init__(self, navigation_service: NavigationServiceImpl, agent_service: AgentServiceImpl, active_turn: ActiveTurn):
        # Initialize all parent repository classes
        ActionRepoImpl.__init__(self)
        EmployeeMessageRepoImpl.__init__(self)
        CustomerRepoImpl.__init__(self)
        OrderRepoImpl.__init__(self)
        EmployeeRepoImpl.__init__(self)
        SeatRepoImpl.__init__(self)
        EntranceRepoImpl.__init__(self)
        GrillRepoImpl.__init__(self)
        CustomerSeatRepoImpl.__init__(self)
        CustomerOrderRepoImpl.__init__(self)
        EmployeeGrillRepoImpl.__init__(self)
        EmployeeOrderRepoImpl.__init__(self)
        
        # GameState specific properties
        self.tick = 0
        self._navigation_service = navigation_service
        self._agent_service = agent_service
        self._active_turn = active_turn


    def get_tick(self) -> int:
        return self.tick
    
    def get_navigation_service(self) -> NavigationServiceImpl:
        return self._navigation_service

    def get_next_valid_action(self, employee_name, state_message, messages, verify):
        return self._agent_service.get_next_valid_action(employee_name, state_message, messages, verify)

    def get_whose_turn(self) -> ActiveTurn:
        return self._active_turn
    
    def set_whose_turn(self, active_turn: ActiveTurn) -> None:
        self._active_turn = active_turn
    
    def copy(self) -> 'GameState':
        """
        Create a deep copy of the game state.
        
        This creates a new GameStateImpl instance with copies of all the
        repository data structures to ensure no shared references.
        
        Returns:
            A new GameStateImpl instance with copied data.
        """
        # Create a new instance
        new_state = GameStateImpl(self._navigation_service, self._agent_service, self._active_turn)
        
        # Copy the game state properties
        new_state.tick = self.tick

        
        # Copy ActionRepo data
        new_state._employee_actions = deepcopy(self._employee_actions)
        
        # Copy EmployeeMessageRepo data
        new_state._employee_messages = deepcopy(self._employee_messages)
        
        # Copy CustomerRepo data
        new_state._customers = deepcopy(self._customers)
        
        # Copy OrderRepo data
        new_state._orders = deepcopy(self._orders)
        new_state._next_order_id = self._next_order_id
        
        # Copy EmployeeRepo data
        new_state._employees = deepcopy(self._employees)
        
        # Copy SeatRepo data
        new_state._seats = deepcopy(self._seats)
        
        # Copy EntranceRepo data
        new_state._entrances = deepcopy(self._entrances)
        
        # Copy GrillRepo data
        new_state._grills = deepcopy(self._grills)
        
        # Copy CustomerSeatRepo data - single dictionary
        new_state._customer_seats = deepcopy(self._customer_seats)
        
        # Copy CustomerOrderRepo data - single dictionary
        new_state._customer_orders = deepcopy(self._customer_orders)
        
        # Copy EmployeeGrillRepo data - single dictionary
        new_state._employee_grills = deepcopy(self._employee_grills)
        
        # Copy EmployeeOrderRepo data - two dictionaries for different relationships
        new_state._employee_orders_taken = deepcopy(self._employee_orders_taken)
        new_state._employee_orders_carried = deepcopy(self._employee_orders_carried)
        
        return new_state
    