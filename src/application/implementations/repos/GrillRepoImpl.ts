import { Grill } from '@core/entities/Grill';
import { GrillRepo } from '@core/repos/GrillRepo';

/**
 * Implementation of the GrillRepo interface that stores grills in a Map.
 */
export class GrillRepoImpl implements GrillRepo {
    private grills: Map<string, Grill>;

    constructor() {
        this.grills = new Map<string, Grill>();
    }

    getAllGrills(): Grill[] {
        return Array.from(this.grills.values());
    }

    addGrill(grill: Grill): void {
        if (this.grills.has(grill.grillId)) {
            throw new Error(`Grill with ID ${grill.grillId} already exists`);
        }
        this.grills.set(grill.grillId, grill);
    }

    getGrill(grillId: string): Grill {
        const grill = this.grills.get(grillId);
        if (!grill) {
            throw new Error(`No grill found with ID ${grillId}`);
        }
        return grill;
    }
} 