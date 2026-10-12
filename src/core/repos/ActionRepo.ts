import { Action } from '@core/actions/Action';

export interface ActionRepo {
    /**
     * Set the action of an employee
     */
    setEmployeeAction(employeeId: string, action: Action | null): void;

    /**
     * Get the action of an employee
     */
    getEmployeeAction(employeeId: string): Action | null;
} 