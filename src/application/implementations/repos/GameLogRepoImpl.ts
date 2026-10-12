import { GameTurn } from '@/core/models/TurnTypes';
import { GameLogRepo } from '@core/repos/GameLogRepo';


/**
 * Implementation of the GameLogRepo interface that stores game logs in a Map.
 */
export class GameLogRepoImpl implements GameLogRepo {
    private gameLogs: Map<number, GameTurn>;

    constructor() {
        this.gameLogs = new Map<number, GameTurn>();
    }

    getGameLogs(): GameTurn[] {
        return Array.from(this.gameLogs.values());
    }

    addTurnLog(turn: number, turnType: GameTurn): void {
        this.gameLogs.set(turn, turnType);
    }

} 