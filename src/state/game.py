from typing import Dict, List, Optional
from enum import Enum

from pydantic import BaseModel, Field

from src.state.employee import Employee
from src.game_engine.location import *
from src.state.customer import Customer
from src.state.order import Order, OrderItem, OrderStatus


class GameState(BaseModel):
    customers: Dict[str, Customer] = Field(default_factory=dict)
    orders: Dict[str, Order] = Field(default_factory=dict)
    unhappy_customers: int = Field(default=0)
    employees: Dict[str, Employee] = Field(default_factory=dict)
    
    def add_customer(self, customer: Customer):
        """Add a new customer to the restaurant"""
        self.customers[customer.id] = customer
        
    def get_waiting_customers(self):
        """Get customers waiting at the entrance"""
        return [c for c in self.customers.values() 
                if c.location == ENTRANCE and c.status == "waiting"]
    
    def get_seated_customers(self):
        """Get customers seated in the dining area waiting to order"""
        return [c for c in self.customers.values() 
                if c.location == DINING and c.status == "seated"]
    
    def get_pending_orders(self):
        """Get orders that need to be cooked"""
        return [o for o in self.orders.values() 
                if o.status == OrderStatus.PENDING]

    def submit_orders_to_kitchen(self, orderIds: List[str]):
        """Submit orders to the kitchen"""
        for orderId in orderIds:
            self.orders[orderId].status = OrderStatus.TAKEN
    
    def get_ready_orders(self):
        """Get orders that are ready to be delivered"""
        return [o for o in self.orders.values() 
                if o.status == OrderStatus.READY]
    
    def seat_customer(self, customer_id: str) -> bool:
        """Seat a customer at a dining table"""
        if customer_id in self.customers:
            customer = self.customers[customer_id]
            customer.location = DINING
            customer.status = "seated"
            return True
        return False
    
    def take_customer_order(self, customer_id: str, employee_id: str) -> List[OrderItem]:
        """Take an order from a customer and create an order"""
        if customer_id in self.customers:
            customer = self.customers[customer_id]
            customer.status = "ordered"
            
            # Generate a random order
            items = customer.take_order()
            
            # Create an order
            order = Order(customer_id=customer_id, items=items, server=employee_id, status=OrderStatus.PENDING)
            self.orders[order.id] = order
            
            return items
        raise ValueError(f"Customer {customer_id} not found")

    def bring_orders_to_kitchen(self, employee_id) -> bool:
        """Bring a servers orders to the kitchen"""
        # Orders can only be delivered to the kitchen by the server that took them
        orders = [o for o in self.orders.values() if o.server == employee_id and o.status == OrderStatus.PENDING]

        # Update status
        for order in orders:
            order.status = OrderStatus.TAKEN
            self.orders[order.id] = order
        return True
    
    def cook_order(self, order_id: str) -> bool:
        """Mark an order as ready"""
        if order_id in self.orders:
            self.orders[order_id].status = OrderStatus.READY
            return True
        return False
    
    def deliver_order(self, order_id: str) -> bool:
        """Deliver an order to a customer"""
        if order_id in self.orders:
            order = self.orders[order_id]
            customer_id = order.customer_id
            
            if customer_id in self.customers:
                self.customers[customer_id].status = "eating"
                del self.orders[order_id]
                return True
        return False
        
    def update_customers(self) -> int:
        """Update customer wait times and return number of unhappy customers this tick"""
        unhappy_this_tick = 0
        customers_to_remove = []
        
        for customer_id, customer in self.customers.items():
            customer.waiting_time += 1
            
            # Update eating time for customers who are eating
            if customer.status == "eating":
                customer.eating_time += 1
            
            # Check if customer has been waiting too long
            if customer.waiting_time >= customer.patience:
                if customer.location != GONE:
                    unhappy_this_tick += 1
                    self.unhappy_customers += 1
                    customers_to_remove.append(customer_id)
            
            # Check if customer is done eating and leaving happy
            if customer.status == "eating" and customer.eating_time >= 3:
                customers_to_remove.append(customer_id)
                print(f"Customer {customer_id} finished eating and left happy!")
        
        # Remove customers who have left
        for customer_id in customers_to_remove:
            if customer_id in self.customers:
                del self.customers[customer_id]
                
        return unhappy_this_tick