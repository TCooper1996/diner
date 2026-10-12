import { Entrance } from '@core/entities/Entrance';

export interface EntranceRepo {
    /**
     * Get all entrances in the restaurant.
     */
    getAllEntrances(): Entrance[];
} 