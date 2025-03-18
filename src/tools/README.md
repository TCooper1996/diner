# Tools Directory

## Overview

This directory contains the action tools that employees can use to interact with the restaurant environment. These tools implement the actual functionality that changes the game state.

## Technical Details

### `restaurant_tools.py`

This file contains all the tool functions that employees can use to interact with the restaurant. Each function:
- Takes parameters including the employee name, current location, and game state
- Returns a string describing the result of the action
- Contains validation logic to ensure actions are only performed in appropriate locations

#### Tool Functions

1. **`move_to_location(employee_name, current_location, destination, game_state)`**
   - Moves an employee between restaurant areas
   - Validates that the destination is valid
   - Returns feedback about the movement

2. **`seat_customer(employee_name, location, game_state)`**
   - Seats waiting customers from entrance to dining area
   - Only works if employee is at entrance
   - Requires waiting customers to be present
   - Returns feedback about the seating action

3. **`take_order(employee_name, location, game_state)`**
   - Takes orders from seated customers
   - Only works if employee is in dining area
   - Requires seated customers without orders
   - Returns feedback about the order-taking action

4. **`cook_food(employee_name, location, game_state)`**
   - Prepares food for pending orders
   - Only works if employee is in kitchen
   - Requires orders in the pending/taken state
   - Returns feedback about the cooking action

5. **`deliver_food(employee_name, location, game_state)`**
   - Delivers prepared food to customers
   - Only works if employee is in kitchen
   - Requires orders in the ready state
   - Returns feedback about the delivery action

6. **`observe_environment(employee_name, location, game_state)`**
   - Provides detailed information about the current location
   - Returns different observations based on location:
     - **Entrance**: Reports waiting customers
     - **Dining**: Reports seated customers, those waiting for orders, and those eating
     - **Kitchen**: Reports pending, cooking, and ready orders

## Integration with LangGraph

These tools are integrated into the LangGraph through dedicated action nodes in the Employee agent:

1. Each action node in the graph extracts relevant parameters from the agent state
2. The node calls the appropriate tool function with those parameters
3. The result is stored in the agent state and returned to the main game loop
4. The Game class displays these results to the player

## Tools vs. Multi-Node Design

The tools in this directory showcase why a multi-node design is valuable in LangGraph:

1. Each tool has specific location requirements that need validation
2. The planning node can decide which tool is appropriate based on context
3. Action nodes can specialize in properly invoking their respective tools
4. Having separate nodes makes it easier to add new tools or modify existing ones

This separation of concerns keeps the code organized and makes the system more maintainable and extensible.