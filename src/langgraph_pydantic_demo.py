"""
Demo showing how to use a Pydantic model as state in LangGraph
"""
from typing import Dict, List, Optional, Literal
import langgraph.graph as lg
from pydantic import BaseModel, Field

# Define a Pydantic model to use as our state
class RestaurantState(BaseModel):
    # State fields
    customer_count: int = 0
    orders_pending: int = 0
    next_node: Optional[str] = None
    
    # A method to demonstrate that methods are preserved
    def add_customer(self) -> str:
        """Add a customer and return a message"""
        self.customer_count += 1
        return f"Added a customer! Total count is now {self.customer_count}"

# Define nodes for our graph
def greet_node(state: RestaurantState) -> RestaurantState:
    """First node that greets and adds a customer"""
    # Call the method on our state object
    message = state.add_customer()
    print(f"Greeting node: {message}")
    
    # Set next node
    state.next_node = "order"
    return state

def order_node(state: RestaurantState) -> RestaurantState:
    """Second node that creates an order"""
    state.orders_pending += 1
    print(f"Order node: Customer count is {state.customer_count}, orders: {state.orders_pending}")
    
    # Set next node
    state.next_node = "cook"
    return state

def cook_node(state: RestaurantState) -> RestaurantState:
    """Third node that cooks the order"""
    if state.orders_pending > 0:
        state.orders_pending -= 1
        print(f"Cook node: Prepared an order! {state.orders_pending} orders left")
    else:
        print("Cook node: No orders to prepare")
    
    # This is the end of our flow
    state.next_node = None
    return state

# Build and run the graph
def main():
    # Define our graph
    builder = lg.Graph()
    
    # Add nodes
    builder.add_node("greet", greet_node)
    builder.add_node("order", order_node)
    builder.add_node("cook", cook_node)
    
    # Add edges with no conditional routing
    builder.add_edge("greet", "order")
    builder.add_edge("order", "cook")
    builder.add_edge("cook", lg.END)
    
    # Set entry point
    builder.set_entry_point("greet")
    
    # Compile graph
    graph = builder.compile()
    
    # Create initial state
    initial_state = RestaurantState(customer_count=0, orders_pending=0)
    
    # Run the graph
    print("Running the graph with a Pydantic model as state...")
    final_state = graph.invoke(initial_state)
    
    # Verify the method still works after going through the graph
    result = final_state.add_customer()
    print(f"\nAfter graph execution: {result}")
    print(f"Final state: {final_state.model_dump()}")

if __name__ == "__main__":
    main()