import { EmployeeGrillRepo } from '@core/repos/EmployeeGrillRepo';

/**
 * Implementation of the EmployeeGrillRepo interface that manages the relationship
 * between employees and grills using a single Map.
 */
export class EmployeeGrillRepoImpl implements EmployeeGrillRepo {
    private employeeGrills: Map<string, string>; // employee_id -> grill_id

    constructor() {
        this.employeeGrills = new Map<string, string>();
    }

    getEmployeeGrill(employeeId: string): string | null {
        return this.employeeGrills.get(employeeId) || null;
    }

    setEmployeeGrill(employeeId: string, grillId: string): void {
        // Check if the grill is already assigned to another employee
        const grillEmployee = this.getEmployeeOfGrill(grillId);
        if (grillEmployee && grillEmployee !== employeeId) {
            throw new Error(`Grill ${grillId} is already assigned to employee ${grillEmployee}`);
        }
        
        // Set the new association
        this.employeeGrills.set(employeeId, grillId);
    }

    isGrillOccupied(grillId: string): boolean {
        return this.getEmployeeOfGrill(grillId) !== null;
    }

    private getGrillOfEmployee(employeeId: string): string | null {
        return this.employeeGrills.get(employeeId) || null;
    }

    private getEmployeeOfGrill(grillId: string): string | null {
        for (const [employeeId, assignedGrillId] of this.employeeGrills.entries()) {
            if (assignedGrillId === grillId) {
                return employeeId;
            }
        }
        return null;
    }
} 