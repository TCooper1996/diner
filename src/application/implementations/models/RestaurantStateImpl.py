from dataclasses import dataclass

from src.core.models.RestaurantState import RestaurantState
from src.core.repos import *
from src.core.services import *


@dataclass
class RestaurantStateImpl(RestaurantState):
    # Basic entities
    customer_repo: CustomerRepo
    order_repo: OrderRepo
    employee_repo: EmployeeRepo
    seat_repo: SeatRepo
    entrance_repo: EntranceRepo
    grill_repo: GrillRepo

    employee_message_repo: EmployeeMessageRepo

    customer_seat_repo: CustomerSeatRepo
    employee_grill_repo: EmployeeGrillRepo

    navigation_service: NavigationService

    def get_customer_repo(self) -> CustomerRepo:
        return self.customer_repo

    def get_order_repo(self) -> OrderRepo:
        return self.order_repo

    def get_employee_repo(self) -> EmployeeRepo:
        return self.employee_repo

    def get_message_repo(self) -> EmployeeMessageRepo:
        return self.employee_message_repo
        
    def get_customer_seat_repo(self) -> CustomerSeatRepo:
        return self.customer_seat_repo

    def get_seat_repo(self) -> SeatRepo:
        return self.seat_repo

    def get_entrance_repo(self) -> EntranceRepo:
        return self.entrance_repo
    
    def get_grill_repo(self) -> GrillRepo:
        return self.grill_repo
    
    def get_employee_grill_repo(self) -> EmployeeGrillRepo:
        return self.employee_grill_repo

    def get_navigation_service(self) -> NavigationService:
        return self.navigation_service
