import { Grill } from '@core/entities/Grill';

export interface GrillRepo {
    /**
     * Get all grills in the restaurant.
     */
    getAllGrills(): Grill[];

    /**
     * Get a specific grill by its ID.
     */
    getGrill(grillId: string): Grill;
} 