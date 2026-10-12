import { ActionRepo } from '@core/repos/ActionRepo';
import { GameLogRepo } from '@core/repos/GameLogRepo';
import { AgentService } from '@core/services/AgentService';
import { RestaurantState } from './RestaurantState';

export type ActiveTurn = EmployeeUpdate | CustomerUpdate;

export interface EmployeeUpdate {
    index: string;
}

export interface CustomerUpdate {}

/**
 * GameState represents the current state of the game.
 * It extends RestaurantState and adds game-specific functionality like turns and ticks.
 */
export interface GameState {
    actions: ActionRepo,
    logs: GameLogRepo,
    agentService: AgentService,
    worldState: RestaurantState 
    /**
     * Get the current tick number
     */
    getTick(): number;

    /**
     * Get the current player's turn.
     * This is used to determine which player's turn it is in a multiplayer game.
     */
    getWhoseTurn(): ActiveTurn;

    /**
     * Set the current player's turn.
     * This is used to determine which player's turn it is in a multiplayer game.
     */
    setWhoseTurn(playerId: ActiveTurn): void;

    /**
     * Create a deep copy of the game state.
     * This is used to ensure that the game state can be passed around without
     * unintended side effects.
     */
    copy(): GameState;
} 