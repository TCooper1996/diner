# 🍽️ Diner Simulation Game

A **terminal-based restaurant management game** where the player **instructs AI-powered employees** to serve customers through **natural language prompts**.

---

## **🏡 Game Setting**
You own a restaurant and must manage your employees to keep it running smoothly. 

**Key Tasks:**
- Seat customers as they arrive.
- Take and submit customer orders.
- Cook and serve food to the correct customers.
- Clean tables after customers leave.

**Game Mechanics:**
- Customers have expectations. If they receive **incorrect food** or are served **too late**, they become unhappy, which lowers the player's score.
- Employees **do not have predefined roles**—the player assigns them responsibilities through prompts before each level.

---

## **🛠️ Game Interactions**
### **Player Role**
The player **writes a prompt** to instruct each AI-powered employee on how they should behave. These instructions influence how each employee reacts to the game state.

### **AI Employees**
- Employees use **LLM-based decision-making** to select an action each turn.
- Employees **can only perform predefined actions** using **Tool Calling**.
- Each employee **invokes exactly 1 tool per turn**.

Employees **must be explicitly instructed** on which actions they should prioritize. For example, a waiter should not decide to **randomly start cooking** unless explicitly told.

---

## **🎯 Objective**
Each level has a set number of customers who will enter the restaurant over time. The goal is to:
1. Seat all customers properly.
2. Take and submit their orders to the kitchen.
3. Cook and serve orders in a timely manner.
4. Keep customers happy by delivering correct food **before they get impatient**.
5. Clean tables to allow new customers to sit.

The level ends when **all customers have been served and have left**.

---

## **🔄 Game Loop (Tick-Based Simulation)**
### **1️⃣ Pre-Game Phase (Prompting Employees)**
Before the level starts, the player **writes a natural language prompt** for each employee. For example:

- **Alice:** `"Alice will seat customers as they arrive."`
- **Jim:** `"Jim will take orders from seated customers, submit them to the kitchen, and deliver the food once cooked."`
- **Bob:** `"Bob will cook any orders that are submitted to the kitchen."`

### **2️⃣ Simulation Phase (AI Decision-Making)**
- The game progresses in discrete **ticks** (like in-game minutes).
- Each tick, employees **observe the game state** and choose an action **based on their prompt**.
- **One employee acts per tick** (they take turns).
- Employees invoke **exactly one tool per tick** to update the game state.

### **3️⃣ End of Tick**
- Once **all employees have acted**, the tick ends.
- The loop repeats until all customers have been served.

---

## **🚀 Additional Notes**
- **No direct player control during simulation:** The player **only defines the initial prompts**—employees act autonomously after that.
- **AI Employees follow instructions but may make mistakes** if prompts are unclear.
- **Tool calling is strictly enforced**—an employee can only perform actions using predefined tools.
- **Customers have patience levels**, and delaying their service too long **reduces the score**.