import { Entrance } from '@core/entities/Entrance';
import { EntranceRepo } from '@core/repos/EntranceRepo';

/**
 * Implementation of the EntranceRepo interface that stores entrances in an array.
 */
export class EntranceRepoImpl implements EntranceRepo {
    private entrances: Entrance[];

    constructor() {
        this.entrances = [];
    }

    getAllEntrances(): Entrance[] {
        return [...this.entrances];
    }

    addEntrance(entrance: Entrance): void {
        this.entrances.push(entrance);
    }
} 