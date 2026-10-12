/**
 * Interface for managing the relationship between employees and grills.
 */
export interface EmployeeGrillRepo {
    /**
     * Get the grill assigned to an employee by their ID
     */
    getEmployeeGrill(employeeId: string): string | null;

    /**
     * Set the grill assigned to an employee by their ID
     */
    setEmployeeGrill(employeeId: string, grillId: string): void;

    /**
     * Check if a grill is assigned to an employee
     */
    isGrillOccupied(grillId: string): boolean;
} 