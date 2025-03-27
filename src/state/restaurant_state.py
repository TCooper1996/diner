
from dataclasses import dataclass, field
import json
from typing import Dict, List, Optional, Tuple

from src.game_engine.location import DINING, ENTRANCE, GONE
from src.state.customer import Customer
from src.state.employee.employee import Employee
from src.state.order import Order, OrderStatus


@dataclass
class RestaurantState:
    customers: Dict[str, Customer] = field(default_factory=dict)
    orders: Dict[str, Order] = field(default_factory=dict)
    unhappy_customers: int = field(default=0)
    employees: Dict[str, Employee] = field(default_factory=dict)
    # relationships
    # maps each employee to the orders they are responsible for
    order_takers: Dict[str, List[str]] = field(default_factory=dict)
    # maps each employee to the orders they are currently carrying
    order_carriers: Dict[str, List[str]] = field(default_factory=dict)


    def to_prompt(self) -> str:
        employees = [self.grab_employee(e) for e in self.employees]
        employee_dict = {e.name: {
            "location": e.location,
            "orders_taken": [repr(o) for o in self.orders_taken_by_employee(e.name)],
            "orders_being_carried": [repr(o) for o in self.orders_carried_by_employee(e.name)]
        } for e in employees}
        d = {
            "employees": employee_dict,
            "customers": {c.name:{"status": c.status.value, "orders": [repr(o) for o in self.get_customers_orders(c.id)]} for c in self.customers.values()},
            "orders": {f"#{o.id}": {"status": o.status.value, "items": o.items, "order#": o.id} for o in self.orders.values()},
        }
        return json.dumps(d, indent=4)


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

    def orders_taken_by_employee(self, employee_name: str) -> List[Order]:
        return list(map(self.grab_order, self.order_takers.get(employee_name, [])))
    
    def orders_carried_by_employee(self, employee_name: str) -> List[Order]:
        return list(map(self.grab_order, self.order_carriers.get(employee_name, [])))

    def grab_employee(self, employee_name: str) -> Employee:
        return self.employees[employee_name]

    
    def  get_customer(self, customer_id: str) -> Optional[Customer]:
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
    
    def add_customer(self, customer: Customer):
        """Add a new customer to the restaurant"""
        self.customers[customer.id] = customer
        
    def get_waiting_customers(self):
        """Get customers waiting at the entrance"""
        return [c for c in self.customers.values() 
                if c.location == ENTRANCE and c.status == "waiting"]

    def get_customers_orders(self, customer_id: str) -> List[Order]:
        return [o for o in self.orders.values() if o.customer_id == customer_id]
    
    def get_seated_customers(self):
        """Get customers seated in the dining area waiting to order"""
        return [c for c in self.customers.values() 
                if c.location == DINING and c.status == "seated"]

    def get_order(self, order_id: str) -> Optional[Order]:
        return self.orders.get(order_id)

    def grab_order(self, /, order_id: str | None = None, customer_id: str | None = None) -> Order:
        if order_id:
            return self.orders[order_id]
        if customer_id:
            return [o for o in self.orders.values() if o.customer_id == customer_id][0]
        raise ValueError("Must provide either order_id or customer_id")
    
    def get_pending_orders(self):
        """Get orders that need to be cooked"""
        return [o for o in self.orders.values() 
                if o.status == OrderStatus.PENDING]

    
    def get_ready_orders(self):
        """Get orders that are ready to be delivered"""
        return [o for o in self.orders.values() 
                if o.status == OrderStatus.READY]
        
    def update_customers(self) -> List[Tuple[str, bool]]:
        """Update customer wait times and return number of unhappy customers this tick"""
        customers_to_remove: List[Tuple[str, bool]] = []
        
        
        for customer_id, customer in self.customers.items():
            customer.waiting_time += 1
            
            # Update eating time for customers who are eating
            if customer.status == "eating":
                customer.eating_time += 1
            
            # Check if customer has been waiting too long
            if customer.waiting_time >= customer.patience:
                if customer.location != GONE:
                    self.unhappy_customers += 1
                    customers_to_remove.append((customer_id, False))
            
            # Check if customer is done eating and leaving happy
            if customer.status == "eating" and customer.eating_time >= 3:
                customers_to_remove.append((customer_id, True))
        
        # Remove customers who have left
        for customer_id, _ in customers_to_remove:
            if customer_id in self.customers:
                del self.customers[customer_id]
                
        return customers_to_remove