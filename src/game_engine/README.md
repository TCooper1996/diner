# Game Engine Directory

## Overview

The game engine directory contains the core simulation and game state management components. It handles restaurant state, customer behavior, and the main game loop.

## Technical Details

### `location.py`

#### `Location` Enum

Defined locations within the restaurant:
- `ENTRANCE`: Front entrance where customers arrive
- `DINING`: Dining area where customers are seated
- `KITCHEN`: Kitchen where food is prepared
- `GONE`: Special state for customers who have left

### `customer.py`

#### `Customer` Class

Represents a customer in the restaurant:

- **Properties**:
  - `id`: Unique identifier
  - `location`: Current location (from Location enum)
  - `waiting_time`: Time customer has been waiting
  - `patience`: Maximum time they'll wait before leaving unhappy
  - `status`: String representing customer state (waiting, seated, ordered, eating, done)
  - `order`: List of ordered items
  - `eating_time`: How long they've been eating

- **Methods**:
  - `place_order()`: Generates a random order
  - `start_eating()`: Updates status to eating
  - `is_done()`: Checks if customer is finished eating

### `state.py`

#### `OrderStatus` Enum

Statusus for an order:
- `PENDING`: Initial state for a new order
- `TAKEN`: Order has been taken from customer
- `COOKING`: Order is being cooked
- `READY`: Order is ready to be delivered
- `DELIVERED`: Order has been delivered to customer

#### `Order` Class

Represents a food order in the restaurant:

- **Properties**:
  - `customer_id`: ID of the customer who placed the order
  - `items`: List of food items ordered
  - `status`: Current order status (from OrderStatus enum)

#### `GameState` Class

Stores and manages the complete state of the restaurant:

- **Properties**:
  - `customers`: Dictionary of Customer objects by ID
  - `orders`: Dictionary of Order objects by ID
  - `unhappy_customers`: Count of customers who left unhappy

- **Methods**:
  - `add_customer()`: Adds a new customer to the restaurant
  - `update_customers()`: Updates waiting times and removes customers who left

### `game.py`

#### `Game` Class

Main game controller that manages the simulation:

- **Properties**:
  - `console`: Rich console for formatted text output
  - `state`: GameState instance
  - `employees`: Dictionary of Employee agents
  - `customer_timer`: Timer for customer arrivals
  - `max_wait_time`: Maximum time before customers leave unhappy

- **Methods**:
  - `setup_employees()`: Gets player instructions for each employee
  - `start()`: Main game loop that:
    - Processes each employee's turn
    - Adds new customers periodically
    - Updates customer state
    - Checks win/loss conditions
    - Handles game over and retry logic

## Game Loop Logic

The game operates on a tick-based system where:

1. Each employee gets a turn to take an action based on their instructions
2. Customer waiting times are updated
3. New customers arrive periodically 
4. Unhappy customers leave if not served in time
5. The game ends when too many customers leave unhappy

## State Management Flow

1. `Game` initializes and manages `GameState`
2. `GameState` tracks `Customers` and `Orders`
3. `Employee` agents interact with the state through their actions
4. Changes to the state affect customer experience and game outcomes