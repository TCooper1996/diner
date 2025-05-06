from dataclasses import dataclass
from typing import Tuple
from src.common.results import ActionResult
from src.core.entities.customer import Customer, CustomerStatus
from src.core.entities.seat import Seat
from src.core.models.RestaurantState import RestaurantState

@dataclass
class CustomerService:
    state: RestaurantState
    def add_customer(self):
        # find entrance
        entrances = self.state.get_entrance_repo().get_all_entrances()
        self.state.get_customer_repo().add_customer(Customer(entrances[0].position))

    def get_customer_seat(self, customer: Customer) -> Seat | None:
        customer_seats = self.state.get_customer_seat_repo()
        return customer_seats.get_customer_seat(customer.id)



    def get_or_assign_customer_seat(self, customer: Customer) -> Seat:
        state = self.state
        customer_seats = state.get_customer_seat_repo()
        seat = self.get_customer_seat(customer)
        if seat:
            return seat
        # Get all seats in SeatRepo, filter out occupied ones
        all_seats = state.get_seat_repo().get_all_seats()
        unoccupied_seats = [s for s in all_seats if not customer_seats.is_occupied(s.seat_id)]
        if not unoccupied_seats:
            raise ValueError("No unoccupied seats available.")
        # get customer position
        customer_position = customer.position
        # Get closest one
        shortest_path: Tuple[Seat, int] = (all_seats[0], 99999)
        for s in unoccupied_seats:
            path = state.get_navigation_service().get_path_between_positions(customer_position, s.position)
            if path is None or len(path) < shortest_path[1]:
                shortest_path = (s, len(path))
        customer_seats.set_customer_seat(customer.id, shortest_path[0].seat_id)
        return shortest_path[0]

class GeneralCustomerAction:
    def execute(self, state: RestaurantState, tick: int):
        cs = CustomerService(state)
        customers = state.get_customer_repo()
        add_new_customer = tick % 5 == 0 and customers.get_count() < 3
        if add_new_customer:
            cs.add_customer()
        for c in customers.get_all_customers():
            match c.status:
                case CustomerStatus.EATING:
                    c.eating_time += 1
                    if c.eating_time >= 3:
                        c.status = CustomerStatus.LEAVING
                        customers.update_customer(c)
                case CustomerStatus.LEAVING:
                    seat = cs.get_or_assign_customer_seat(c)
                    new_position = state.get_navigation_service().move_toward(c.position, seat.position)
                    c.position = new_position
                    customers.update_customer(c)
                case CustomerStatus.WAITING:
                    # Check if the customer is waiting for a seat
                    if c.waiting_time >= 3:
                        c.status = CustomerStatus.LEAVING
                        customers.update_customer(c)
                    else:
                        c.waiting_time += 1
                        customers.update_customer(c)

                        
