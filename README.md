# Diner Simulation Game

A terminal-based restaurant management game where you instruct AI employees to serve customers through natural language prompts.

## About LangGraph Multi-Node Architecture

This game demonstrates the power of LangGraph's multi-node architecture. Each employee in the game is powered by a LangGraph with multiple specialized nodes:

1. **Perception Node**: Observes the environment and gathers information about the restaurant state
2. **Planning Node**: Decides what action to take based on instructions and current state
3. **Action Nodes**: Specialized nodes for different actions (move, seat customers, take orders, etc.)

Benefits of this multi-node approach:

- **Separation of Concerns**: Each node handles a specific function (perception, planning, action)
- **Conditional Routing**: The planning node routes to the appropriate action node
- **State Management**: State is passed and updated between nodes
- **Customized Prompting**: Each node can use different prompts optimized for its specific task
- **Focused Decision Making**: Breaking the agent's work into smaller steps leads to better outcomes

## Setup

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Set up your Anthropic API key:
   - Copy `example.env` to `.env`
   - Add your Anthropic API key to the `.env` file

## Running the Game

```bash
python src/main.py
```

## How to Play

1. When the game starts, you'll be asked to give instructions to each employee
2. Craft your instructions carefully to create an efficient restaurant system
3. For example:
   - Jim: "Stay at the entrance and seat any customers who arrive"
   - Alice: "Take orders from seated customers and bring them to the kitchen"
   - Bob: "Cook any orders that come to the kitchen and have them ready for delivery"

4. Watch as your employees follow your instructions automatically
5. If too many customers leave unhappy, you'll get a chance to adjust your instructions
