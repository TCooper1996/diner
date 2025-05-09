from dataclasses import dataclass
from typing import Protocol

from src.core.repos import *
from src.core.services import *


"""
Ideally, only actions should be able to modify the state of the restaurant.
RestaurantState should only contain real world objects and relationships, no agent messages 
"""
class RestaurantState(CustomerRepo, OrderRepo, EmployeeRepo, SeatRepo, EntranceRepo, GrillRepo,
                    CustomerSeatRepo, CustomerOrderRepo, EmployeeGrillRepo, EmployeeOrderRepo, 
                    Protocol):
    def get_navigation_service(self) -> NavigationService:
        ...