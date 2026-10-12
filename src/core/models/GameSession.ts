import { ActiveTurn } from './ActiveTurn';

/**
 * GameSession represents the application-level state of the game.
 * This includes turn management, game progression, and other session-level concerns.
 * 
 * This interface focuses on the game's progression and management, separate from
 * the actual state of the restaurant world.
 */
export interface GameSession {
    /**
     * The current actor (employee or customer) whose turn it is
     */
    currentActor: string;

    /**
     * The order in which actors take turns
     */
    actorOrder: string[];

    /**
     * The current turn number
     */
    turnNumber: number;

    /**
     * Whether the game is currently paused
     */
    isPaused: boolean;

    /**
     * The current tick number
     */
    tick: number;

    /**
     * Create a deep copy of the game session state
     */
    clone(): GameSession;
} 