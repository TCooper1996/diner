# Actions

This directory contains all the actions that can be performed in the diner simulation. Each action is contained in its own module with a consistent structure.

## Action Module Structure

Each action module contains:

1. A tool definition class (e.g., `MoveTool`) that's used by the agent system
2. A tool function (e.g., `move_tool()`) that creates the tool for the agent
3. A validation function (e.g., `validate_move()`) that checks if the action can be performed
4. A state-changing function (e.g., `move_to_location()`) that actually performs the action

## Available Actions

- **Move**: Move an employee to a different location (entrance, dining, kitchen)
- **Seat**: Seat a waiting customer at a table in the dining area
- **Take Order**: Take an order from a seated customer
- **Notify Kitchen**: Notify the kitchen about pending orders
- **Cook**: Cook food for a taken order
- **Deliver**: Deliver cooked food to a customer
- **Wait**: Take no action
- **Observe**: Look around the current location (utility action, not directly invoked by agents)

## Action Flow

1. Agent selects an action to perform
2. The action is parsed into a tool object
3. The validation function is called to check if the action can be performed
4. If valid, the state-changing function is called to update the game state
5. An ActionResult is returned with success/failure status, a message, and the updated game state

## Benefits of This Architecture

- Each action is self-contained in its own module
- Clear separation between validation and state changes
- Consistent interface across all actions
- Easier to add new actions without modifying multiple files
- Better organization of code functionality