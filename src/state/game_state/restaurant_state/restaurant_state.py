import copy
from dataclasses import Field, dataclass, field
import json
from typing import Dict, List, Literal, Optional, Set, Tuple

from src.common.location import DINING, ENTRANCE, GONE
from src.common.position import Position
from src.core.types import StationType, TileType
from .entities import Customer, Employee, Order, OrderStatus
from .managers import OrderManager, StationManager, LocationManager

"""
    An entity is any game object that will have a visible world position
"""
EntityType = Literal["employee", "customer", "station"] 
@dataclass
class RestaurantState:
    location_manager: LocationManager[TileType]
    customers: Dict[str, Customer] = field( default_factory=dict)
    order_manager: OrderManager = field(default_factory=OrderManager)  # Manages all orders in the restaurant
    employees: Dict[str, Employee] = field(default_factory=dict)
    entities: Dict[str, EntityType] = field(default_factory=dict)  # Maps entity ID to its type ("employee" or "customer")
    order_takers: Dict[str, List[str]] = field(default_factory=dict)  # Maps employee name to list of order IDs they have taken
    order_carriers: Dict[str, List[str]] = field( default_factory=dict)  # Maps employee name to list of order IDs they are carrying
    station_manager: StationManager[StationType] = field(default_factory=StationManager)
    employee_instructions: Dict[str, str] = field(default_factory=dict)  # Maps employee name to their current instruction

    @property
    def employee_names(self) -> List[str]:
        return [name for name,e_type in self.entities.items() if e_type == "employee"]


    def __copy__(self):
        return RestaurantState(
            customers=self.customers.copy(),
            order_manager=copy.deepcopy(self.order_manager),
            employees=self.employees.copy(),
            entities=self.entities.copy(),
            order_takers=self.order_takers.copy(),
            order_carriers=self.order_carriers.copy(),
            employee_instructions=self.employee_instructions.copy,
            location_manager=copy.deepcopy(self.location_manager),  # Assuming LocationManager is copyable
            station_manager=copy.deepcopy(self.station_manager),  # Assuming StationManager is copyable
        )

    def get_position_of(self, entity_id: str) -> Position:
        """Get the position of an entity by its ID"""
        return self.location_manager._get_entity_position(entity_id)



    def to_prompt(self) -> str:
        employees = [self.grab_employee(e) for e in self.employees]
        employee_dict = {e.name: {
            "location": self.location_manager.entity_location_tile(e.name).tileType,
            "orders_taken": [repr(o) for o in self.orders_taken_by_employee(e.name)],
            "orders_being_carried": [repr(o) for o in self.orders_carried_by_employee(e.name)],
            "type": "employee"
        } for e in employees}
        customer_dict = {
            c.name: {
                "status": c.status.value,
                "orders": [repr(o) for o in self.get_customers_orders(c.id)],
                "type": "customer",
                } for c in self.customers.values()}
        d = {
            "employees": employee_dict,
            "customers": customer_dict,
            "orders": {f"#{o.id}": {"status": o.status.value, "order#": o.id} for o in self.order_manager.get_orders()},
        }
        return json.dumps(d, indent=4)

    def entity_at_location(self, entity_id, location: TileType) -> bool:
        """Check if an entity is at a specific location"""
        tileType = self.location_manager.entity_location_tile(entity_id).tileType
        return tileType == location


    def get_seats(self) -> List[str]:
        return [s.station_id for s in self.station_manager.get_stations() if s.station_type == "dining"]
    
    def get_floors(self) -> List[Position]:
        return [f.pos for f in self.location_manager.floor_plan.get_tiles()]

    def orders_taken_by_employee(self, employee_name: str) -> List[str]:
        return self.order_takers.get(employee_name, [])

    def orders_carried_by_employee(self, employee_name: str) -> List[str]:
        return self.order_carriers.get(employee_name, [])
    
    def assign_order_to_employee(self, employee_name: str, order_id: str):
        if employee_name not in self.order_takers:
            self.order_takers[employee_name] = []
        self.order_takers[employee_name].append(order_id)

    def remove_order_from_employee(self, employee_name: str, order_id: str):
        if employee_name in self.order_takers:
            self.order_takers[employee_name].remove(order_id)

    def assign_order_to_employee_inventory(self, employee_name: str, order_id: str):
        if employee_name not in self.order_carriers:
            self.order_carriers[employee_name] = []
        self.order_carriers[employee_name].append(order_id)

    def remove_order_from_employee_inventory(self, employee_name: str, order_id: str):
        if employee_name in self.order_carriers:
            self.order_carriers[employee_name].remove(order_id)

    def update_order_status(self, order_id: str, status: OrderStatus):
        self.order_manager.grab_order(order_id=order_id).status = status

    def grab_employee(self, employee_name: str) -> Employee:
        return self.employees[employee_name]

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get a customer by ID"""
        c = self.customers.get(customer_id)
        if c:
            return c
        # try by name
        for customer in self.customers.values():
            if customer.name == customer_id:
                return customer
        return None

    def grab_customer(self, customer_id: str) -> Customer:
        return self.customers[customer_id]


    def get_waiting_customers(self):
        """Get customers waiting at the entrance"""
        return [c for c in self.customers.values()
                if c.location.at(ENTRANCE) and c.status == "waiting"]

    def get_customers_orders(self, customer_id: str) -> List[Order]:
        return [o for o in self.order_manager.get_orders() if o.customer_id == customer_id]

    def get_seated_customers(self):
        """Get customers seated in the dining area waiting to order"""
        return [c for c in self.customers.values()
                if c.location.at(DINING) and c.status == "seated"]

