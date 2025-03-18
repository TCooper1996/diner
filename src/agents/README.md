# Agents Directory

## Overview

This directory contains the AI-powered employee agents that operate within the restaurant simulation. Each agent uses a LangGraph multi-node architecture to perform actions based on natural language instructions.

## Technical Details

### `employee.py`

#### `AgentState` TypedDict

Defines the state that flows through the LangGraph nodes:

- `messages`: List of conversation messages (maintains context between nodes)
- `location`: Current employee location (entrance, dining, kitchen)
- `next_node`: String indicating which node to execute next
- `game_state_info`: Serialized game state information
- `action_result`: String containing the result of the most recent action

#### `Employee` Class

The core agent class that wraps the LangGraph implementation:

- **Constructor**:
  - Takes a `name` and natural language `instruction` 
  - Initializes the employee at the ENTRANCE location
  - Creates the Claude LLM instance
  - Builds and compiles the LangGraph

- **`_build_graph()`**:
  Creates the multi-node graph structure with:
  
  - **Perception Node**: Processes the current game state and location
  - **Planning Node**: Uses Claude to decide what action to take based on instructions
  - **Action Nodes**:
    - `move_node`: Changes employee location
    - `seat_node`: Seats waiting customers
    - `order_node`: Takes customer orders
    - `cook_node`: Prepares food
    - `deliver_node`: Delivers food to customers
    - `observe_node`: Looks around the current location
  
  The graph uses conditional routing via `add_conditional_edges` where the planning node determines which action node to execute next.

- **`process()`**:
  - Takes the current game state
  - Serializes it for the LLM
  - Initializes agent state
  - Runs the graph
  - Updates the employee's location
  - Returns the action result

- **`_prepare_game_state()`**:
  - Converts the GameState object to a serializable dict
  - Formats customer and order information

## LangGraph Multi-Node Architecture Benefits

This implementation showcases the following benefits of multi-node graphs:

1. **Separation of Concerns**: Each node handles a specific function - perception, planning, or action execution

2. **Conditional Routing**: The planning node decides which action node should be called based on the situation

3. **State Management**: The AgentState dict is passed between nodes, allowing them to share and update information

4. **Customized Processing**: Each node can implement specialized logic for its function

5. **Reduced Prompt Complexity**: Instead of one large, complex prompt, each node can have simpler, focused logic