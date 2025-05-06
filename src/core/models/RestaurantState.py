from dataclasses import dataclass
from typing import Protocol

from src.core.repos import *
from src.core.services import *


"""
Ideally, only actions should be able to modify the state of the restaurant.
RestaurantState should only contain real world objects and relationships, no agent messages 
"""
class RestaurantState(Protocol):
    # Basic entities

    def get_customer_repo(self) -> CustomerRepo:
        ...

    def get_order_repo(self) -> OrderRepo:
        ...

    def get_employee_repo(self) -> EmployeeRepo:
        ...

    def get_message_repo(self) -> EmployeeMessageRepo:
        ...
    
    def get_seat_repo(self) -> SeatRepo:
        ...

    def get_entrance_repo(self) -> EntranceRepo:
        ...
    
    def get_grill_repo(self) -> GrillRepo:
        ...
        

    # Relationships between entities
    def get_customer_seat_repo(self) -> CustomerSeatRepo:
        ...

    def get_customer_order_repo(self) -> CustomerOrderRepo:
        ...
    
    def get_employee_grill_repo(self) -> EmployeeGrillRepo:
        ...
    
    def get_employee_order_repo(self) -> EmployeeOrderRepo:
        ...

    def get_navigation_service(self) -> NavigationService:
        ...

    def get_customer_seat_service(self) -> CustomerSeatService:
        ...
    