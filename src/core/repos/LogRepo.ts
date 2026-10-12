import { GameLog } from '@core/models/GameLog';

export interface LogRepo {
    /**
     * Add a log to the repository
     */
    addLog(log: GameLog): void;

    /**
     * Get all logs from the repository
     */
    getLogs(): GameLog[];
} 