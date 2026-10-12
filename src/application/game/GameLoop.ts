import { RestaurantWorld } from '@core/models/RestaurantWorld';
import { GameSession } from '@core/models/GameSession';
import { ActiveTurn, EmployeeUpdate } from '@core/models/ActiveTurn';

/**
 * GameLoop manages the core game loop, handling turns and state updates.
 * It uses a hybrid approach to state management, keeping both world state
 * and session state separate but coordinated.
 * 
 * This is an application service that orchestrates the game's core loop,
 * coordinating between the domain models and handling the game's progression.
 */
export class GameLoop {
    private world: RestaurantWorld;
    private session: GameSession;

    constructor(initialWorld: RestaurantWorld, initialSession: GameSession) {
        this.world = initialWorld;
        this.session = initialSession;
    }

    /**
     * Run the game loop, yielding state updates after each turn.
     * This is an async generator that yields both world and session state
     * after each turn is processed.
     */
    async *run(): AsyncGenerator<{ world: RestaurantWorld; session: GameSession }> {
        while (true) {
            const { currentActor } = this.session;
            
            // Handle the turn based on actor type
            if (currentActor.startsWith('Employee')) {
                await this.handleEmployeeTurn(currentActor);
            } else {
                await this.handleCustomerTurn(currentActor);
            }

            // Update session state
            this.session = this.nextTurn();
            
            // Yield both states together
            yield {
                world: this.world.clone(),
                session: this.session.clone()
            };
        }
    }

    /**
     * Handle an employee's turn
     */
    private async handleEmployeeTurn(employeeId: string): Promise<void> {
        // TODO: Implement employee turn logic
        // This will involve getting the next action from the AI agent
        // and executing it
    }

    /**
     * Handle a customer's turn
     */
    private async handleCustomerTurn(customerId: string): Promise<void> {
        // TODO: Implement customer turn logic
        // This will involve handling customer behavior
    }

    /**
     * Advance to the next turn
     */
    private nextTurn(): GameSession {
        const nextIndex = (this.session.turnNumber + 1) % this.session.actorOrder.length;
        return {
            ...this.session,
            currentActor: this.session.actorOrder[nextIndex],
            turnNumber: nextIndex,
            tick: this.session.tick + 1
        };
    }
} 