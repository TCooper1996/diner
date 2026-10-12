import { GameTurn } from "../models/TurnTypes";

export interface GameLogRepo {
    /**
     * Get the game log for a given game ID
     */
    getGameLogs(): GameTurn[];

    /**
     * Add a game log for a given game ID
     */
    addTurnEffect(turn: number, effects: string): void;

    addAgentInteraction(turn: number, agent_response: string, verification_error: string | null): void;
} 